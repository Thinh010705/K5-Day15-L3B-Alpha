"""Đếm số liệu pain từ data pre-class BTC — theo đúng cách đếm ở evidence/data-mining.md mục 1.

Chạy (chỉ thư viện chuẩn, cần chạy evidence/prepare_data.py trước):
  python evidence/count.py                          # đọc data-btc/preclass → in bảng + ghi evidence/data-mining-output.json
  python evidence/count.py --data <thư mục> --out <file.json>

Chỉ in / ghi số đã tổng hợp (x/N, %, trung vị…). Không chép dòng data nào ra ngoài.
Mã số liệu (P0–P2, M1, M4, M5, M7, M8, V1–V3) khớp bảng trong evidence/data-mining.md.
"""
import argparse
import csv
import json
import math
import os
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_DATA = os.path.join(ROOT, "data-btc", "preclass")
DEFAULT_OUT = os.path.join(ROOT, "evidence", "data-mining-output.json")
TA = "teaching_assistant"
VIDEO_Q = "video_question"
EVENT_TYPES_KEPT = ("agent_replied",)

# Ngưỡng do nhóm tự chọn — ghi ở evidence/data-mining.md mục 1.
FOLLOW_UP_MIN = 5     # M5: hỏi tiếp trong 5 phút
SESSION_GAP_MIN = 30  # V2: hai lượt cách nhau ≤ 30 phút là cùng một phiên hỏi
SLOW_MS = 10000       # M7: chờ > 10 giây
HYPOTHESIS_M1 = 0.20  # evidence/hypothesis.md: ≥ 20% phản hồi trợ giảng không có mốc trích dẫn


# ---------- tiện ích ----------
def parse_ts(s):
    return datetime.fromisoformat(s) if s else None


def video_stem(s):
    """'Day01/d01-r1-v05.txt' hoặc 'd01-r1-v05' → 'd01-r1-v05'."""
    if not s:
        return ""
    base = s.rsplit("/", 1)[-1]
    return base[:-4] if base.endswith(".txt") else base


def rate_text(x, n):
    return "%d/%d (%.1f%%)" % (x, n, 100.0 * x / n) if n else "%d/%d (—)" % (x, n)


def rate(x, n):
    return {"x": x, "n": n, "pct": round(100.0 * x / n, 1) if n else None, "text": rate_text(x, n)}


def percentile(values, p):
    """Phân vị kiểu nearest-rank (không nội suy) — dễ kiểm tay."""
    v = sorted(values)
    return v[max(0, math.ceil(p / 100.0 * len(v)) - 1)] if v else None


def describe(values):
    if not values:
        return {"n": 0}
    return {"n": len(values), "mean": round(sum(values) / len(values), 2), "median": percentile(values, 50),
            "p75": percentile(values, 75), "p90": percentile(values, 90), "max": max(values)}


def read_csv(path, keep=None):
    with open(path, encoding="utf-8-sig", newline="") as f:
        return [r for r in csv.DictReader(f) if keep is None or keep(r)]


def utc_date(ts):
    return ts.astimezone(timezone.utc).date()


def day_span(start, end):
    return (utc_date(end) - utc_date(start)).days + 1


# ---------- dựng lượt hỏi ----------
def build_turns(chats, events):
    """Mỗi dòng chat.csv → một lượt, gắn data của agent_replied (nối events.ref_id = chat.id)."""
    replies = {e["ref_id"]: e for e in events if e.get("type") == "agent_replied" and e.get("ref_id")}
    turns = []
    for c in chats:
        e = replies.get(c["id"])
        reply = json.loads(e["data"]) if e and e.get("data") else None
        created = parse_ts(c.get("created_at"))
        asked = parse_ts(c.get("asked_at")) or created  # thiếu giờ gửi thì lấy giờ ghi câu trả lời
        turns.append({
            "id": c["id"], "hv": c["hv"], "channel": c.get("channel", ""), "agent": c.get("agent_id", ""),
            "ta": c.get("agent_id") == TA, "video": video_stem(c.get("transcript", "")),
            "asked_at": asked, "created_at": created,
            "reply_at": parse_ts(e["occurred_at"]) if e else created, "reply": reply,
            "cached": (reply or {}).get("cached", c.get("cached") == "True"),
            "q_len": int(c["do_dai_cau_hoi"]) if c.get("do_dai_cau_hoi") else None,
            "a_len": int(c["do_dai_tra_loi"]) if c.get("do_dai_tra_loi") else None,
        })
    turns.sort(key=lambda t: t["asked_at"])
    return turns


def ta_turns(turns):
    return [t for t in turns if t["ta"]]


def citation_start(turns):
    """00:00 UTC của ngày đầu tiên có câu trả lời ghi khoá moc_trich_dan."""
    times = [t["reply_at"] for t in turns if t["reply"] and "moc_trich_dan" in t["reply"]]
    if not times:
        return None
    d = min(times).astimezone(timezone.utc)
    return datetime(d.year, d.month, d.day, tzinfo=timezone.utc)


def people_stats(in_n, is_x, days):
    """Số người gặp (≥1 lần x) / số người trong mẫu số, số lần trung bình mỗi người gặp, đổi ra / tháng."""
    per = defaultdict(int)
    people_n = set()
    for t in in_n:
        people_n.add(t["hv"])
        if is_x(t):
            per[t["hv"]] += 1
    mean = round(sum(per.values()) / len(per), 2) if per else 0.0
    return {"people_x": len(per), "people_n": len(people_n), "people": rate_text(len(per), len(people_n)),
            "mean_per_affected": mean, "per_month_per_affected": round(mean * 30.0 / days, 2) if days else None,
            "window_days": days}


# ---------- M1: không có mốc trích dẫn ----------
def has_citation_key(t):
    return bool(t["reply"]) and "moc_trich_dan" in t["reply"]


def no_citation(t):
    return has_citation_key(t) and t["reply"]["moc_trich_dan"] == []


def m1_no_citation(turns, start=None, exclude_missing_context=False):
    """exclude_missing_context=True: độ nhạy — bỏ lượt AI ghi thiếu ngữ cảnh (có thể là câu hỏi lại, không cần mốc)."""
    start = start or citation_start(turns)
    win = [t for t in ta_turns(turns) if start and t["reply_at"] >= start]
    n_rows = [t for t in win if has_citation_key(t)]
    if exclude_missing_context:
        n_rows = [t for t in n_rows if t["reply"].get("missing_context") is not True]
    x = sum(1 for t in n_rows if no_citation(t))
    u = sum(1 for t in win if not has_citation_key(t))
    end = max((t["reply_at"] for t in turns), default=start)
    res = rate(x, len(n_rows))
    res.update({
        "window_start": utc_date(start).isoformat() if start else None, "window_end": utc_date(end).isoformat() if end else None,
        "u": u, "bound_low": rate_text(x, len(n_rows) + u), "bound_high": rate_text(x + u, len(n_rows) + u),
        "hypothesis_threshold_pct": 100 * HYPOTHESIS_M1,
        "meets_hypothesis": (x / len(n_rows) >= HYPOTHESIS_M1) if n_rows else None,
        "by_channel": {}, "by_cached": {},
    })
    for key, field in (("by_channel", "channel"), ("by_cached", "cached")):
        groups = defaultdict(list)
        for t in n_rows:
            groups[str(t[field])].append(t)
        res[key] = {g: rate(sum(1 for t in ts if no_citation(t)), len(ts)) for g, ts in sorted(groups.items())}
    res.update(people_stats(n_rows, no_citation, day_span(start, end) if start else 0))
    return res


# ---------- hành vi sau câu trả lời ----------


def m8_verdict_reply_kind(turns, sent):
    """verdict / reply_kind ghi ở lượt nào? (kế hoạch §5.1 định dùng cho A1.3) — chỉ mô tả, không làm mẫu số."""
    out = {}
    for key in ("verdict", "reply_kind"):
        rows = [t for t in turns if t["reply"] and key in t["reply"]]
        values, agents = defaultdict(int), defaultdict(int)
        for t in rows:
            values[t["reply"][key]] += 1
            agents[t["agent"]] += 1
        out[key] = {"n": len(rows), "values": dict(sorted(values.items())), "agents": dict(sorted(agents.items())),
                    "tren_khung_thao_luan": rate_text(sum(t["channel"] == "video_discussion_reply" for t in rows), len(rows)),
                    "tra_loi_lai_mot_loi_AI": rate_text(sum("reply_to" in sent.get(t["id"], {}) for t in rows), len(rows))}
    return out


def m5_follow_up(turns, minutes=FOLLOW_UP_MIN):
    base = [t for t in ta_turns(turns) if t["channel"] == VIDEO_Q and t["video"]]
    by_key = defaultdict(list)
    for t in ta_turns(turns):
        by_key[(t["hv"], t["video"])].append(t["asked_at"])
    x = 0
    for t in base:
        end = t["created_at"] + timedelta(minutes=minutes)
        x += any(t["created_at"] < a <= end for a in by_key[(t["hv"], t["video"])])
    res = rate(x, len(base))
    res["minutes"] = minutes
    return res


# ---------- M4, M7, M8 ----------
def data_days(turns):
    times = [t["asked_at"] for t in turns if t["asked_at"]]
    return day_span(min(times), max(times)) if times else 0


def m4_missing_context(turns, days=None):
    rows = [t for t in ta_turns(turns) if t["reply"] and "missing_context" in t["reply"]]
    is_x = lambda t: t["reply"]["missing_context"] is True  # noqa: E731
    res = rate(sum(1 for t in rows if is_x(t)), len(rows))
    res.update(people_stats(rows, is_x, days if days is not None else data_days(turns)))
    return res


def m7_latency(turns):
    lat = [t["reply"]["latency_ms"] for t in ta_turns(turns)
           if t["reply"] and isinstance(t["reply"].get("latency_ms"), (int, float)) and not t["cached"]]
    return {"n": len(lat), "median_ms": percentile(lat, 50), "p90_ms": percentile(lat, 90),
            "over_10s": rate(sum(1 for v in lat if v > SLOW_MS), len(lat))}


# ---------- V1, V2: khối lượng ----------
def session_sizes(times, gap_minutes=SESSION_GAP_MIN):
    """Số lượt của từng phiên hỏi: lượt cách lượt trước > gap_minutes thì mở phiên mới."""
    times = sorted(times)
    sizes = [1] if times else []
    for a, b in zip(times, times[1:]):
        if b - a > timedelta(minutes=gap_minutes):
            sizes.append(1)
        else:
            sizes[-1] += 1
    return sizes


def ta_times_by_hv(turns):
    per = defaultdict(list)
    for t in ta_turns(turns):
        per[t["hv"]].append(t["asked_at"])
    return per


def volume(turns, gap_minutes=SESSION_GAP_MIN):
    per = ta_times_by_hv(turns)
    sessions_per, turns_per_session = [], []
    for times in per.values():
        sizes = session_sizes(times, gap_minutes)
        sessions_per.append(len(sizes))
        turns_per_session.extend(sizes)
    days = data_days(turns)
    return {"people": len(per), "turns_total": sum(len(v) for v in per.values()),
            "turns_per_person": describe([len(v) for v in per.values()]),
            "sessions_total": len(turns_per_session), "sessions_per_person": describe(sessions_per),
            "turns_per_session": describe(turns_per_session), "session_gap_minutes": gap_minutes,
            "days": days, "per_month_factor": round(30.0 / days, 3) if days else None}


# ---------- V3: persona cho cost/personas.yaml ----------
# Quy tắc (chốt trước khi chạy, ghi ở evidence/data-mining.md): chia người hỏi trợ giảng (P2) theo số phiên hỏi
# trong cửa sổ data: 1 phiên = dung_it · 2–3 phiên = dung_vua · ≥4 phiên = dung_nhieu.
PERSONA_RULES = (("dung_it", 1, 1), ("dung_vua", 2, 3), ("dung_nhieu", 4, None))


def personas(turns, days=None, gap_minutes=SESSION_GAP_MIN):
    days = days if days is not None else data_days(turns)
    groups = {name: [] for name, _, _ in PERSONA_RULES}
    for times in ta_times_by_hv(turns).values():
        sizes = session_sizes(times, gap_minutes)
        for name, lo, hi in PERSONA_RULES:
            if len(sizes) >= lo and (hi is None or len(sizes) <= hi):
                groups[name].append(sizes)
    total = sum(len(g) for g in groups.values())
    out = []
    for name, lo, hi in PERSONA_RULES:
        g = groups[name]
        sessions = [len(s) for s in g]
        turns_n = [sum(s) for s in g]
        mean_s = sum(sessions) / len(g) if g else 0.0
        tps = sum(turns_n) / sum(sessions) if g else 0.0
        out.append({"name": name, "rule_sessions": "%d%s" % (lo, "+" if hi is None else ("" if hi == lo else "-%d" % hi)),
                    "people": len(g), "share": round(len(g) / total, 3) if total else 0.0,
                    "sessions_mean": round(mean_s, 2), "uses_per_month": round(mean_s * 30.0 / days, 1) if days else None,
                    "turns_per_session_mean": round(tps, 2), "turns_per_session": int(tps + 0.5), "window_days": days})
    return out


# ---------- dữ liệu cho bộ câu thử (evidence/data-mining.md mục 7) ----------
LENGTH_BUCKETS = ((20, "1-20"), (60, "21-60"), (150, "61-150"))


def length_bucket(n):
    if n is None:
        return "?"
    for top, name in LENGTH_BUCKETS:
        if n <= top:
            return name
    return ">150"


def breakdowns(turns):
    """Lượt trợ giảng theo độ dài câu hỏi, kèm tỉ lệ M4 (thiếu ngữ cảnh) và M1 (không có mốc) — dữ liệu cho bộ câu thử."""
    by_len = defaultdict(list)
    for t in ta_turns(turns):
        by_len[length_bucket(t["q_len"])].append(t)

    def stats(rows):
        mc = [t for t in rows if t["reply"] and "missing_context" in t["reply"]]
        cit = [t for t in rows if has_citation_key(t)]
        return {"n": len(rows), "missing_context": rate(sum(t["reply"]["missing_context"] is True for t in mc), len(mc)),
                "no_citation": rate(sum(no_citation(t) for t in cit), len(cit))}

    order = [name for _, name in LENGTH_BUCKETS] + [">150", "?"]
    return {"by_length": {b: stats(by_len[b]) for b in order if by_len.get(b)}}


# ---------- ví dụ cụ thể (mục 4 của data-mining.md) ----------
def _example(kind, t, **extra):
    """Chỉ mã lượt chat (đã ẩn danh), ngày, video, độ dài — KHÔNG đưa mã học viên."""
    e = {"kind": kind, "chat_id": t["id"], "ngay_utc": utc_date(t["asked_at"]).isoformat(), "channel": t["channel"],
         "video": t["video"], "do_dai_cau_hoi": t["q_len"], "do_dai_tra_loi": t["a_len"]}
    e.update(extra)
    return e


def examples(turns, per_kind=2):
    """Lấy per_kind lượt sớm nhất cho mỗi kiểu (M1, M4, M5) — tất định, ai chạy lại cũng ra cùng mã."""
    start = citation_start(turns)
    ta = ta_turns(turns)
    win = [t for t in ta if start and t["reply_at"] >= start and has_citation_key(t)]
    video_q = {t["id"] for t in ta if t["channel"] == VIDEO_Q and t["video"]}
    by_key = defaultdict(list)
    for t in ta:
        by_key[(t["hv"], t["video"])].append(t["asked_at"])
    kinds = [
        ("khong_trich_dan", [t for t in win if no_citation(t)], lambda t: {"moc": []}),
        ("thieu_ngu_canh", [t for t in ta if t["reply"] and t["reply"].get("missing_context") is True],
         lambda t: {"missing_context": True}),
        ("hoi_tiep_5_phut",
         [t for t in ta if t["id"] in video_q and any(
             t["created_at"] < a <= t["created_at"] + timedelta(minutes=FOLLOW_UP_MIN) for a in by_key[(t["hv"], t["video"])])],
         lambda t: {}),
    ]
    out = []
    for kind, rows, extra in kinds:
        for t in sorted(rows, key=lambda r: r["asked_at"])[:per_kind]:
            out.append(_example(kind, t, **extra(t)))
    return out


# ---------- chạy trên data thật ----------
def compute(folder):
    learners = read_csv(os.path.join(folder, "learners.csv"))
    chats = read_csv(os.path.join(folder, "chat.csv"))
    active, first, last, events, sent = set(), None, None, [], {}
    with open(os.path.join(folder, "events.csv"), encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            if r["actor"] == "learner":
                active.add(r["hv"])
            ts = r["occurred_at"]
            first, last = min(first or ts, ts), max(last or ts, ts)
            if r["type"] in EVENT_TYPES_KEPT:
                events.append(r)
            elif r["type"] == "chat_sent" and r["ref_id"]:
                sent[r["ref_id"]] = json.loads(r["data"]) if r["data"] else {}
    turns = build_turns(chats, events)
    ta = ta_turns(turns)
    return {
        "data": {"folder": os.path.relpath(folder, ROOT), "first_event_utc": first, "last_event_utc": last},
        "P0_tai_khoan": len(learners),
        "P1_co_hoat_dong": rate(len(active), len(learners)),
        "P2_hoi_tro_giang": rate(len({t["hv"] for t in ta}), len(active)),
        "P2_hoi_duoi_video": rate(len({t["hv"] for t in ta if t["channel"] == VIDEO_Q}), len(active)),
        "luot_tro_giang": rate(len(ta), len(turns)),
        "M1_khong_moc_trich_dan": m1_no_citation(turns),
        "M1_do_nhay_bo_thieu_ngu_canh": m1_no_citation(turns, exclude_missing_context=True),
        "M4_thieu_ngu_canh": m4_missing_context(turns),
        "M5_hoi_tiep_5_phut": m5_follow_up(turns),
        "M5_do_nhay": {"2_phut": m5_follow_up(turns, minutes=2), "10_phut": m5_follow_up(turns, minutes=10)},
        "M7_do_tre": m7_latency(turns),
        "M8_verdict_reply_kind": m8_verdict_reply_kind(turns, sent),
        "V_khoi_luong": volume(turns),
        "V3_persona": personas(turns),
        "phan_ra": breakdowns(turns),
        "vi_du": examples(turns),
    }


def print_report(r):
    m1 = r["M1_khong_moc_trich_dan"]
    rows = [
        ("P1 người có hoạt động / tài khoản", r["P1_co_hoat_dong"]["text"]),
        ("P2 người hỏi trợ giảng / người có hoạt động", r["P2_hoi_tro_giang"]["text"]),
        ("Lượt trợ giảng / mọi lượt chat", r["luot_tro_giang"]["text"]),
        ("M1 lượt trợ giảng không có mốc trích dẫn (%s → %s)" % (m1["window_start"], m1["window_end"]), m1["text"]),
        ("M1 khoảng chặn nếu tính cả %d lượt không ghi khoá" % m1["u"], "%s … %s" % (m1["bound_low"], m1["bound_high"])),
        ("M1 người gặp ≥1 lần", m1["people"]),
        ("M4 lượt trợ giảng thiếu ngữ cảnh", r["M4_thieu_ngu_canh"]["text"]),
        ("M4 người gặp ≥1 lần", r["M4_thieu_ngu_canh"]["people"]),
        ("M5 lượt hỏi dưới video → hỏi tiếp trong 5 phút", r["M5_hoi_tiep_5_phut"]["text"]),
        ("M7 độ trễ trung vị / p90 (ms)", "%s / %s" % (r["M7_do_tre"]["median_ms"], r["M7_do_tre"]["p90_ms"])),
        ("M7 lượt chờ > 10 giây", r["M7_do_tre"]["over_10s"]["text"]),
    ]
    print("| Đếm gì | Kết quả |\n|---|---|")
    for k, v in rows:
        print("| %s | %s |" % (k, v))
    print("Ngưỡng giả thuyết M1 ≥ %.0f%%: %s" % (m1["hypothesis_threshold_pct"],
          "ĐẠT" if m1["meets_hypothesis"] else "KHÔNG ĐẠT" if m1["meets_hypothesis"] is False else "chưa tính được"))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--data", default=DEFAULT_DATA, help="thư mục preclass đã chuẩn hoá (mặc định data-btc/preclass)")
    ap.add_argument("--out", default=DEFAULT_OUT, help="file JSON ghi số tổng hợp")
    a = ap.parse_args(argv)
    if not os.path.isfile(os.path.join(a.data, "events.csv")):
        sys.exit("Không thấy %s/events.csv — chạy python evidence/prepare_data.py trước." % a.data)
    r = compute(a.data)
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(r, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print_report(r)
    print("Đã ghi " + os.path.relpath(a.out, ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())

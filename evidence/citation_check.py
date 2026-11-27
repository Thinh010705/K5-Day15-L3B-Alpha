"""Kiểm chéo của TV1: sau câu trả lời KHÔNG có mốc trích dẫn, học viên có hỏi tiếp / tua lùi nhiều hơn không?

Vì sao có file này: giả thuyết (evidence/hypothesis.md) nói thiếu mốc trích dẫn khiến học viên "phải tua lại
video, hỏi tiếp". count.py (TV2) đã đếm M1 (tỉ lệ thiếu mốc) và M5 (hỏi tiếp) nhưng không tách M5 theo có / không
có mốc. File này chỉ làm đúng việc đó, dùng lại hàm và định nghĩa của count.py để không ra bộ số thứ hai.

Chạy (sau evidence/prepare_data.py):
  python evidence/citation_check.py                 # đọc data-btc/preclass
  python evidence/citation_check.py --data <thư mục>

Cách đếm (viết trước khi chạy):
- Tập: lượt trợ giảng, kênh video_question, có ghi khoá moc_trich_dan, trả lời từ ngày bắt đầu ghi khoá
  (citation_start của count.py) — chính là mẫu số M1 thu về câu hỏi dưới video.
- Chia hai nhóm: moc_trich_dan = [] (không có mốc) và có ≥1 mốc.
- Hỏi tiếp: định nghĩa M5 của count.py — cùng học viên hỏi trợ giảng về CÙNG video trong 5 phút sau câu trả lời.
- Tua lùi: cùng học viên có video_seeked với to < from, cùng video, trong 5 phút sau câu trả lời.
- Chỉ là dấu vết hành vi, không kết luận nguyên nhân. Chỉ in số tổng hợp.
"""
import argparse
import csv
import json
import os
import sys
from collections import defaultdict
from datetime import timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import count  # noqa: E402  (evidence/count.py của TV2)

WINDOW = timedelta(minutes=count.FOLLOW_UP_MIN)


def load(folder):
    chats = count.read_csv(os.path.join(folder, "chat.csv"))
    replies, seeks = [], defaultdict(list)
    with open(os.path.join(folder, "events.csv"), encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            if r["type"] == "agent_replied":
                replies.append(r)
            elif r["type"] == "video_seeked" and r["video"]:
                d = json.loads(r["data"]) if r["data"] else {}
                try:
                    back = float(d.get("to")) < float(d.get("from"))
                except (TypeError, ValueError):
                    back = False
                if back:
                    seeks[(r["hv"], r["video"])].append(count.parse_ts(r["occurred_at"]))
    return count.build_turns(chats, replies), seeks


def compute(folder):
    turns, seeks = load(folder)
    start = count.citation_start(turns)
    asks = defaultdict(list)
    for t in count.ta_turns(turns):
        asks[(t["hv"], t["video"])].append(t["asked_at"])
    base = [t for t in count.ta_turns(turns)
            if t["channel"] == count.VIDEO_Q and t["video"] and t["reply_at"] >= start and count.has_citation_key(t)]
    out = {}
    for name, group in (("khong_moc", [t for t in base if count.no_citation(t)]),
                        ("co_moc", [t for t in base if not count.no_citation(t)])):
        ask = back = either = mc = 0
        for t in group:
            end = t["created_at"] + WINDOW
            a = any(t["created_at"] < x <= end for x in asks[(t["hv"], t["video"])])
            # video trong events là mã video (vd d01-r1-v01), khớp video_stem của transcript
            b = any(t["created_at"] < x <= end for x in seeks[(t["hv"], t["video"])])
            ask, back, either = ask + a, back + b, either + (a or b)
            mc += t["reply"].get("missing_context") is True
        n = len(group)
        out[name] = {"n": n, "hoi_tiep": count.rate_text(ask, n), "tua_lui": count.rate_text(back, n),
                     "hoi_tiep_hoac_tua_lui": count.rate_text(either, n), "thieu_ngu_canh": count.rate_text(mc, n)}
    out["window_start"] = count.utc_date(start).isoformat()
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--data", default=count.DEFAULT_DATA)
    a = ap.parse_args(argv)
    r = compute(a.data)
    print(f"Câu hỏi dưới video, trợ giảng trả lời từ {r['window_start']}, trong {count.FOLLOW_UP_MIN} phút sau câu trả lời:")
    print("| Nhóm | n | Hỏi tiếp cùng video | Tua lùi cùng video | Hỏi tiếp hoặc tua lùi | AI ghi thiếu ngữ cảnh |")
    print("|---|---|---|---|---|---|")
    for key, label in (("khong_moc", "Không có mốc"), ("co_moc", "Có mốc")):
        g = r[key]
        print(f"| {label} | {g['n']} | {g['hoi_tiep']} | {g['tua_lui']} | {g['hoi_tiep_hoac_tua_lui']} | {g['thieu_ngu_canh']} |")


if __name__ == "__main__":
    main()

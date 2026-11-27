"""Test cho evidence/count.py — chạy: python -m unittest discover -s evidence/tests -v"""
import json
import os
import sys
import unittest
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # thư mục evidence/
import count  # noqa: E402


def ts(day, hh=10, mm=0, ss=0):
    return "2026-11-%02dT%02d:%02d:%02d.000000+00:00" % (day, hh, mm, ss)


def chat(cid, hv="L1", day=13, hh=10, mm=0, agent="teaching_assistant", channel="video_question", video="Day01/d01-r1-v01.txt"):
    return {"id": cid, "hv": hv, "channel": channel, "agent_id": agent, "transcript": video,
            "asked_at": ts(day, hh, mm, 0), "created_at": ts(day, hh, mm, 5), "cached": "False"}


def replied(cid, hv="L1", day=13, hh=10, mm=0, **data):
    return {"hv": hv, "actor": "agent", "type": "agent_replied", "video": "", "ref_id": cid,
            "data": json.dumps(data), "occurred_at": ts(day, hh, mm, 5)}


def seek(hv="L1", day=13, hh=10, mm=1, video="d01-r1-v01", by="player", frm=100, to=50):
    return {"hv": hv, "actor": "learner", "type": "video_seeked", "video": video, "ref_id": "",
            "data": json.dumps({"by": by, "from": frm, "to": to, "crossed_stop": False}), "occurred_at": ts(day, hh, mm, 30)}


class HelpersTest(unittest.TestCase):
    def test_video_stem_from_transcript_path(self):
        self.assertEqual(count.video_stem("Day01/d01-r1-v05.txt"), "d01-r1-v05")
        self.assertEqual(count.video_stem("d01-r1-v05"), "d01-r1-v05")
        self.assertEqual(count.video_stem(""), "")

    def test_rate_text(self):
        self.assertEqual(count.rate_text(1, 4), "1/4 (25.0%)")
        self.assertEqual(count.rate_text(0, 0), "0/0 (—)")

    def test_percentile_nearest_rank(self):
        self.assertEqual(count.percentile([1, 2, 3, 4], 50), 2)
        self.assertEqual(count.percentile([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 90), 9)


class CitationTest(unittest.TestCase):
    def turns(self, chats, events):
        return count.build_turns(chats, events)

    def test_window_starts_at_first_day_with_citation_key(self):
        t = self.turns([chat("C1", day=10), chat("C2", day=13, hh=15)],
                       [replied("C1", day=10, missing_context=False), replied("C2", day=13, hh=15, moc_trich_dan=[])])
        self.assertEqual(count.citation_start(t), datetime(2026, 11, 13, tzinfo=timezone.utc))

    def test_empty_list_counts_as_no_citation_absent_key_is_excluded(self):
        chats = [chat("C1", day=10), chat("C2", day=13), chat("C3", day=13, hh=11), chat("C4", day=14), chat("C5", day=14, hh=11)]
        events = [replied("C1", day=10),                                   # trước cửa sổ: bỏ
                  replied("C2", day=13, moc_trich_dan=[]),                  # x
                  replied("C3", day=13, hh=11, moc_trich_dan=["@16"]),     # có trích dẫn
                  replied("C4", day=14, moc_trich_dan=["Day01/d01-r1-v01.txt@5"]),
                  replied("C5", day=14, hh=11, missing_context=False)]      # trong cửa sổ nhưng không ghi khoá → u
        m = count.m1_no_citation(self.turns(chats, events))
        self.assertEqual((m["x"], m["n"], m["u"]), (1, 3, 1))
        self.assertEqual(m["bound_low"], "1/4 (25.0%)")
        self.assertEqual(m["bound_high"], "2/4 (50.0%)")

    def test_classmate_replies_are_not_counted(self):
        chats = [chat("C1", day=13), chat("C2", day=13, hh=11, agent="classmate_clown", channel="video_discussion_reply")]
        events = [replied("C1", day=13, moc_trich_dan=["@1"]), replied("C2", day=13, hh=11, moc_trich_dan=[])]
        m = count.m1_no_citation(self.turns(chats, events))
        self.assertEqual((m["x"], m["n"]), (0, 1))

    def test_people_counts_and_frequency(self):
        chats = [chat("C1", hv="L1", day=13), chat("C2", hv="L1", day=14), chat("C3", hv="L2", day=14)]
        events = [replied("C1", hv="L1", day=13, moc_trich_dan=[]), replied("C2", hv="L1", day=14, moc_trich_dan=[]),
                  replied("C3", hv="L2", day=14, moc_trich_dan=["@3"])]
        m = count.m1_no_citation(self.turns(chats, events))
        self.assertEqual((m["people_x"], m["people_n"]), (1, 2))
        self.assertEqual(m["mean_per_affected"], 2.0)


class BehaviourAfterReplyTest(unittest.TestCase):
    def setUp(self):
        self.chats = [chat("C1", day=13, hh=10, mm=0)]

    def m3(self, *seeks, cite=None):
        ev = [replied("C1", day=13, moc_trich_dan=cite if cite is not None else [])] + list(seeks)
        t = count.build_turns(self.chats, ev)
        return count.m3_rewind(t, count.seeks_by_hv(ev))

    def test_backward_seek_same_video_within_5_minutes_counts(self):
        self.assertEqual(self.m3(seek(mm=3))["all"]["x"], 1)

    def test_forward_seek_does_not_count(self):
        self.assertEqual(self.m3(seek(mm=3, frm=10, to=90))["all"]["x"], 0)

    def test_seek_in_other_video_does_not_count(self):
        self.assertEqual(self.m3(seek(mm=3, video="d02-r1-v01"))["all"]["x"], 0)

    def test_seek_after_window_does_not_count(self):
        self.assertEqual(self.m3(seek(mm=6))["all"]["x"], 0)

    def test_link_seek_is_not_a_rewind(self):
        self.assertEqual(self.m3(seek(mm=3, by="link"))["all"]["x"], 0)

    def test_rewind_split_by_citation(self):
        m = self.m3(seek(mm=3), cite=["@5"])
        self.assertEqual((m["co_trich_dan"]["x"], m["khong_trich_dan"]["n"]), (1, 0))

    def test_link_seek_after_cited_reply_counts_for_m2(self):
        ev = [replied("C1", day=13, moc_trich_dan=["@5"]), seek(mm=8, by="link", frm=0, to=5)]
        t = count.build_turns(self.chats, ev)
        m = count.m2_link_use(t, count.seeks_by_hv(ev), minutes=10)
        self.assertEqual((m["x"], m["n"]), (1, 1))

    def test_follow_up_question_same_video_within_5_minutes(self):
        chats = [chat("C1", mm=0), chat("C2", mm=3), chat("C3", mm=4, video="Day02/d02-r1-v01.txt")]
        ev = [replied(c, mm=m) for c, m in (("C1", 0), ("C2", 3), ("C3", 4))]
        m = count.m5_follow_up(count.build_turns(chats, ev))
        self.assertEqual((m["x"], m["n"]), (1, 3))


class OtherMetricsTest(unittest.TestCase):
    def test_missing_context_true_over_rows_with_key(self):
        chats = [chat("C1"), chat("C2", hh=11), chat("C3", hh=12)]
        ev = [replied("C1", missing_context=True), replied("C2", hh=11, missing_context=False), replied("C3", hh=12)]
        m = count.m4_missing_context(count.build_turns(chats, ev))
        self.assertEqual((m["x"], m["n"]), (1, 2))

    def test_off_lesson_rubric_zero_among_graded_ta_questions(self):
        t = count.build_turns([chat("C1"), chat("C2", hh=11), chat("C3", hh=12, agent="classmate_clown")], [])
        answers = [{"nguon": "chat", "ref": "C1", "trang_thai_cham": "da_cham", "rubric_bam_bai": "0"},
                   {"nguon": "chat", "ref": "C2", "trang_thai_cham": "da_cham", "rubric_bam_bai": "2"},
                   {"nguon": "chat", "ref": "C3", "trang_thai_cham": "da_cham", "rubric_bam_bai": "0"},
                   {"nguon": "chat", "ref": "C1", "trang_thai_cham": "bo_qua", "rubric_bam_bai": ""}]
        m = count.m6_off_lesson(answers, t)
        self.assertEqual((m["x"], m["n"]), (1, 2))

    def test_latency_ignores_cached(self):
        chats = [chat("C1"), chat("C2", hh=11)]
        chats[1]["cached"] = "True"
        ev = [replied("C1", latency_ms=12000, cached=False), replied("C2", hh=11, latency_ms=5, cached=True)]
        m = count.m7_latency(count.build_turns(chats, ev))
        self.assertEqual((m["n"], m["median_ms"], m["over_10s"]["x"]), (1, 12000, 1))

    def test_sessions_split_on_gap_over_30_minutes(self):
        chats = [chat("C1", mm=0), chat("C2", mm=20), chat("C3", hh=11, mm=30), chat("C4", hv="L2")]
        v = count.volume(count.build_turns(chats, []))
        self.assertEqual(v["people"], 2)
        self.assertEqual(v["sessions_total"], 3)
        self.assertEqual(v["turns_per_person"]["max"], 3)


class ExamplesTest(unittest.TestCase):
    def test_examples_pick_earliest_row_of_each_kind(self):
        chats = [chat("C9", day=13, hh=9), chat("C2", day=13, hh=10), chat("C3", day=13, hh=11), chat("C4", day=12)]
        ev = [replied("C9", day=13, hh=9, moc_trich_dan=[], missing_context=False),
              replied("C2", day=13, hh=10, moc_trich_dan=[], missing_context=True),
              replied("C3", day=13, hh=11, moc_trich_dan=["Day01/d01-r1-v01.txt@40"], missing_context=False),
              replied("C4", day=12, missing_context=False),
              seek(day=13, hh=11, mm=2, by="link", frm=0, to=40)]
        t = count.build_turns(chats, ev)
        ex = {}
        for e in count.examples(t, count.seeks_by_hv(ev), []):
            ex.setdefault(e["kind"], e)  # ví dụ sớm nhất của mỗi kiểu
        self.assertEqual(ex["khong_trich_dan"]["chat_id"], "C9")
        self.assertEqual(ex["thieu_ngu_canh"]["chat_id"], "C2")
        self.assertEqual(ex["co_trich_dan_bam_link"]["chat_id"], "C3")
        self.assertEqual(ex["co_trich_dan_bam_link"]["moc"], ["Day01/d01-r1-v01.txt@40"])
        self.assertNotIn("hv", ex["khong_trich_dan"])  # không đưa mã học viên ra ví dụ

    def test_examples_limit_per_kind(self):
        chats = [chat("C%d" % i, day=13, hh=i) for i in range(1, 6)]
        ev = [replied("C%d" % i, day=13, hh=i, moc_trich_dan=[]) for i in range(1, 6)]
        ex = count.examples(count.build_turns(chats, ev), {}, [], per_kind=2)
        self.assertEqual([e["chat_id"] for e in ex if e["kind"] == "khong_trich_dan"], ["C1", "C2"])


class BreakdownTest(unittest.TestCase):
    def test_length_bucket_edges(self):
        self.assertEqual([count.length_bucket(n) for n in (None, 1, 20, 21, 60, 61, 150, 151)],
                         ["?", "1-20", "1-20", "21-60", "21-60", "61-150", "61-150", ">150"])

    def test_breakdown_by_day_and_length(self):
        chats = [chat("C1", video="Day01/d01-r1-v01.txt"), chat("C2", hh=11, video="Day01/d01-r1-v02.txt"),
                 chat("C3", hh=12, video="Day04/d04-r1-v01.txt")]
        for c, n in zip(chats, ("10", "30", "200")):
            c["do_dai_cau_hoi"] = n
        ev = [replied("C1", missing_context=True, moc_trich_dan=[]), replied("C2", hh=11, missing_context=False, moc_trich_dan=["@1"]),
              replied("C3", hh=12, missing_context=False)]
        b = count.breakdowns(count.build_turns(chats, ev))
        self.assertEqual(b["by_day"]["Day01"]["n"], 2)
        self.assertEqual(b["by_length"]["1-20"]["missing_context"]["text"], "1/1 (100.0%)")
        self.assertEqual(b["by_length"]["1-20"]["no_citation"]["text"], "1/1 (100.0%)")
        self.assertEqual(b["top_videos"][0], ("d01-r1-v01", 1))


class PersonaTest(unittest.TestCase):
    def test_personas_split_by_sessions(self):
        chats = [chat("A1", hv="L1"),                                              # L1: 1 phiên, 1 lượt
                 chat("B1", hv="L2"), chat("B2", hv="L2", hh=12), chat("B3", hv="L2", hh=12, mm=10),  # L2: 2 phiên
                 chat("D1", hv="L3", hh=8), chat("D2", hv="L3", hh=10), chat("D3", hv="L3", hh=12), chat("D4", hv="L3", hh=14)]  # L3: 4 phiên
        p = {x["name"]: x for x in count.personas(count.build_turns(chats, []), days=21)}
        self.assertEqual([p[k]["people"] for k in ("dung_it", "dung_vua", "dung_nhieu")], [1, 1, 1])
        self.assertAlmostEqual(p["dung_it"]["share"], 0.333, places=3)
        self.assertEqual(p["dung_vua"]["sessions_mean"], 2.0)
        self.assertEqual(p["dung_vua"]["uses_per_month"], 2.9)      # 2 × 30/21
        self.assertEqual(p["dung_vua"]["turns_per_session"], 2)     # 3 lượt / 2 phiên = 1.5 → làm tròn lên 2
        self.assertEqual(p["dung_nhieu"]["uses_per_month"], 5.7)


if __name__ == "__main__":
    unittest.main()

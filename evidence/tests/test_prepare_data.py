"""Test cho evidence/prepare_data.py — chạy: python -m unittest discover -s evidence/tests -v"""
import csv
import json
import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # thư mục evidence/
import prepare_data as pdp  # noqa: E402


class _TmpDir(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def write_raw(self, name, text):
        """Ghi file kiểu bản BTC: có BOM UTF-8 và xuống dòng CRLF."""
        path = os.path.join(self.tmp, name)
        with open(path, "wb") as f:
            f.write(text.replace("\n", "\r\n").encode("utf-8-sig"))
        return path

    def read_rows(self, path):
        with open(path, encoding="utf-8", newline="") as f:
            return list(csv.reader(f))


class NormalizeCsvTest(_TmpDir):
    def test_removes_bom_and_crlf(self):
        src = self.write_raw("learners.csv", "hv,created_date\nL0001,2026-11-05\n")
        dst = os.path.join(self.tmp, "out", "learners.csv")
        n = pdp.normalize_csv(src, dst)
        with open(dst, "rb") as f:
            raw = f.read()
        self.assertFalse(raw.startswith(b"\xef\xbb\xbf"))
        self.assertNotIn(b"\r", raw)
        self.assertEqual(n, 1)
        self.assertEqual(self.read_rows(dst)[0], ["hv", "created_date"])

    def test_trims_whitespace_around_cells(self):
        src = self.write_raw("event_types.csv", "type,khoa_trong_data\ntyping_started, field\n")
        dst = os.path.join(self.tmp, "out.csv")
        notes = []
        pdp.normalize_csv(src, dst, notes=notes)
        self.assertEqual(self.read_rows(dst)[1], ["typing_started", "field"])
        self.assertTrue(any("khoảng trắng" in n for n in notes))

    def test_keeps_quoted_json_cell_intact(self):
        src = self.write_raw("events.csv", 'hv,data\nL0001,"{""a"": 1, ""b"": ""x,y""}"\n')
        dst = os.path.join(self.tmp, "out.csv")
        pdp.normalize_csv(src, dst)
        self.assertEqual(json.loads(self.read_rows(dst)[1][1]), {"a": 1, "b": "x,y"})

    def test_fixes_old_answers_filename_in_event_types(self):
        src = self.write_raw("event_types.csv", "type,nghia\nanswer_submitted,ref_id trỏ tới tra_loi.csv. nguon là loại câu\n")
        dst = os.path.join(self.tmp, "out.csv")
        notes = []
        pdp.normalize_csv(src, dst, notes=notes)
        nghia = self.read_rows(dst)[1][1]
        self.assertIn("answers.csv", nghia)
        self.assertNotIn("tra_loi.csv", nghia)
        self.assertTrue(any("tra_loi.csv" in n for n in notes))

    def test_does_not_touch_same_text_in_other_files(self):
        src = self.write_raw("chat.csv", "id,note\nC1,tra_loi.csv\n")
        dst = os.path.join(self.tmp, "out.csv")
        pdp.normalize_csv(src, dst)
        self.assertEqual(self.read_rows(dst)[1][1], "tra_loi.csv")


class CountChecksTest(_TmpDir):
    def test_flags_row_count_mismatch(self):
        self.write_raw("learners.csv", "hv,created_date\nL0001,2026-11-05\nL0002,2026-11-05\n")
        res = pdp.check_row_counts(self.tmp, {"learners.csv": 3})
        self.assertEqual(res, [("learners.csv", 3, 2, False)])

    def test_row_count_match_is_ok(self):
        self.write_raw("learners.csv", "hv,created_date\nL0001,2026-11-05\n")
        self.assertEqual(pdp.check_row_counts(self.tmp, {"learners.csv": 1}), [("learners.csv", 1, 1, True)])

    def test_event_type_counts_compared_with_dictionary(self):
        self.write_raw("event_types.csv", "type,so_dong_trong_ban_nay\nlogged_in,2\napp_started,1\nsurvey_answered,0\n")
        self.write_raw("events.csv", "hv,type\nL1,logged_in\nL2,logged_in\n")
        self.write_raw("class_events.csv", "actor,type\nsystem,app_started\nsystem,app_started\n")
        res = {t: (exp, act, ok) for t, exp, act, ok in pdp.check_event_type_counts(self.tmp)}
        self.assertEqual(res["logged_in"], (2, 2, True))
        self.assertEqual(res["app_started"], (1, 2, False))
        self.assertEqual(res["survey_answered"], (0, 0, True))


class RunTest(_TmpDir):
    def test_refuses_when_output_would_overwrite_source(self):
        os.makedirs(os.path.join(self.tmp, "preclass"))
        with self.assertRaises(SystemExit):
            pdp.run(src=self.tmp, out=self.tmp)


if __name__ == "__main__":
    unittest.main()

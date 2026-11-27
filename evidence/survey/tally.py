"""Đếm kết quả khảo sát (evidence/survey/results.csv) — in x/n từng câu, tách 'tất cả' và 'dùng trợ giảng 30 ngày qua'.

Chạy: python evidence/survey/tally.py
Cách đếm: phiếu hợp lệ = câu 1 trả lời "Có" (đúng người dùng). Form không có logic bỏ câu nên phiếu "Không"
vẫn có câu trả lời sau; chỉ in ở cột "tất cả", không tính vào số chính.
"""
import csv
import os
from collections import Counter

PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results.csv")


def main():
    with open(PATH, encoding="utf-8-sig", newline="") as f:
        head, *rows = list(csv.reader(f))
    valid = [r for r in rows if r[1] == "Có"]
    print(f"Phiếu: {len(rows)} · hợp lệ (câu 1 = Có): {len(valid)}")
    for i in range(2, len(head)):
        print(f"\n{head[i]}")
        all_c, val_c = Counter(r[i] for r in rows), Counter(r[i] for r in valid)
        for k, _ in val_c.most_common() + [(k, 0) for k in all_c if k not in val_c]:
            print(f"  {val_c[k]}/{len(valid)} hợp lệ · {all_c[k]}/{len(rows)} tất cả | {k or '(trống)'}")


if __name__ == "__main__":
    main()

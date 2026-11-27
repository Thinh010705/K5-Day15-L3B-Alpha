"""Chuẩn hoá data BTC cấp về đúng chỗ, đúng định dạng — chạy một lần trước evidence/count.py.

Vì sao cần: bản data pack tải về (pre-class + training-ops) có
  - BOM UTF-8 ở đầu mọi file CSV và xuống dòng CRLF (kiểu Excel xuất) → đọc bằng open(..., "utf-8")
    thì tên cột đầu bị dính ký tự BOM (thành "<BOM>hv"), nối bảng theo cột hv bị hỏng;
  - khoảng trắng thừa đầu ô (cột khoa_trong_data của event_types.csv);
  - mô tả answer_submitted trong event_types.csv trỏ tới tên file cũ "tra_loi.csv" (bộ hiện tại là answers.csv);
  - và bị để ở thư mục lạ (vd data1/) — repo quy ước để nguyên file BTC ở data-btc/ (đã .gitignore, KHÔNG commit).

Script KHÔNG đổi giá trị dữ liệu: chỉ đổi mã hoá, xuống dòng, cắt khoảng trắng đầu/cuối ô và sửa đúng một
lỗi tên file trong từ điển. File khác CSV (README.md, .xlsx) được chép nguyên.
Sau khi ghi, script tự kiểm: số dòng từng file so với README của BTC, số dòng từng loại việc so với
event_types.csv, và in sha256 để nhóm so cùng một bản data.

Chạy (chỉ thư viện chuẩn):
  python evidence/prepare_data.py                    # đọc data-btc/raw/ → ghi data-btc/preclass/, data-btc/training-ops/
  python evidence/prepare_data.py --src data1        # bản tải về để ở chỗ khác
"""
import argparse
import csv
import hashlib
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_SRC = os.path.join(ROOT, "data-btc", "raw")
DEFAULT_OUT = os.path.join(ROOT, "data-btc")
PACKS = ("preclass", "training-ops")

# Số dòng (không tính tiêu đề) theo bảng "Các file" trong README.md của data pack pre-class (BTC).
EXPECTED_ROWS = {
    "learners.csv": 721,
    "events.csv": 107709,
    "class_events.csv": 849,
    "answers.csv": 3776,
    "chat.csv": 1260,
    "completed_items.csv": 2472,
    "rewards.csv": 228,
}

# Sửa chữ đã biết: (tên file, cột) → [(chữ cũ, chữ mới, lý do)].
KNOWN_FIXES = {
    ("event_types.csv", "nghia"): [
        ("tra_loi.csv", "answers.csv", "tên file cũ; ref_id của answer_submitted trỏ tới answers.csv (column_dictionary.csv)"),
    ],
}


def normalize_csv(src, dst, notes=None):
    """Đọc CSV (có/không BOM, CRLF/LF) → ghi UTF-8 không BOM, LF, ô đã cắt khoảng trắng. Trả số dòng dữ liệu."""
    notes = notes if notes is not None else []
    name = os.path.basename(src)
    with open(src, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.reader(f))
    if not rows:
        raise SystemExit("%s: file rỗng" % src)
    header = [h.strip() for h in rows[0]]
    fixes = {header.index(col): subs for (fname, col), subs in KNOWN_FIXES.items() if fname == name and col in header}
    trimmed = 0
    out = [header]
    for row in rows[1:]:
        cells = []
        for i, cell in enumerate(row):
            clean = cell.strip()
            trimmed += clean != cell
            for old, new, why in fixes.get(i, []):
                if old in clean:
                    clean = clean.replace(old, new)
                    notes.append("%s cột %s: đổi '%s' → '%s' (%s)" % (name, header[i], old, new, why))
            cells.append(clean)
        out.append(cells)
    if trimmed:
        notes.append("%s: cắt khoảng trắng đầu/cuối ở %d ô" % (name, trimmed))
    os.makedirs(os.path.dirname(os.path.abspath(dst)), exist_ok=True)
    with open(dst, "w", encoding="utf-8", newline="") as f:
        csv.writer(f, lineterminator="\n").writerows(out)
    return len(out) - 1


def _rows(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def check_row_counts(folder, expected=None):
    """[(file, số dòng mong đợi, số dòng thật, khớp?)] cho từng file trong expected."""
    expected = EXPECTED_ROWS if expected is None else expected
    res = []
    for name, exp in expected.items():
        path = os.path.join(folder, name)
        act = len(_rows(path)) if os.path.exists(path) else None
        res.append((name, exp, act, act == exp))
    return res


def check_event_type_counts(folder):
    """So số dòng mỗi type trong events.csv + class_events.csv với cột so_dong_trong_ban_nay của event_types.csv."""
    actual = {}
    for name in ("events.csv", "class_events.csv"):
        path = os.path.join(folder, name)
        if os.path.exists(path):
            for r in _rows(path):
                actual[r["type"]] = actual.get(r["type"], 0) + 1
    res = []
    for r in _rows(os.path.join(folder, "event_types.csv")):
        exp = int(r["so_dong_trong_ban_nay"])
        act = actual.get(r["type"], 0)
        res.append((r["type"], exp, act, exp == act))
    return res


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def run(src=DEFAULT_SRC, out=DEFAULT_OUT):
    src, out = os.path.abspath(src), os.path.abspath(out)
    packs = [p for p in PACKS if os.path.isdir(os.path.join(src, p))]
    if not packs:
        raise SystemExit("Không thấy %s trong %s — chép data pack BTC (preclass/, training-ops/) vào đó trước." % ("/".join(PACKS), src))
    if any(os.path.join(src, p) == os.path.join(out, p) for p in packs):
        raise SystemExit("--src và --out trùng nhau: sẽ ghi đè bản gốc. Để bản gốc ở data-btc/raw/.")
    notes, manifest = [], []
    for pack in packs:
        for name in sorted(os.listdir(os.path.join(src, pack))):
            s, d = os.path.join(src, pack, name), os.path.join(out, pack, name)
            if not os.path.isfile(s):
                continue
            if name.endswith(".csv"):
                n = normalize_csv(s, d, notes)
            else:
                os.makedirs(os.path.dirname(d), exist_ok=True)
                shutil.copy2(s, d)
                n = ""
            manifest.append((sha256(d), os.path.relpath(d, out), n))
    with open(os.path.join(out, "MANIFEST.txt"), "w", encoding="utf-8") as f:
        f.write("# sha256  file  số_dòng — sinh bởi evidence/prepare_data.py; nhóm so file này để chắc cùng một bản data\n")
        for h, rel, n in manifest:
            f.write("%s  %s  %s\n" % (h, rel, n))
    print("Đã ghi %d file vào %s" % (len(manifest), out))
    for n in notes:
        print("  sửa: " + n)
    ok = True
    pre = os.path.join(out, "preclass")
    if os.path.isdir(pre):
        print("Kiểm số dòng so với README BTC:")
        for name, exp, act, good in check_row_counts(pre):
            ok &= good
            print("  %s %-20s mong đợi %7s · thật %7s" % ("✓" if good else "✗", name, exp, act))
        bad = [r for r in check_event_type_counts(pre) if not r[3]]
        ok &= not bad
        print("Kiểm số dòng mỗi loại việc so với event_types.csv: %s" % ("khớp hết" if not bad else "%d loại lệch" % len(bad)))
        for t, exp, act, _ in bad:
            print("  ✗ %-28s mong đợi %6d · thật %6d" % (t, exp, act))
    print("MANIFEST: " + os.path.relpath(os.path.join(out, "MANIFEST.txt"), ROOT))
    return ok


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--src", default=DEFAULT_SRC, help="thư mục chứa preclass/ và training-ops/ bản BTC (mặc định data-btc/raw)")
    ap.add_argument("--out", default=DEFAULT_OUT, help="thư mục ghi bản đã chuẩn hoá (mặc định data-btc)")
    a = ap.parse_args(argv)
    return 0 if run(a.src, a.out) else 1


if __name__ == "__main__":
    sys.exit(main())

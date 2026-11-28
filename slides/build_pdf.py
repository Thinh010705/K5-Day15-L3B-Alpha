"""Dựng demo-slides.pdf từ slides/outline.md (mỗi mục "## N. Tiêu đề" là một trang).

Chạy: python slides/build_pdf.py
Cần Google Chrome hoặc Microsoft Edge (in PDF bằng chế độ headless). Ghi slides/demo-slides.html và demo-slides.pdf.
Sửa nội dung ở slides/outline.md rồi chạy lại; không sửa tay file HTML / PDF.
"""
import html
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTLINE = os.path.join(ROOT, "slides", "outline.md")
HTML_OUT = os.path.join(ROOT, "slides", "demo-slides.html")
PDF_OUT = os.path.join(ROOT, "demo-slides.pdf")
BROWSERS = ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
            "google-chrome", "chromium", "msedge"]

CSS = """
@page { size: 960pt 540pt; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: "Segoe UI", -apple-system, "Helvetica Neue", Arial, sans-serif; }
.slide { width: 960pt; height: 540pt; background: #0f2529; color: #eef4f3; position: relative;
         border-top: 6pt solid #5ee6c4; padding: 40pt 58pt 0; page-break-after: always; overflow: hidden; }
.kicker { color: #5ee6c4; font-size: 10.5pt; letter-spacing: 2.2pt; }
h1 { font-size: 30pt; font-weight: 700; margin-top: 12pt; }
.big { color: #5ee6c4; font-size: 40pt; font-weight: 700; margin-top: 4pt; line-height: 1.15; }
.sub { color: #c7d3d1; font-size: 13pt; margin-top: 2pt; }
ul { margin-top: 16pt; padding-left: 18pt; }
li { font-size: 13pt; line-height: 1.5; margin-bottom: 8pt; color: #e3ebe9; }
.foot { position: absolute; left: 58pt; right: 58pt; bottom: 26pt; border-top: 1pt solid #3a5257;
        padding-top: 8pt; font-size: 8.5pt; color: #9fb3b0; display: flex; justify-content: space-between; }
"""


def parse(text):
    slides = []
    for block in re.split(r"^## ", text, flags=re.M)[1:]:
        lines = block.strip().splitlines()
        m = re.match(r"(\d+)\.\s+(.*)", lines[0])
        if not m:
            continue
        s = {"title": m.group(2).strip(), "big": "", "sub": "", "bullets": [], "src": ""}
        for ln in lines[1:]:
            ln = ln.strip()
            b = re.match(r"\*\*(.+?)\*\*\s*·\s*(.*)", ln)
            if b and not s["big"]:
                s["big"], s["sub"] = b.group(1), b.group(2)
            elif ln.startswith("- "):
                s["bullets"].append(ln[2:])
            elif ln.startswith("Nguồn ·"):
                s["src"] = ln[len("Nguồn ·"):].strip()
        slides.append(s)
    return slides


def render(slides):
    e = html.escape
    pages = []
    for i, s in enumerate(slides, start=1):
        items = "".join("<li>%s</li>" % e(b) for b in s["bullets"])
        pages.append(
            '<section class="slide"><div class="kicker">LESSONLENS · ALPHA · AI20K K5</div>'
            "<h1>%s</h1><div class=\"big\">%s</div><div class=\"sub\">%s</div><ul>%s</ul>"
            '<div class="foot"><span>%s</span><span>%d / %d</span></div></section>'
            % (e(s["title"]), e(s["big"]), e(s["sub"]), items, e(s["src"]), i, len(slides)))
    return ('<!doctype html><html lang="vi"><head><meta charset="utf-8"><title>LessonLens · demo slides</title>'
            "<style>%s</style></head><body>%s</body></html>" % (CSS, "".join(pages)))


def main():
    with open(OUTLINE, encoding="utf-8") as f:
        slides = parse(f.read())
    if len(slides) != 8:
        sys.exit("outline.md cần đúng 8 trang (## 1. … ## 8.), đang có %d." % len(slides))
    with open(HTML_OUT, "w", encoding="utf-8") as f:
        f.write(render(slides))
    for b in BROWSERS:
        try:
            subprocess.run([b, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                            "--print-to-pdf=%s" % PDF_OUT, "file://" + HTML_OUT],
                           check=True, capture_output=True, timeout=120)
            print("Đã ghi %s (%d trang) bằng %s" % (os.path.relpath(PDF_OUT, ROOT), len(slides), os.path.basename(b)))
            return 0
        except (FileNotFoundError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
            continue
    sys.exit("Không tìm thấy Chrome / Edge để in PDF. Đã ghi %s — mở bằng trình duyệt rồi in ra PDF." % HTML_OUT)


if __name__ == "__main__":
    sys.exit(main())

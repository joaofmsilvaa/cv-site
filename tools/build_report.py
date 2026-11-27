"""Assemble report/report.md from report_body.md + knowledge files, then export the PDF.

Usage (from cv-site/): python tools/build_report.py
"""
import re
import pathlib
import pypandoc
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
REPORT = ROOT / "report"


def include(rel: str) -> str:
    """Inline a Markdown file: drop its own H1 title, push its headings 3 levels down."""
    text = (ROOT / rel).read_text(encoding="utf-8").strip()
    text = re.sub(r"\A# .*\n+", "", text)
    out, in_code = [], False
    for line in text.splitlines():
        if line.startswith("```"):
            in_code = not in_code
        if not in_code and re.match(r"#{1,3} ", line):
            line = "###" + line
        out.append(line)
    return "\n".join(out)


def raw(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8").strip()


body = (REPORT / "report_body.md").read_text(encoding="utf-8")
body = re.sub(r"\{\{include:([^}]+)\}\}", lambda m: include(m.group(1)), body)
body = re.sub(r"\{\{raw:([^}]+)\}\}", lambda m: raw(m.group(1)), body)
(REPORT / "report.md").write_text(body, encoding="utf-8")
print("report.md written")

common = ["--toc", "--toc-depth=2", f"--resource-path={REPORT}"]

css = """
body { font-family: 'Segoe UI', Arial, sans-serif; font-size: 10.5pt; line-height: 1.5; color: #0b1b3f; max-width: none; margin: 0; padding: 0; }
h1, h2, h3, h4 { color: #1f3fbf; line-height: 1.2; page-break-after: avoid; }
h1 { font-size: 20pt; border-bottom: 2px solid #1f3fbf; padding-bottom: 4pt; margin-top: 18pt; }
h1.title { font-size: 28pt; border: 0; margin-bottom: 0; }
p.subtitle { font-size: 13pt; color: #4a5675; margin-top: 4pt; }
h2 { font-size: 14pt; } h3, h4, h5, h6 { font-size: 11.5pt; }
table { border-collapse: collapse; width: 100%; margin: 8pt 0; font-size: 9.5pt; page-break-inside: auto; }
th, td { border: 1px solid #d7dcea; padding: 3pt 6pt; text-align: left; vertical-align: top; }
th { background: #dce4fa; }
tr { page-break-inside: avoid; }
pre, code { font-family: Consolas, monospace; font-size: 8.5pt; }
pre { background: #f6f7fb; border: 1px solid #d7dcea; padding: 6pt; white-space: pre-wrap; }
figure { margin: 10pt 0; page-break-inside: avoid; }
img { max-width: 100%; border: 1px solid #d7dcea; }
figcaption { font-size: 9pt; color: #4a5675; margin-top: 3pt; }
a { color: #1f3fbf; }
nav#TOC { page-break-after: always; }
"""
html_path = REPORT / "report.html"
pypandoc.convert_file(
    str(REPORT / "report.md"), "html5", outputfile=str(html_path),
    extra_args=common + ["--standalone", "--embed-resources", "--metadata", "lang=en",
                         "--css", str(REPORT / "_print.css")] if (REPORT / "_print.css").write_text(css) or True else [],
)
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page()
    pg.goto(html_path.as_uri(), wait_until="load")
    pg.pdf(path=str(REPORT / "report.pdf"), format="A4", print_background=True,
           margin={"top": "18mm", "bottom": "18mm", "left": "16mm", "right": "16mm"},
           display_header_footer=True, header_template="<span></span>",
           footer_template='<div style="font-size:8pt;width:100%;text-align:center;color:#4a5675"><span class="pageNumber"></span> / <span class="totalPages"></span></div>')
    b.close()
html_path.unlink()
(REPORT / "_print.css").unlink()
print("report.pdf written")

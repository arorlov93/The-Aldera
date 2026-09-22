#!/usr/bin/env python3
"""Render a one-page spec markdown file to print-ready HTML for Chromium."""
import re
import sys
import markdown

CSS = """
@page { size: A4; margin: 13mm 14mm 14mm 14mm; }
* { box-sizing: border-box; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body {
  font-family: %(font)s;
  font-size: 8.6pt;
  line-height: 1.34;
  color: #1c1c1a;
  margin: 0;
}
.masthead {
  display: flex; align-items: baseline; justify-content: space-between;
  border-bottom: 1.6pt solid #2d4739; padding-bottom: 5pt; margin-bottom: 10pt;
}
.brand { font-size: 13pt; letter-spacing: .22em; font-weight: 700; color: #2d4739; }
.masthead .kicker { font-size: 7.4pt; letter-spacing: .1em; color: #6b6b63; text-transform: uppercase; }
h1 { font-size: 12.5pt; margin: 0 0 8pt; color: #2d4739; font-weight: 700; }
h2 {
  font-size: 9.8pt; margin: 8pt 0 4pt; color: #2d4739;
  border-bottom: .6pt solid #c9cfc6; padding-bottom: 2.5pt; font-weight: 700;
}
h3 {
  font-size: 8.9pt; margin: 6pt 0 2.5pt; color: #1c1c1a; font-weight: 700;
  page-break-after: avoid;
}
p { margin: 0 0 4.5pt; }
ol, ul { margin: 0 0 5pt; padding-left: 15pt; }
li { margin-bottom: 2pt; }
hr { border: 0; border-top: .6pt solid #d9ddd4; margin: 6pt 0; }
table {
  width: 100%%; border-collapse: collapse; margin: 3pt 0 5pt;
  font-size: 8.1pt; page-break-inside: avoid;
}
th {
  background: #eef1ea; text-align: left; font-weight: 700; color: #2d4739;
  border: .6pt solid #b9c1b2; padding: 3pt 4.5pt;
}
td { border: .6pt solid #cfd5c9; padding: 3pt 4.5pt; vertical-align: top; }
table { table-layout: fixed; }
th:first-child, td:first-child { width: 26%%; }
th:nth-child(2), td:nth-child(2) { width: 37%%; }
strong { font-weight: 700; }
code { font-family: inherit; }
h2 + p, h3 + p { margin-top: 2pt; }
"""

HEAD = """<!DOCTYPE html>
<html lang="%(lang)s"><head><meta charset="utf-8">
<title>%(title)s</title><style>%(css)s</style></head><body>
<div class="masthead"><span class="brand">THE ALDERA</span><span class="kicker">%(kicker)s</span></div>
"""


def build(src, dst, font, lang, kicker):
    text = open(src, encoding="utf-8").read()
    title = re.match(r"#\s+(.+)", text).group(1).strip()
    # Drop the Russian working note between the H1 and the first horizontal rule.
    body_md = text.split("\n---\n", 1)[1]
    html = markdown.markdown(body_md, extensions=["tables", "sane_lists"])
    page = HEAD % {"lang": lang, "title": title, "css": CSS % {"font": font},
                   "kicker": kicker}
    page += "<h1>%s</h1>\n%s\n</body></html>" % (title, html)
    open(dst, "w", encoding="utf-8").write(page)
    print("wrote", dst)


if __name__ == "__main__":
    build(*sys.argv[1:6])

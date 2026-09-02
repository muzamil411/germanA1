#!/usr/bin/env python3
"""
German A1 — Complete Guide (Roman Urdu)
Build system: HTML fragments  ->  single HTML  ->  PDF (headless Chromium)

Content files live in content/ and are split into pages by markers:
    <!--PAGE ch="Chapter 1 - Alphabet" -->
Optional marker attributes:
    cls="cover"      extra CSS class on the page div
    nofoot="1"       hide the page footer (cover pages)
"""
import glob
import html
import os
import re
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(ROOT, "content")
BUILD = os.path.join(ROOT, "build")
OUT = os.path.join(ROOT, "output")
PDF_NAME = "German_A1_Complete_Guide_Roman_Urdu.pdf"

MARKER = re.compile(r'<!--\s*PAGE\s*(?P<attrs>[^>]*?)-->')
ATTR = re.compile(r'(\w+)\s*=\s*"([^"]*)"')

CHROME_CANDIDATES = [
    "/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
    "/opt/pw-browsers/chromium/chrome-linux/chrome",
    shutil.which("chromium") or "",
    shutil.which("google-chrome") or "",
]


def find_chrome():
    for c in CHROME_CANDIDATES:
        if c and os.path.exists(c):
            return c
    sys.exit("ERROR: no Chromium binary found")


def collect_pages():
    """Return list of (attrs_dict, html_body) in file order."""
    pages = []
    for path in sorted(glob.glob(os.path.join(CONTENT, "*.html"))):
        raw = open(path, encoding="utf-8").read()
        parts = MARKER.split(raw)
        # re.split with named group yields: [pre, attrs, body, attrs, body, ...]
        if parts[0].strip():
            sys.exit(f"ERROR: {os.path.basename(path)} has content before the first PAGE marker")
        for i in range(1, len(parts), 2):
            attrs = dict(ATTR.findall(parts[i]))
            body = parts[i + 1]
            attrs["_file"] = os.path.basename(path)
            pages.append((attrs, body))
    return pages


def render(pages):
    css = open(os.path.join(ROOT, "assets", "style.css"), encoding="utf-8").read()
    out = [
        "<!DOCTYPE html>",
        '<html lang="de"><head><meta charset="utf-8">',
        "<title>German A1 — Complete Guide (Roman Urdu)</title>",
        f"<style>\n{css}\n</style></head><body>",
    ]
    for n, (attrs, body) in enumerate(pages, start=1):
        cls = "page " + attrs.get("cls", "")
        out.append(f'<div class="{cls.strip()}" id="p{n}">')
        out.append('<div class="pg-body">')
        out.append(body.strip())
        out.append("</div>")
        if attrs.get("nofoot") != "1":
            ch = html.escape(attrs.get("ch", ""))
            out.append(
                '<div class="pg-foot">'
                f"<span>{ch}</span>"
                '<span>German A1 &middot; Roman Urdu Guide</span>'
                f'<span class="num">{n}</span>'
                "</div>"
            )
        out.append("</div>")
    # Overflow probe: runs before --dump-dom captures the DOM, so the build
    # can tell exactly which page has more content than fits on A4.
    out.append("""<script>
document.querySelectorAll('.page').forEach(function(pg){
  var b = pg.querySelector('.pg-body');
  if (b && b.scrollHeight > b.clientHeight + 2) {
    pg.setAttribute('data-overflow', pg.id + ':' + (b.scrollHeight - b.clientHeight));
  }
});
</script>""")
    out.append("</body></html>")
    return "\n".join(out)


def pdf_page_count(path):
    """Count pages in a PDF without external deps."""
    data = open(path, "rb").read()
    n = len(re.findall(rb"/Type\s*/Page[^s]", data))
    if n:
        return n
    counts = [int(m) for m in re.findall(rb"/Count\s+(\d+)", data)]
    return max(counts) if counts else -1


def main():
    os.makedirs(BUILD, exist_ok=True)
    os.makedirs(OUT, exist_ok=True)

    pages = collect_pages()
    if not pages:
        sys.exit("ERROR: no content pages found")

    html_path = os.path.join(BUILD, "book.html")
    with open(html_path, "w", encoding="utf-8") as fh:
        fh.write(render(pages))

    # Locate overflowing pages before printing.
    dom = subprocess.run(
        [find_chrome(), "--headless", "--disable-gpu", "--no-sandbox",
         "--virtual-time-budget=8000", "--dump-dom", "file://" + html_path],
        capture_output=True, text=True,
    ).stdout
    overflows = re.findall(r'data-overflow="(p\d+):(\d+)"', dom)
    if overflows:
        print("OVERFLOW - in dono pages par content zyada hai:")
        for pid, extra in overflows:
            idx = int(pid[1:])
            attrs = pages[idx - 1][0]
            print(f"   page {idx} ({attrs['_file']}, {attrs.get('ch','')}) : {extra}px extra")
    else:
        print("Overflow : none - har page ka content page ke andar hai.")

    pdf_path = os.path.join(OUT, PDF_NAME)
    subprocess.run(
        [
            find_chrome(),
            "--headless",
            "--disable-gpu",
            "--no-sandbox",
            "--no-pdf-header-footer",
            "--run-all-compositor-stages-before-draw",
            "--virtual-time-budget=10000",
            f"--print-to-pdf={pdf_path}",
            "file://" + html_path,
        ],
        check=True,
        capture_output=True,
    )

    expected = len(pages)
    actual = pdf_page_count(pdf_path)
    size = os.path.getsize(pdf_path) / 1024
    print(f"HTML   : {html_path}")
    print(f"PDF    : {pdf_path}  ({size:.0f} KB)")
    print(f"Pages  : expected {expected}  |  in PDF {actual}")
    if actual != expected:
        print("WARNING: page overflow - some page has more content than fits on A4.")
        # Report which files contribute, to help locate the overflow.
        by_file = {}
        for attrs, _ in pages:
            by_file[attrs["_file"]] = by_file.get(attrs["_file"], 0) + 1
        for f, c in by_file.items():
            print(f"   {f}: {c} page(s)")
        return 1
    print("OK: page count matches.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

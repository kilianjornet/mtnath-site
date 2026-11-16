#!/usr/bin/env python3
"""Prepare a new export of the Instructions (or Methods) page for the site.

    python3 tools/extract_images.py new-guide.html            -> instructions/index.html + instructions/img/
    python3 tools/extract_images.py new-methods.html --methods -> methods/index.html

Moves embedded base64 images into files, adds lazy loading, the site bar, favicon and sitebar.css.
"""
import base64, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = [("/", "Home"), ("/instructions/", "Instructions"), ("/methods/", "Methods"),
         ("/legal/", "Legal"), ("/contact/", "Contact")]
EXT = {"jpeg": "jpg", "jpg": "jpg", "png": "png", "webp": "webp", "gif": "gif", "svg+xml": "svg"}


def site_bar(current):
    links = "".join(
        f'<a href="{href}"' + (' aria-current="page"' if name == current else "") + f">{name}</a>"
        for href, name in PAGES)
    return ('<header class="sitebar"><div class="in"><a class="logo" href="/">MTNATH</a>'
            f'<nav aria-label="Site">{links}</nav>'
            '<a class="cta" href="https://app.mtnath.com">Open the app</a></div></header>\n')


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    src = Path(sys.argv[1])
    methods = "--methods" in sys.argv
    folder = ROOT / ("methods" if methods else "instructions")
    html = src.read_text(encoding="utf-8")

    if not methods:
        img_dir = folder / "img"
        img_dir.mkdir(parents=True, exist_ok=True)
        for old in img_dir.glob("fig-*"):
            old.unlink()
        count = 0

        def save(m):
            nonlocal count
            count += 1
            name = f"img/fig-{count:02d}.{EXT.get(m.group(1), 'bin')}"
            (folder / name).write_bytes(base64.b64decode(m.group(2)))
            return name

        html = re.sub(r"data:image/([a-z+]+);base64,([A-Za-z0-9+/=\s]+)", save, html)
        html = re.sub(r"<img (?!loading=)", '<img loading="lazy" ', html)
        html = html.replace("document.querySelectorAll('nav a')",
                            "document.querySelectorAll('.wrap > nav a')")
        print(f"{count} images saved to {img_dir}")

    if 'class="sitebar"' not in html:
        extra = ('<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">\n'
                 '<link rel="stylesheet" href="/assets/sitebar.css">\n')
        html = html.replace("</head>", extra + "</head>", 1)
        html = re.sub(r"<body([^>]*)>", lambda m: f"<body{m.group(1)}>\n" +
                      site_bar("Methods" if methods else "Instructions"), html, count=1)

    out = folder / "index.html"
    out.write_text(html, encoding="utf-8")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()

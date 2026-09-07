#!/usr/bin/env python3
"""The whole test suite: every page parses, every local link and asset resolves.

A static site's only real failure mode is a link or an image that points at
nothing, so that is what this checks, plus the handful of tags a page must not
ship without. It needs nothing installed.
"""

import html.parser
import pathlib
import sys
from urllib.parse import urlparse, unquote

ROOT = pathlib.Path(__file__).resolve().parent.parent
REQUIRED_TAGS = ("<title>", 'rel="stylesheet"', 'name="viewport"')

failures: list[str] = []


class Refs(html.parser.HTMLParser):
    """Collects href/src values and the alt text of every image."""

    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []
        self.images_without_alt = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        for key in ("href", "src"):
            if a.get(key):
                self.links.append(a[key])
        if tag == "img" and a.get("alt") is None:
            self.images_without_alt += 1


def check(page: pathlib.Path) -> None:
    rel = page.relative_to(ROOT)
    text = page.read_text(encoding="utf-8")

    for tag in REQUIRED_TAGS:
        if tag not in text:
            failures.append(f"{rel}: missing {tag}")

    parser = Refs()
    parser.feed(text)

    if parser.images_without_alt:
        failures.append(f"{rel}: {parser.images_without_alt} <img> without alt")

    for link in parser.links:
        target = urlparse(link)
        if target.scheme or target.netloc or link.startswith("#"):
            continue  # external, or an anchor on this page

        path = unquote(target.path)
        if not path:
            continue

        base = ROOT if path.startswith("/") else page.parent
        resolved = (base / path.lstrip("/")).resolve()

        if resolved.is_dir():
            resolved = resolved / "index.html"

        if not resolved.exists():
            failures.append(f"{rel}: broken link -> {link}")


for page in sorted(ROOT.rglob("*.html")):
    check(page)

if not (ROOT / "CNAME").exists():
    failures.append("CNAME is missing; GitHub Pages will drop the custom domain")

if failures:
    print("FAIL")
    for line in failures:
        print("  " + line)
    sys.exit(1)

count = len(list(ROOT.rglob("*.html")))
print(f"ok — {count} pages, all links and assets resolve")

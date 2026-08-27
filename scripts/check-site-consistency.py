#!/usr/bin/env python3
"""Consistency checks for this static site.

The site is plain HTML/CSS/JS with no build step, so nothing regenerates
`sitemap.xml`, `robots.txt` or `site.webmanifest` when `index.html` changes.
This script enforces that they stay in sync, and that every local asset and
in-page anchor actually resolves.

Run locally with:

    python3 scripts/check-site-consistency.py

Exits 0 when the site is consistent, 1 otherwise.
"""

from __future__ import annotations

import json
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parent.parent

# Meta tags whose `content` attribute holds a URL.
URL_META = {"og:image", "og:url", "twitter:image", "twitter:url"}

errors: list[str] = []
checks_run = 0


def fail(message: str) -> None:
    errors.append(message)


def ok(label: str) -> None:
    global checks_run
    checks_run += 1
    print(f"  ok  {label}")


class SiteParser(HTMLParser):
    """Collects element ids and referenced URLs from an HTML document."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: set[str] = set()
        # (url, tag) pairs, so error messages can point back at the element.
        self.refs: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = {k: (v or "") for k, v in attrs}

        if attr.get("id"):
            self.ids.add(attr["id"])

        # <meta content="..."> is only a URL for a known subset of meta tags.
        if tag == "meta":
            key = attr.get("property") or attr.get("name") or ""
            if key in URL_META and attr.get("content"):
                self.refs.append((attr["content"], "meta"))
            return

        # rel=preconnect/dns-prefetch point at origins, not documents.
        if tag == "link" and attr.get("rel", "") in {"preconnect", "dns-prefetch"}:
            return

        for name in ("href", "src"):
            value = attr.get(name, "").strip()
            if value:
                self.refs.append((value, tag))

        if tag in {"img", "source"} and attr.get("srcset"):
            for candidate in attr["srcset"].split(","):
                url = candidate.strip().split(" ")[0]
                if url:
                    self.refs.append((url, tag))


def is_external(url: str) -> bool:
    return url.startswith(("http://", "https://", "//", "mailto:", "tel:", "data:"))


def load_index() -> SiteParser:
    parser = SiteParser()
    parser.feed((ROOT / "index.html").read_text(encoding="utf-8"))
    return parser


def check_local_assets(page: SiteParser) -> None:
    """Every relative href/src in index.html must exist on disk."""
    missing = [
        f"<{tag}> references missing local file: {url}"
        for url, tag in page.refs
        if url
        and not is_external(url)
        and not url.startswith("#")
        and urlparse(url).path
        and not (ROOT / unquote(urlparse(url).path.lstrip("/"))).exists()
    ]
    if missing:
        for item in missing:
            fail(item)
    else:
        ok("all local assets referenced by index.html exist")


def check_anchors(page: SiteParser) -> None:
    """Every in-page #fragment link must resolve to a real element id."""
    broken = [
        f"<{tag}> links to #{url[1:]} but no element has that id"
        for url, tag in page.refs
        if url.startswith("#") and url != "#" and url[1:] not in page.ids
    ]
    if broken:
        for item in broken:
            fail(item)
    else:
        ok("all in-page anchors resolve to an existing element id")


def check_sitemap(page: SiteParser, domain: str) -> None:
    """sitemap.xml must be well-formed, on-domain, and point at real anchors."""
    try:
        tree = ET.parse(ROOT / "sitemap.xml")
    except ET.ParseError as exc:
        fail(f"sitemap.xml is not well-formed XML: {exc}")
        return

    namespace = "http://www.sitemaps.org/schemas/sitemap/0.9"
    locs = [el.text.strip() for el in tree.iter(f"{{{namespace}}}loc") if el.text]
    if not locs:
        fail("sitemap.xml contains no <loc> entries")
        return

    off_domain = [loc for loc in locs if urlparse(loc).netloc != domain]
    if off_domain:
        for loc in off_domain:
            fail(f"sitemap.xml <loc> does not match CNAME domain '{domain}': {loc}")
    else:
        ok(f"all {len(locs)} sitemap <loc> entries use the CNAME domain '{domain}'")

    dangling = [
        f"sitemap.xml lists #{urlparse(loc).fragment} but index.html has no such id"
        for loc in locs
        if urlparse(loc).fragment and urlparse(loc).fragment not in page.ids
    ]
    if dangling:
        for item in dangling:
            fail(item)
    else:
        ok("every sitemap fragment URL matches a section id in index.html")

    duplicates = sorted({loc for loc in locs if locs.count(loc) > 1})
    if duplicates:
        fail(f"sitemap.xml contains duplicate <loc> entries: {duplicates}")
    else:
        ok("sitemap.xml has no duplicate <loc> entries")


def check_robots(domain: str) -> None:
    """robots.txt must advertise the sitemap on the canonical domain."""
    robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
    match = re.search(r"(?im)^\s*Sitemap:\s*(\S+)\s*$", robots)
    if not match:
        fail("robots.txt does not declare a 'Sitemap:' line")
        return

    declared, expected = match.group(1), f"https://{domain}/sitemap.xml"
    if declared != expected:
        fail(f"robots.txt Sitemap is '{declared}' but CNAME implies '{expected}'")
    else:
        ok(f"robots.txt advertises the sitemap at {expected}")


def check_manifest(html: str) -> None:
    """site.webmanifest must be valid JSON, linked, and its icons must exist."""
    try:
        manifest = json.loads((ROOT / "site.webmanifest").read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"site.webmanifest is not valid JSON: {exc}")
        return
    ok("site.webmanifest is valid JSON")

    missing = [
        icon["src"]
        for icon in manifest.get("icons", [])
        if icon.get("src") and not (ROOT / icon["src"].lstrip("/")).exists()
    ]
    if missing:
        for src in missing:
            fail(f"site.webmanifest references missing icon: {src}")
    else:
        ok("all site.webmanifest icons exist on disk")

    if "site.webmanifest" in html:
        ok("index.html links to site.webmanifest")
    else:
        fail("index.html does not link to site.webmanifest")


def check_canonical(html: str, domain: str) -> None:
    """The canonical URL must agree with the CNAME domain."""
    match = re.search(r'<link[^>]+rel="canonical"[^>]+href="([^"]+)"', html)
    if not match:
        fail('index.html has no <link rel="canonical"> tag')
        return

    netloc = urlparse(match.group(1)).netloc
    if netloc != domain:
        fail(f"canonical URL host '{netloc}' does not match CNAME domain '{domain}'")
    else:
        ok(f"canonical URL matches the CNAME domain '{domain}'")


def main() -> int:
    domain = (ROOT / "CNAME").read_text(encoding="utf-8").strip()
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    print(f"Checking site consistency against CNAME domain: {domain}\n")

    page = load_index()
    check_local_assets(page)
    check_anchors(page)
    check_canonical(html, domain)
    check_sitemap(page, domain)
    check_robots(domain)
    check_manifest(html)

    print()
    if errors:
        print(f"FAILED - {len(errors)} problem(s) found:\n")
        for error in errors:
            print(f"  error  {error}")
        return 1

    print(f"PASSED - {checks_run} consistency checks succeeded.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

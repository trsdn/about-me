#!/usr/bin/env python3
"""Extract the release notes for a single version from CHANGELOG.md.

Used by the release workflow to turn a pushed tag into GitHub Release notes.

    python3 scripts/extract-release-notes.py 1.2.0

Exits non-zero when the version has no changelog section, so that tagging a
release that was never written up fails loudly instead of publishing an empty
release.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: extract-release-notes.py <version>", file=sys.stderr)
        return 2

    version = sys.argv[1].lstrip("v")
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")

    section = re.search(
        rf"^## \[{re.escape(version)}\][^\n]*\n(.*?)(?=^## |\Z)",
        changelog,
        re.MULTILINE | re.DOTALL,
    )
    if not section:
        print(
            f"error: CHANGELOG.md has no '## [{version}]' section. "
            "Add the release notes before tagging.",
            file=sys.stderr,
        )
        return 1

    # Strip the link reference definitions that trail the end of the file.
    body = "\n".join(
        line
        for line in section.group(1).strip().splitlines()
        if not re.match(r"^\[[^\]]+\]:\s", line)
    ).strip()

    if not body:
        print(
            f"error: the CHANGELOG.md section for {version} is empty.",
            file=sys.stderr,
        )
        return 1

    print(body)
    return 0


if __name__ == "__main__":
    sys.exit(main())

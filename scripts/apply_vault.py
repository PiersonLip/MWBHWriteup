#!/usr/bin/env python3
"""Apply Obsidian vault Markdown back onto index.html (prose/captions only)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from content_lib import (  # noqa: E402
    ARTICLE_RE,
    CHAPTERS_DIR,
    FLOW_PATHS_NOTE,
    INDEX,
    VAULT,
    apply_deep_notes,
    apply_flow_path_details,
    apply_hero_footer,
    parse_chapter_markdown,
    parse_flow_paths_markdown,
    parse_home_markdown,
    rebuild_article_inner,
)


def main() -> None:
    html = INDEX.read_text(encoding="utf-8")

    home = VAULT / "00 Home.md"
    if home.exists():
        hero, footer = parse_home_markdown(home.read_text(encoding="utf-8"))
        html = apply_hero_footer(html, hero, footer)
        print("Applied home/hero/footer")

    chapter_files = sorted(CHAPTERS_DIR.glob("*.md"))
    if not chapter_files:
        print("No chapter files in vault/chapters — run export_to_vault.py first", file=sys.stderr)
        sys.exit(1)

    by_id = {}
    for path in chapter_files:
        ch = parse_chapter_markdown(path.read_text(encoding="utf-8"))
        by_id[ch.id] = (path, ch)

    def repl(m: re.Match) -> str:
        cid = m.group(2)
        if cid not in by_id:
            print(f"skip {cid}: no vault file", file=sys.stderr)
            return m.group(0)
        path, ch = by_id[cid]
        try:
            new_inner = rebuild_article_inner(ch, m.group(4))
        except ValueError as e:
            print(f"ERROR {path.name}: {e}", file=sys.stderr)
            sys.exit(1)
        print(f"Applied {path.name} → #{cid}")
        return f"{m.group(1)}{cid}{m.group(3)}\n{new_inner}    {m.group(5)}"

    new_html, n = ARTICLE_RE.subn(repl, html)
    if n == 0:
        print("No articles found in index.html", file=sys.stderr)
        sys.exit(1)

    new_html = apply_deep_notes(new_html)
    print("Applied deep notes from glossary")

    if FLOW_PATHS_NOTE.exists():
        paths = parse_flow_paths_markdown(FLOW_PATHS_NOTE.read_text(encoding="utf-8"))
        new_html = apply_flow_path_details(new_html, paths)
        print(f"Applied flow path blurbs ({len(paths)} channels) from {FLOW_PATHS_NOTE.name}")
    else:
        print(f"skip flow paths: missing {FLOW_PATHS_NOTE}", file=sys.stderr)

    INDEX.write_text(new_html, encoding="utf-8")
    print(f"Wrote {INDEX}")


if __name__ == "__main__":
    main()

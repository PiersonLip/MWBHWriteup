#!/usr/bin/env python3
"""Export editable site content from index.html into the Obsidian vault."""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from content_lib import (  # noqa: E402
    ARTICLE_RE,
    CHAPTERS_DIR,
    INDEX,
    VAULT,
    chapter_to_markdown,
    hero_to_markdown,
    parse_article_html,
    parse_hero_footer_from_html,
)

ORDER = [
    "why",
    "how",
    "census",
    "kicks",
    "channels",
    "ce",
    "galaxy",
    "observe",
    "takeaways",
]


def main() -> None:
    html = INDEX.read_text(encoding="utf-8")
    CHAPTERS_DIR.mkdir(parents=True, exist_ok=True)

    hero, footer = parse_hero_footer_from_html(html)
    (VAULT / "00 Home.md").write_text(hero_to_markdown(hero, footer), encoding="utf-8")

    found = {}
    for m in ARTICLE_RE.finditer(html):
        cid = m.group(2)
        found[cid] = parse_article_html(m.group(4), cid)

    index_lines = [
        "# Content vault",
        "",
        "Edit these notes in Obsidian. When you're happy, run:",
        "",
        "```bash",
        "python3 scripts/apply_vault.py",
        "```",
        "",
        "To refresh the vault from the live site (overwrites vault text):",
        "",
        "```bash",
        "python3 scripts/export_to_vault.py",
        "```",
        "",
        "## Pages",
        "",
        "- [[00 Home]] — hero + footer",
        "",
        "## Chapters",
        "",
    ]

    tips = []
    for i, cid in enumerate(ORDER, start=1):
        if cid not in found:
            print(f"warning: missing chapter {cid}", file=sys.stderr)
            continue
        ch = found[cid]
        fname = f"{i:02d} {ch.id}.md"
        path = CHAPTERS_DIR / fname
        path.write_text(chapter_to_markdown(ch), encoding="utf-8")
        index_lines.append(f"- [[chapters/{fname[:-3]}|{ch.label} — {ch.title}]]")
        # collect tips for glossary
        for b in ch.blocks:
            blob = " ".join(b.paragraphs) + " " + b.text + " " + " ".join(x for pair in b.items for x in pair)
            for tm in re.finditer(r"\[([^\]]+)\]\{tip:\s*([^}]*)\}", blob):
                tips.append((tm.group(1), tm.group(2).strip()))

    (VAULT / "00 Index.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")

    # Glossary (unique by term)
    seen = {}
    for term, tip in tips:
        seen.setdefault(term, tip)
    gloss = ["# Glossary", "", "Hover tips used on the site. Edit carefully — re-export may reshuffle.", ""]
    for term in sorted(seen, key=str.lower):
        gloss.append(f"## {term}")
        gloss.append(seen[term])
        gloss.append("")
    (VAULT / "Glossary.md").write_text("\n".join(gloss), encoding="utf-8")

    workflow = Path(__file__).resolve().parents[1] / "vault" / "00 Workflow.md"
    if not workflow.exists():
        pass  # written separately

    print(f"Exported {len(found)} chapters → {CHAPTERS_DIR}")
    print(f"Home → {VAULT / '00 Home.md'}")


if __name__ == "__main__":
    main()

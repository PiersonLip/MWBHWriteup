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
    GLOSSARY_DIR,
    INDEX,
    VAULT,
    chapter_to_markdown,
    hero_to_markdown,
    load_glossary,
    parse_article_html,
    parse_hero_footer_from_html,
    write_glossary_note,
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
        # collect tips for glossary notes
        for b in ch.blocks:
            blob = " ".join(b.paragraphs) + " " + b.text + " " + " ".join(x for pair in b.items for x in pair)
            for tm in re.finditer(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]", blob):
                tips.append((tm.group(1).strip(), ""))  # wikilink; tip lives in note
            for tm in re.finditer(r"\[([^\]]+)\]\{tip:\s*([^}]*)\}", blob):
                tips.append((tm.group(1), tm.group(2).strip()))

    index_lines += ["", "## Glossary", "", "- [[Glossary]] — index of tip notes", ""]
    (VAULT / "00 Index.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")

    # Upsert glossary notes from any legacy inline tips found during export;
    # existing note bodies are preserved unless missing.
    load_glossary(force=True)
    existing = load_glossary()
    GLOSSARY_DIR.mkdir(parents=True, exist_ok=True)
    for term, tip in tips:
        key = term.lower()
        if key.startswith("glossary/"):
            continue
        if key in existing:
            continue
        if tip:
            write_glossary_note(term, tip)
    load_glossary(force=True)

    notes = sorted(GLOSSARY_DIR.glob("*.md"), key=lambda p: p.stem.lower())
    gloss_idx = [
        "# Glossary",
        "",
        "Each entry is a note in `Glossary/`. Link from chapters with `[[Term]]` or an alias like `[[XrB]]`.",
        "",
    ]
    for n in notes:
        gloss_idx.append(f"- [[{n.stem}]]")
    gloss_idx.append("")
    (VAULT / "Glossary.md").write_text("\n".join(gloss_idx), encoding="utf-8")

    print(f"Exported {len(found)} chapters → {CHAPTERS_DIR}")
    print(f"Home → {VAULT / '00 Home.md'}")
    print(f"Glossary notes → {GLOSSARY_DIR} ({len(notes)} notes)")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Split Glossary.md into vault/Glossary/*.md notes and rewrite chapter tips to [[wikilinks]]."""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from content_lib import (  # noqa: E402
    GLOSSARY_DIR,
    TIP_MD_RE,
    VAULT,
    load_glossary,
    tip_wikilink,
    write_glossary_note,
)


def parse_flat_glossary(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    out = {}
    parts = re.split(r"(?m)^(## .+)$", text)
    i = 1
    while i < len(parts):
        term = parts[i][3:].strip()
        body = parts[i + 1] if i + 1 < len(parts) else ""
        tip = re.sub(r"\s+", " ", body).strip()
        if tip:
            out[term] = tip
        i += 2
    return out


def main() -> None:
    flat = VAULT / "Glossary.md"
    if not flat.exists():
        print("No Glossary.md to migrate", file=sys.stderr)
        sys.exit(1)

    terms = parse_flat_glossary(flat)
    GLOSSARY_DIR.mkdir(parents=True, exist_ok=True)

    for term, tip in terms.items():
        path = write_glossary_note(term, tip)
        print(f"wrote {path.relative_to(VAULT)}")

    load_glossary(force=True)

    # Rewrite inline tips → wikilinks in chapters + home
    files = list((VAULT / "chapters").glob("*.md")) + [VAULT / "00 Home.md"]
    for path in files:
        raw = path.read_text(encoding="utf-8")

        def repl(m: re.Match) -> str:
            return tip_wikilink(m.group(1), m.group(2).strip())

        new = TIP_MD_RE.sub(repl, raw)
        if new != raw:
            path.write_text(new, encoding="utf-8")
            print(f"wikilinked tips in {path.name}")

    # Replace flat Glossary.md with an index/MOC
    notes = sorted(GLOSSARY_DIR.glob("*.md"), key=lambda p: p.stem.lower())
    lines = [
        "# Glossary",
        "",
        "Each entry is its own note under `Glossary/`. In chapters, link them as `[[Term]]` or a short alias like `[[XrB]]`.",
        "",
        "Hover text on the site comes from the note body (after the title).",
        "",
    ]
    for n in notes:
        lines.append(f"- [[{n.stem}]]")
    lines.append("")
    flat.write_text("\n".join(lines), encoding="utf-8")
    print(f"index → {flat}")


if __name__ == "__main__":
    main()

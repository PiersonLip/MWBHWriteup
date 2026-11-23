# Workflow — edit here, ship to the site

This folder is an **Obsidian vault** that mirrors the *writable* content of the site.

Interactive bits (canvases, sliders, JS) live only in `index.html`. You edit words, captions, callouts, timelines, and stats here.

Obsidian hotkeys, community plugins, themes, and snippets were copied from `~/notes/obsidianNotes`. Plugin `data.json` files are gitignored (machine-local / secrets).

## Day to day

1. Open this `vault/` folder as a vault in Obsidian.
2. Edit chapter notes under `chapters/`, plus [[00 Home]] for the hero/footer.
3. Glossary tips are real notes in `Glossary/`. In chapters, link them:

   `[[POSYDON]]` · `[[XrB]]` · `[[common envelope|common envelopes]]`

   The note body (under the title) is the hover text on the site. Short aliases like `XrB` / `CE` live in each note’s frontmatter.
4. When a chunk of writing feels right, from the project root:

```bash
python3 scripts/apply_vault.py
```

5. Preview the site (`python3 -m http.server 8765`), then commit/push if you're done.

## Pull site → vault (reset / resync)

If the HTML was edited directly and you want the vault chapters to match again:

```bash
python3 scripts/export_to_vault.py
```

**Warning:** export overwrites vault chapter text. Existing `Glossary/*.md` bodies are kept; new tip terms may get new notes.

## What syncs to the site

| Vault block | Site |
|-------------|------|
| `:::prose` | `.prose` paragraphs |
| `:::callout` | `.callout` |
| `:::timeline` | methods timeline cards |
| `:::stats` | census stat row |
| `:::eq` | equation line |
| `:::figure` cap/title/hint | figure caption, h3, hint only |
| `00 Home` hero/footer | header + footer |
| `[[Glossary note]]` | hover tip from that note’s body |

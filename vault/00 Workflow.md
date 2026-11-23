# Workflow — edit here, ship to the site

This folder is an **Obsidian vault** that mirrors the *writable* content of the site.

Interactive bits (canvases, sliders, JS) live only in `index.html`. You edit words, captions, callouts, timelines, and stats here.

## Day to day

1. Open this `vault/` folder as a vault in Obsidian.
2. Edit chapter notes under `chapters/`, plus [[00 Home]] for the hero/footer.
3. Tips use this syntax (keeps hover glossary on the site):

   `[Gaia]{tip: ESA's space observatory that measures precise positions of stars.}`

4. When a chunk of writing feels right, from the project root:

```bash
python3 scripts/apply_vault.py
```

5. Preview the site (`python3 -m http.server 8765`), then commit/push if you're done.

## Pull site → vault (reset / resync)

If the HTML was edited directly and you want the vault to match again:

```bash
python3 scripts/export_to_vault.py
```

**Warning:** export overwrites vault chapter text.

## What syncs

| Vault block | Site |
|-------------|------|
| `:::prose` | `.prose` paragraphs |
| `:::callout` | `.callout` |
| `:::timeline` | methods timeline cards |
| `:::stats` | census stat row |
| `:::eq` | equation line |
| `:::figure` cap/title/hint | figure caption, h3, hint only |
| `00 Home` hero/footer | header + footer |

## What does **not** sync from the vault

- Canvas / SVG / slider markup inside figures
- CSS, JS, galaxy physics, kick simulator
- TOC link list (kept automatically on the site)

Don't add or remove `:::figure` blocks — same count and order as the site.

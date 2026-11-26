# Binary stars deep note (`data-deep="binary-stars"`)

## Purpose

Rich glossary note for **binary stars** / **binary systems** — the **full explanation lives in a large hover tip**, with a Focus action that opens the orbit viz + same copy in a modal panel (fullscreen capable).

## Site wiring

- Glossary: `vault/Glossary/binary stars.md` — **source of truth** for the full deep-note prose (`deep: binary-stars`, `tip:` teaser, body with `{{orbit-viz}}` / `{{orion-viz}}`; applied by `apply_vault.py`)
- Tip markup: `.tip.tip-deep[data-deep="binary-stars"]` (via `apply_vault.py`)
- **Hover:** `.tip-bubble.tip-rich` clones `.deep-copy` with the live orbit viz inline after the “what binary means” definition paragraph (`.binary-orbit-tip-canvas`)
- **Focus:** maximize icon (top-right) opens `#deep-root` focus panel (not browser fullscreen); click/Enter on the tip term does the same
- Focus panel: `#deep-root` / `#deep-panel` / `#binary-orbit-canvas` (shared `drawBinaryOrbit` painter; panel has its own real fullscreen control)

## Viz

- Unequal-mass circular binary around a shared CM; primary (gold) + companion (blue); trail ticks
- Animates while a tip canvas exists and/or the deep panel is open; uses `vizColors()` stage background
- Shared animation clock (`deepState.anim`) paints every active orbit canvas

## Copy covers

- What a binary is (and multiples)
- How common they are; night-sky / massive-star binary fractions
- Why this paper’s BH story depends on binary evolution

Single source of truth for the prose: `.deep-copy` inside `#deep-root` (tip clones it on hover).

## Changelog

- 2026-11-24: Initial rich deep-dive + orbit canvas + glossary `deep:` support in `content_lib.py`.
- 2026-11-24: Full note in large hover tip (`.tip-rich`); Focus opens panel + viz.
- 2026-11-24: Orbit viz in the tip popup; Focus button → top-right fullscreen icon.
- 2026-11-24: Maximize icon opens focus panel again (not tip browser-fullscreen).
- 2026-11-24: Orbit viz sits after the definition paragraph (tip + focus panel).
- 2026-11-24: Focus panel floats viz left with text wrap; tighter square canvas.
- 2026-11-24: Orion map under the “binary-rich” paragraph in the focus panel (not tip); gold labels for known multiples.
- 2026-11-24: Canvas redraw from EarthSky Orion star layout (club, bow, short sword hook); Betelgeuse marked companion; no embedded image.
- 2026-11-24: Orion unlabeled; gold = multiple; hover tip shows name, binary status, short blurb.

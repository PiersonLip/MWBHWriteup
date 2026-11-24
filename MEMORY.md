# Project memory

Standalone browser explainer for arXiv:2610.07152 (Kiato, Lipschultz, Kalogera et al. — Galactic BHs with POSYDON).

## Deliverable

- Single self-contained file: `index.html` (HTML + CSS + canvas JS, no build step).
- Serve locally (e.g. `python3 -m http.server 8765`) and open `/` or `/#galaxy`.

## Site themes

Two themes via `data-theme` on `<html>` + CSS variables. Light = former slate; dark = former observatory.

| Theme | Feel |
|-------|------|
| `light` (default) | Cool gray paper, navy accent |
| `dark` | Charcoal night mode, soft gold accent |

- Picker in the hero (`#theme-picker`); choice persists in `localStorage.siteTheme`.
- Anti-FOUC snippet in `<head>` applies the saved theme before paint (migrates old `slate`/`parchment`/`cedar` → `light`, `observatory` → `dark`).
- Viz canvases/SVGs follow theme via `--viz-*` CSS vars + `vizColors()` / `refreshThemeVisuals()` (kick, flow, channels, CE, galaxy, microlensing).

## Content editing (Obsidian vault)

- Vault path: `vault/` (open that folder in Obsidian).
- Chapters: `vault/chapters/*.md`; hero/footer: `vault/00 Home.md`; how-to: `vault/00 Workflow.md`.
- Glossary tips are individual notes in `vault/Glossary/*.md` (index: `vault/Glossary.md`). Edit note body for hover text; link from chapters as `[[Term]]` or aliases (`[[XrB]]`, `[[CE]]`, …).
- `apply_vault.py` resolves those wikilinks into site `.tip` spans using the note body.
- Obsidian hotkeys/plugins/themes/snippets synced from `~/notes/obsidianNotes` (plugin `data.json` gitignored; `semantic-auto-linker` not committed — bundled API key).
- Nested tips: site builds a glossary from all `.tip[data-tip]` terms and linkifies matches inside open tip bubbles (hover MESA inside POSYDON).
- Footnotes: Obsidian `[^id]` / `^[inline]` in chapter markdown ↔ site `.fn-ref` + `.footnotes` section (round-trip via apply/export). Hover/focus on a superscript previews the note in the same tip bubble UI (text pulled from the chapter Notes list); click still jumps to the footnote.
- Figure blocks only sync **cap / title / hint** — do not add/remove `:::figure` blocks without updating vault + docs.
- Apply vault → site: `python3 scripts/apply_vault.py`
- Resync site → vault (overwrites `chapters/` + Home + regenerates Glossary): `python3 scripts/export_to_vault.py`
- Shared logic: `scripts/content_lib.py`

## Visualization docs (required)

- Index: [`visualizations/README.md`](visualizations/README.md)
- Per-figure notes: `visualizations/{flow,kick,wind,ce,galaxy,micro}.md`
- Cursor rule: `.cursor/rules/visualizations.mdc` — **read the matching doc before editing a viz; update it + this MEMORY when behavior changes.**

| Figure | Doc | Status |
|--------|-----|--------|
| Formation flowchart `#flow` | [flow.md](visualizations/flow.md) | Active |
| Natal kick orbit | [kick.md](visualizations/kick.md) | Active (+ Default reset) |
| M_ZAMS→M_BH `#wind` | [wind.md](visualizations/wind.md) | Hidden with §05 `#channels` |
| CE α toy | [ce.md](visualizations/ce.md) | Hidden with §06 `#ce` |
| Galactic seeding `#galaxy` | [galaxy.md](visualizations/galaxy.md) | Active |
| Microlensing `#micro` | [micro.md](visualizations/micro.md) | Active (3D+2D stacked) |
| BH lens gag (`data-effect="lens"`) | [lens.md](visualizations/lens.md) | Active (glossary easter egg) |
| Fiducial demographics `#demo` | — | **Removed** (flowchart replaces it) |

## Paper concepts covered

- Natal kicks / Blaauw mass loss / bound vs disrupted binaries (kick orbit interactive + Default button).
- Census: interactive formation-channel flowchart (`#flow`) only — demographics bar stack `#demo` removed.
- Observe: single-lens microlensing (`#micro`) — 3D Roman→lens→source (orbit/zoom/fullscreen) + 2D lens plane + light curve with Gaudi-style `A = (μ₊+μ₋)/source` fraction; Roman BH-BH prose follows.
- Channel demographics (~4e8 BHs; mostly isolated today).
- Wind-driven vs stable MT (~13 M☉ feature), CE efficiency.
- Galactic seeding (§II.3): POSYDON survivors → MW components → orbit integration → kick → present-day catalog hooks.

## Galaxy viz (`#galaxy`) — summary

See [visualizations/galaxy.md](visualizations/galaxy.md) for full detail.

- Examples Mild / Typical / Strong; drag camera; scroll zoom; maximize-icon fullscreen on `#gal-stage`.
- `KMS_MYR_TO_KPC = 0.001022712165`; flat Vc ≈ 220; idle spin after 5s or at 100%.

## Microlensing viz (`#micro`) — summary

See [visualizations/micro.md](visualizations/micro.md) for full detail.

- Stacked full-width: 3D above, 2D below; pitch 0…π/2; zoom 0.75–1.55; FS maximize icon.
- Labels: lensing black hole / source star / Roman; brightness·time axes; inset curve on 3D.
- Light-curve `A` fraction uses live mini major/minor limbs (shared Einstein scale with source disk).

## Hidden chapters (parked)

- `#channels` and `#ce` are `display: none`, labeled “Parked”, and omitted from the TOC. Visible chapters renumber 01–07 (galaxy→05, observe→06, takeaways→07). Vault files + HTML kept for a later return.

## BH lens gag — summary

See [visualizations/lens.md](visualizations/lens.md) for full detail.

- Nested tip **“weird things with light”** (`effect: lens` in glossary) inside the black-holes tip.
- Hover → instant tiny cursor BH + word ghosts; ~1.2s dwell → pinned focus; exit via hint click or Esc.
- UI chrome stays put; copy turns transparent and ghosts peel toward the cursor. BH eats overlapping words and grows from feeding after a natural size plateau.
- Photon ring near the outer horizon rim; scroll locked while active; eat-everything → “well that was awfully rude”.

## Writing / UX conventions

- Casual copy, no em dashes.
- Hover glossary tips via `.tip[data-tip]`. Rich tips use glossary frontmatter `deep: id` → `.tip-deep`: **large hover tip** with live orbit viz + full note; top-right maximize icon opens the focus panel (see `binary stars` / `visualizations/binary-stars.md`).
- Tip frontmatter `effect: lens` wires the BH lens gag (see [lens.md](visualizations/lens.md)); `image:` tips show a figure in the bubble (e.g. Crescent Nebula under Wolf-Rayet; XRB under X-ray binaries); `viz: gw` shows the pannable 3D GW mesh (LIGO / Gravitational-wave — [gw-tip.md](visualizations/gw-tip.md)); `viz: envelope` shows a stellar core+envelope cutaway ([envelope-tip.md](visualizations/envelope-tip.md)).
- Teaching-faithful schematics, not raw POSYDON dumps.
- Fullscreen controls use maximize / exit icons (not the word “Fullscreen”).

## Workflow (agent)

- When a chunk of work is clearly done: **commit** with a concise why-focused message, then **push** to `origin`.
- Keep this `MEMORY.md` **and** the relevant `visualizations/*.md` updated when behavior, controls, physics constants, or scope change.
- Do not commit `verify/` screenshots or secrets.

## Repo

- GitHub remote via `gh`; default branch `main`.
- Primary artifact to review: `index.html`.

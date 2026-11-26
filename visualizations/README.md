# Visualizations

Living docs for every interactive figure in `index.html`.

| Doc | Figure DOM id | Chapter |
|-----|----------------|---------|
| [flow.md](./flow.md) | `#flow` | Demographics |
| [kick.md](./kick.md) | kick canvas (kicks chapter) | Natal kicks |
| [wind.md](./wind.md) | `#wind` | Formation pathways (chapter hidden) |
| [ce.md](./ce.md) | CE figure | Common envelope (chapter hidden) |
| [galaxy.md](./galaxy.md) | `#gal-figure` / `#galaxy` | Galactic seeding |
| [micro.md](./micro.md) | `#micro` | Observational links |
| [lens.md](./lens.md) | `data-effect="lens"` (page overlay) | Glossary gag (“weird things with light”) |
| [tip-singularity.md](./tip-singularity.md) | 10-deep tip nest (page overlay) | Glossary gag (tip recursion) |
| [easter-eggs.md](./easter-eggs.md) | orbit / Sgr stare / super-dark / name confetti | Small gags |

## Agent rule

When changing a visualization:

1. Read the matching file here first.
2. Edit `index.html` (and vault caption/hint if needed).
3. Update that visualization’s `.md` with what changed.
4. Touch the summary in root `MEMORY.md` if controls, physics, or scope shifted.

Removed / parked: **Fiducial demographics** bar stack (`#demo`) — flowchart covers the same story.

Related: rich glossary deep-dive for **binary stars** — [binary-stars.md](./binary-stars.md) (`data-deep="binary-stars"`).

Related: BH lens easter egg — [lens.md](./lens.md) (`effect: lens` on glossary note **weird things with light**).

Related: tip-nest singularity — [tip-singularity.md](./tip-singularity.md) (10 nested tips → word-ghost swallow).

Related: small easter eggs — [easter-eggs.md](./easter-eggs.md) (orbital cursor, Sgr stare, super-dark veil, name confetti).

Related: tip canvases — [gw-tip.md](./gw-tip.md) (`viz: gw`), [envelope-tip.md](./envelope-tip.md) (`viz: envelope`), [common-envelope-tip.md](./common-envelope-tip.md) (`viz: common-envelope`), [mw-components-tip.md](./mw-components-tip.md) (`viz: mw-components`), [eccentricity-tip.md](./eccentricity-tip.md) (`viz: eccentricity`), [supernova-tip.md](./supernova-tip.md) (`viz: supernova`).

## Page themes

Site themes are `light` and `dark` (`data-theme` + CSS vars). See root `MEMORY.md`. Dark also recolors viz backgrounds/palettes through `--viz-*` and `vizColors()`; theme switches call `refreshThemeVisuals()`. After three theme toggles in a session, a one-shot **Super dark** picker option fades the page to black for 3s (not a persisted theme).

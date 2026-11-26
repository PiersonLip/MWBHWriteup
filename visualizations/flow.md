# Formation-channel flowchart (`#flow`)

## Purpose

Map how present-day Galactic BHs get to each demographic channel (mergers, disrupted, detached BH-BH, etc.) for the fiducial solar-Z POSYDON run.

## DOM / code

- Figure: `#flow` in census chapter
- SVG: `#flow-svg` (viewBox `980×560`)
- Detail panel: `#flow-detail`
- Data: `channels[]`, `flowPaths{}`, `renderFlow()`, `setActiveChannel()`
- Shared selection state: `active` channel id (also used to fill `#flow-detail`)

## Behavior

- Click a path or endpoint node → highlight that route (nodes + edges) and show channel % / blurb in `#flow-detail`.
- Non-highlighted trails stay visible but dimmed; colored endpoints keep their channel colors.
- Column labels and `%` on endpoints are real fractions of all present-day BHs from `channels[].pct`.
- Path changes animate in place (SVG is not rebuilt): edges fade/draw on, nodes get a light pop, detail panel fades up. Theme changes still rebuild fills. Honors `prefers-reduced-motion`.

## Sync notes

- Old `#demo` demographics stack was removed; do not reintroduce without updating this doc + MEMORY.
- Vault: `vault/chapters/03 census.md` figure block `id: flow` (cap/title/hint only).
- Path detail blurbs (`channels[].detail`): edit `vault/figures/flow-paths.md`, then `python3 scripts/apply_vault.py`.
- Column label under the third hub column is **Fate** (not “Binary fate”).

## Changelog

- 2026-11-23: `#demo` bar chart removed; flowchart is sole demographics interactive.
- 2026-11-24: Single-star path inserts **Supernova** between Born single and Initially single.
- 2026-11-24: Today endpoint boxes get a light/dark rim so borders read like the hub steps.
- 2026-11-26: Renamed column label to Fate; path blurbs editable via `vault/figures/flow-paths.md`.
- 2026-11-26: Path-selection transitions (edge draw, node pop, detail fade).

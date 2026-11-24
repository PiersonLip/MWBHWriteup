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

## Sync notes

- Old `#demo` demographics stack was removed; do not reintroduce without updating this doc + MEMORY.
- Vault: `vault/chapters/03 census.md` figure block `id: flow` (cap/title/hint only).

## Changelog

- 2026-11-23: `#demo` bar chart removed; flowchart is sole demographics interactive.
- 2026-11-24: Single-star path inserts **Supernova** between Born single and Initially single.

# M_ZAMS → M_BH by channel (`#wind`)

## Purpose

Show stable mass transfer vs wind-driven (non-interacting) pathways and the ~13 M☉ pile-up vs metallicity.

## DOM / code

- Figure: `#wind`
- SVG: `#channel-svg`
- Toggle: `#channel-toggle` (both / SMT / wind)
- Z slider: metallicity level → `zLevel` 0/1/2 (`0.01`, `0.1`, `1.0 Z☉`)
- Note: `#channel-note`
- Render: synthetic scatter via seeded RNG (`mulberry32`), not raw catalog points

## Behavior

- Points colored by channel; opacity drops for hidden channel.
- Note text updates with Z / mode to explain when the wind plateau washes out.

## Changelog

- (baseline) Fiducial teaching scatter for paper § channels.

# Eccentricity tip viz (`data-viz="eccentricity"`)

## Purpose

Side-by-side equal-mass binaries: **e = 0** (circle) vs **e = 0.5** (ellipse), stars orbiting a shared COM. Primary and secondary each get their own trajectory (gold / blue).

## Wiring

- Glossary: `vault/Glossary/eccentricity.md` (`viz: eccentricity`)
- Nested from §02 timeline “eccentricities”
- Tip system: `data-viz="eccentricity"` → `.tip-has-viz` / `.tip-ecc-viz` / `.ecc-tip-canvas`
- `paintEccentricityTip` / `ensureEccTipAnim`

## Changelog

- 2026-11-24: Initial dual-orbit eccentricity tip viz.

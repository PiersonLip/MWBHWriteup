# Natal kick: bound or disrupted?

## Purpose

Instantaneous post-SN 2-body schematic: pre-SN circular orbit → collapse + kick → bound ellipse or unbound escape.

## DOM / code

- Canvas: `#kick-canvas` (640×640)
- Presets: `#kick-presets` (`fiducial` / `fallback` / `zero`) — UI label **Kick handling**
- Sliders: `#vns`, `#mbh`, `#m2`, `#a`, `#theta`, `#dm`
- Reset: `#kick-default` → restores `kickDefaults`
- Status: `#kick-status`, `#kick-meta`
- State: `kickUI`, `kickDefaults`, `rebuildSim()`, draw loop phases `pre` / `flash` / `post`
- Fallback button wraps a glossary tip (`vault/Glossary/fallback.md`)

## Physics (schematic)

- Pre-SN circular relative orbit; SN at fixed true anomaly.
- Kick modes:
  - **Inverse mass (fiducial, default):** `v = v_NS × M_NS / M_BH`
  - **Fallback:** `(1 − f_fb) × v_NS` with `f_fb` from remnant mass
  - **Zero:** `0`
- Blaauw mass loss via `dm` + remnant mass; energy test → bound vs disrupted.
- Timeline: pre ≈2.4s → flash hold ≈1.2s → post → ~1.6s blend back to pre; full cycle ≈9.7s.

## Defaults (`kickDefaults`)

`mode: fiducial` (Inverse mass), `vns: 200`, `mbh: 8`, `m2: 10`, `a: 0.5`, `theta: 45`, `dm: 5`

## Changelog

- 2026-11-26: Renamed control to Kick handling; removed NS-like; Fallback tip; Inverse mass remains default.
- 2026-11-23: Added **Default** button to reset prescription + sliders.
- 2026-11-24: Pre-SN phase draws companion circular orbit as well as the primary’s.
- 2026-11-24: Pre/flash framed on pre-SN `a`; post phase zooms out so the new orbit fits.
- 2026-11-24: Star/BH marker size tracks view zoom for a sense of scale.
- 2026-11-24: Post-kick zoom eases in/out (~1.2s) instead of jumping.
- 2026-11-24: Loop restart blends post → pre (positions, guides, BH→progenitor).
- 2026-11-24: Post guides drawn from the body trail; bound paths use analytic Kepler (guides match stars).
- 2026-11-24: Phase clock is wall-time (kick on schedule); orbital motion rate still scales with zoom.

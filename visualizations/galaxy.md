# Galactic seeding orbit (`#galaxy` / `#gal-figure`)

## Purpose

Drop a binary into a MW-like potential: birth → pre-SN disk arc → SN+kick → separate BH + companion paths to “today.”

## DOM / code

- Stage: `#gal-stage` (fullscreen target)
- Canvas: `#gal-canvas`
- FS button: `#gal-fs` (maximize / exit icons)
- Kick strength: `#gal-examples` Mild / Typical / Strong (`GAL_EXAMPLES`) — label text “Kick strength”
- Progress: `#gal-progress`; play/pause/replay
- State: `gal` (yaw, pitch, zoom, progress, path, …)
- Draw: `drawGalaxy()`, `galProject()`, Verlet integrator

## Camera / UX

- Drag orbit (yaw/pitch); scroll/pinch zoom
- Look-at + `camDist` camera (`galProject`); home view looks at origin from ~28 kpc
- Default pitch ≈ 16° from edge-on (`π/2 − 16°`; pitch 0 = face-on, π/2 = edge-on)
- **Click** ω Cen / M13 / M22 or **GC** → animate zoom + orbit that target; empty-space click returns home
- GC focus draws schematic **Sgr A*** (small marker) + eccentric **S-stars** (exaggerated kpc-scale orbits)
- Fullscreen = stage only; icon button (not text label)
- Idle spin after 5s inactivity (home); while focused, continuous yaw orbit
- Shortcuts: `R` restart; `1`/`2`/`3` examples; `Space` play/pause only in fullscreen

## Physics notes

- `KMS_MYR_TO_KPC = 0.001022712165`
- Flat rotation ~220 km/s; vertical spring `nu2 ≈ 0.005`
- Easter eggs: ω Cen, M13, M22; **GC** → Sgr A* zoom

## Changelog

- FS control uses maximize icon (shared `.gal-fs-btn` styling with micro).
- 2026-11-23: Hovering GC shows “Galactic center” + “Sgr A*”.
- 2026-11-23: More gap between stage and controls; “Example system” → “Kick strength”.
- 2026-11-26: Click clusters/GC to zoom-orbit; GC focus shows Sgr A* + schematic S-stars.

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

- Drag orbit (yaw/pitch); scroll zoom ~0.72–1.55×
- Default pitch ≈ 16° from edge-on (`π/2 − 16°`; pitch 0 = face-on, π/2 = edge-on)
- Fullscreen = stage only; icon button (not text label)
- Idle spin after 5s inactivity, or immediately at 100% story
- Shortcuts: `R` restart; `1`/`2`/`3` examples; `Space` play/pause only in fullscreen

## Physics notes

- `KMS_MYR_TO_KPC = 0.001022712165`
- Flat rotation ~220 km/s; vertical spring `nu2 ≈ 0.005`
- Easter eggs: ω Cen, M13, M22 on hover; **GC** hover tip → “Galactic center” / “Sgr A*”

## Changelog

- FS control uses maximize icon (shared `.gal-fs-btn` styling with micro).
- 2026-11-23: Hovering GC shows “Galactic center” + “Sgr A*”.
- 2026-11-23: More gap between stage and controls; “Example system” → “Kick strength”.

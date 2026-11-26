# Single-lens microlensing (`#micro`)

## Purpose

Gaudi-style teaching schematic: how a dark lens (BH) brightens a background source; Roman as observer. Two synced panels — 3D geometry first, then lens-plane + light curve.

## DOM / code

- Figure: `#micro`
- Controls: `#micro-u0`, `#micro-spd`, `#micro-t` (time scrubber, full-width), `#micro-play`
- Status: `#micro-A` (whole `A ≈ …` is a tip; live value in `#micro-A-val`), `#micro-meta`
- 3D stage: `#micro-stage-3d` + `#micro-canvas-3d` + `#micro-fs`
- 2D: `#micro-canvas`
- State: `micro` (`u0`, `t`, `spd`, `yaw`, `pitch`, `zoom`, `trail`, …)
- Core: `microMag(u)`, `microLensMap`, `microImageShapes`, `microState`, `drawMicro`, `drawMicro3D`, `drawMicroCurveInset`

## Layout

- Controls on top (horizontal strip)
- Stacked full figure-width: **3D above**, 2D lens-plane + light curve below
- Reference GIF: `laymanPaperWriteup/.../Scott_Gaudi__single_lens_animation.gif`

## 3D panel

- Scene: Roman (observer) → lensing BH → source star on a spacetime grid with gravity well
- Camera: drag orbit; pitch `0` = edge-on, `π/2` = top-down; scroll zoom `0.75–1.55`
- Bent rays: midpoints from the point-lens image positions (track the source past the BH); edge-on boosts the image’s vertical offset so major/minor read above/below
- Fullscreen on `#micro-stage-3d`; maximize icon button
- Canvas resizes to stage (incl. fullscreen) via `clientWidth/Height` + DPR
- Inset light curve (bottom-right) mirrors the main brightness curve
- Roman icon (compact): dark hex aperture + silver barrel; **flat SASS** on barrel top; **single DAC** panel hinged open (not V-wings); spider + HGA

## 2D panel

- Canvas matches the stage box and device pixel ratio (same approach as the 3D panel)
- Einstein ring + true source + major (blue) / minor (red) mapped arcs (finite-source samples)
- Light curve: axes labeled **brightness** / **time**
- Gaudi-style visual fraction in light-curve corner:
  `A = (major + minor) / source`
  Numerator uses **live mini copies** of `limbPlus` / `limbMinus` at a shared Einstein px-scale (same scale as the yellow source disk), so glyph area tracks magnification as the event evolves.

## Labels

- “lensing black hole”, “source star”, “Roman”

## Changelog

- 2026-11-23: 3D-first stacked layout; orbit + zoom + fullscreen; larger grid; Roman redraw; brightness axis; Gaudi fraction in light-curve corner; maximize icon; inset curve on 3D.
- 2026-11-23: Roman scaled down; shield fixed to flat SASS + single hinged DAC (removed V-wings).
- 2026-11-23: Fraction glyphs are live image limbs (not fixed ellipses) so major/minor size updates with the event.
- 2026-11-24: Credit line under legend — “amazing diagram” links to Gaudi’s point-lens GIF.
- 2026-11-24: Space toggles play/pause while `#micro` is in view (or 3D fullscreen).
- 2026-11-24: Time scrubber (`#micro-t`, units of t_E); pauses play while dragging.
- 2026-11-24: 3D rays follow lens-map image positions so the major path doesn’t keep warping the wrong way after the source passes the BH.
- 2026-11-24: Side-on 3D view shows minor (red) below / major above when u₀>0; top-down follows image (x,y).
- 2026-11-23: Start farther out (`tmax` 5.2); minor image/ray fades in only as `|u|` drops; clock advances only while `#micro` is in view (resets to early single-path frame on enter).
- 2026-11-26: 2D canvas uses the stage size and device pixel ratio. While paused or off-screen the figure is not redrawn every frame (orbit drag and sliders still paint immediately).

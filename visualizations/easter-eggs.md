# Small easter eggs

Lightweight gags in `index.html` (not full chapter figures). Separate from the bigger [lens](./lens.md) and [tip-singularity](./tip-singularity.md) overlays.

## Orbital companion (`#orbit-companion`)

Hold ~600ms on the **period** / **periods** / **orbital period** tip. A tiny star dot orbits the cursor slowly (~44px radius, ~7s), drawn **under** tip bubbles (`z-index` 4500 vs tip-layer 5000). Skipped when `prefers-reduced-motion`.

## Sgr A* stare (galaxy HUD)

Stay in **GC focus** (Sgr A* zoom) with vignette settled (`gcVig > 0.95`, no focus anim) for **~9s**. HUD line **“still watching?”** fades in under the focus chrome, holds, then fades out. Resets on `exitGalFocus()`. See [galaxy.md](./galaxy.md).

## Super dark mode (`#theme-picker` / `#super-dark-veil`)

After **3 theme changes** (e.g. light → dark → light → dark), a **Super dark** button reveals in the picker. Clicking it does **not** persist a theme: the screen fades to black for **3s** (700ms fade; reduced-motion → short flash), then returns. Count is session-only.

## Pierson tip confetti (`#name-confetti`)

Each open of the byline tip (**Pierson** / **Pierson Lipschultz**, depth 0) pops **7** star particles outward from the name, then fades them in place. Skipped when `prefers-reduced-motion`.

## Changelog

- **2026-11-26** — Added orbital companion, Sgr A* stare, super-dark veil, name confetti.

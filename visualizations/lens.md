# Black-hole lens gag (`data-effect="lens"`)

Easter-egg spacetime lens on the nested glossary tip **“weird things with light”** (inside the **black holes** tip in §01). Not a chapter figure — page-level overlay effect in `index.html` (`initNestedTips`).

Glossary note: `vault/Glossary/weird things with light.md` (`effect: lens`).

## Trigger

| Action | Result |
|--------|--------|
| Hover `[data-effect="lens"]` | Effect starts **immediately** (tiny BH + word ghosts). |
| Hold hover **~1.2s** | Pins into **focused** mode (roam freely, exit hint). |
| Click exit hint / `Esc` | Soft exit; restores page. |
| Prefers-reduced-motion | Vignette only; no ghosts / BH / scroll lock. |

Click no longer pins — focus is dwell-only on the lens tip itself (not the parent tip bubble).

## DOM / CSS

| Id / class | Role |
|------------|------|
| `#bh-overlay` | Screen vignette, radial at `--bh-x` / `--bh-y`. |
| `#bh-core` | Cursor BH: soft outer falloff, event horizon (`::before`), photon ring (`::after` + rim shadow). |
| `#bh-ghost` | Ghost words/blocks from `.wrap` (z ~3150). |
| `#bh-ghost-ui` | Ghosts for the exit button label (z 5250, above hint chrome). |
| `#bh-lens-hint` | “Click to go back to normal” — solid panel; text transparent when lifted so ghosts show. |
| `#bh-lens-rude` | “well that was awfully rude” when every ghost item is eaten. |
| `html.is-lensing` | Cursor none (auto when pinned), scroll lock, tip-layer stacking. |
| `html.bh-lens-lifted` | Page copy → transparent; chrome (buttons etc.) stays; ghosts visible. |
| `html.bh-lens-pinned` | Focused mode; exit hint visible / clickable. |

Photon ring sits near the **outer** horizon rim (`::before` inset ~12%; spinning mask ~86–93% radial).

## Growth model

Size = **natural plateau** + **feed bonus** from eaten words.

1. **Kick** (`kickMs` ≈ 950ms): tiny → small, ease-in cubic.
2. **Ramp** (`rampMs` ≈ 16.2s): ease-out up to `pull = 1` → natural scale ≈ `naturalScale` (1.12).
3. **Plateau**: time-based growth **stops**.
4. **Feed**: each swallowed word bumps `feedTarget` by `perEat` (~0.022), smoothed into `feed` (cap `feedMax` ~2.4).

`bhScaleFromPull(pull)` → base from eased pull + live `feed`. Swallow radius tracks horizon (~0.88 × half of scaled 120px core).

## Word ghosts

- Built from text in `.wrap` (+ canvases/images as blocks) via `buildGhost()` / `appendGhostWordsFrom()`.
- On pin, `ghostifyExitHint()` clones the exit-button label into `#bh-ghost-ui`.
- Near-field pull toward cursor + light turbulence; far words stay put.
- BH overlapping a word → `eaten` (fade/scale into core); triggers feed + maybe rude popup.
- UI chrome (button boxes, toc pills, etc.) stays; only **text** lifts off (`color: transparent` under `.bh-lens-lifted`).

## Scroll / input

While lensing: `overflow: hidden` on html/body, non-passive `wheel` / `touchmove` preventDefault, restore scrollY on unlock.

## Key JS knobs (`lens` object in `initNestedTips`)

| Field | Meaning |
|-------|---------|
| `kickMs` / `rampMs` | Initial ease-in timing |
| `naturalScale` | Time-only size plateau |
| `perEat` / `feedMax` | Growth per eaten word / cap |
| `dwellTimer` (1200ms) | Hover duration before pin |

## Changelog

- **2026-11-24** — Word-ghost lens; pin + Esc/click exit; cursor BH with photon ring; natural grow then feed-on-eat; exit-button ghosts; rude popup; scroll lock; dwell-to-focus (not click); chrome stays / text lifts.

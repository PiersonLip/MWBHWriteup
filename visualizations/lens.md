# Black-hole lens gag (`data-effect="lens"`)

Easter-egg spacetime lens on the nested glossary tip **“weird things with light”** (inside the **black holes** tip in §01). Not a chapter figure — page-level overlay effect in `index.html` (`initNestedTips`).

Glossary note: `vault/Glossary/weird things with light.md` (`effect: lens`).

## Trigger

| Action | Result |
|--------|--------|
| Hover `[data-effect="lens"]` | Effect starts **immediately** (tiny BH + word ghosts). |
| Hold hover **~1.2s** | Pins into **focused** mode (roam freely, exit hint). |
| Click exit hint / `Esc` | Soft exit; restores page. Exit label stays solid (not edible). |
| Prefers-reduced-motion | Vignette only; no ghosts / BH / scroll lock. |

Click no longer pins — focus is dwell-only on the lens tip itself (not the parent tip bubble).

## DOM / CSS

| Id / class | Role |
|------------|------|
| `#bh-overlay` | Screen vignette, radial at `--bh-x` / `--bh-y`. |
| `#bh-core` | Cursor BH: soft outer falloff, event horizon (`::before`), photon ring (`::after` + rim shadow). |
| `#bh-ghost` | Ghost words/blocks from `.wrap` (z ~3150). |
| `#bh-ghost-ui` | Ghosts for the exit button label (z 5250, above hint chrome). |
| `#bh-lens-hint` | “Back to normal” — solid panel; text transparent when lifted so ghosts show. |
| `#bh-lens-rude` | Escalating taunts once every page ghost is eaten (edible stages). |
| `#bh-lens-chains` | Dashed restraints from the final center `:D` popup to the four corners. |
| `html.is-lensing` | Cursor none (incl. when pinned; exit hint keeps `cursor: pointer`), scroll lock, tip-layer stacking. |
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
- Soft global pull toward cursor (falloff with distance, never a hard near/far cutoff) + light turbulence.
- BH overlapping a word → `eaten` (fade/scale into core); triggers feed + maybe rude chain.
- When a rude stage’s text is fully eaten, the empty popup chrome slides off-screen, then the next stage slides in. Exit hint stays put.
- On soft exit, eaten ghosts ease back to home (opacity/scale/position, slight stagger) so page copy doesn’t pop in.
- UI chrome (button boxes, toc pills, etc.) stays; only **text** lifts off (`color: transparent` under `.bh-lens-lifted`).

## Rude chain

After every non-rude ghost is swallowed, `#bh-lens-rude` stages (each edible except the last):

1. “well that was awfully rude” — slides in from the top (center)
2. “C'mon...” — from the left (bottom-left)
3. “Hey I'm trying to talk to you” — from the right (top-right)
4. “:(” / “:((” / “:(((” — from bottom / top / left
5. “:D” **chained dead-center** — not edible; `#bh-lens-chains` ties it to the four corners

Panel chrome sits under `#bh-ghost-ui` so glyphs render on the box. Edible stages wait for the slide-in, then ghostify with a read grace (`eatAfter`) so the first taunt isn’t instantly swallowed.

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

- **2026-11-26** — Rude popup is edible; escalating chain ends with center `:D` chained to the corners.
- **2026-11-24** — Soft exit resurrects eaten ghosts (fade/scale home) instead of popping page text.
- **2026-11-24** — Word-ghost lens; pin + Esc/click exit; cursor BH with photon ring; natural grow then feed-on-eat; exit-button ghosts; rude popup; scroll lock; dwell-to-focus (not click); chrome stays / text lifts.

# Tip-nest singularity gag

Easter egg when glossary tips nest **5 deep** (depths `0…4`). Open tip bubbles slowly converge on their shared midpoint (staying visible); only then does a black hole form there. Page copy lifts into **word ghosts** and is pulled in hard. Once everything is swallowed, the BH shrinks to a vanishing point (no explode), a small twinkle blinks on the black field, then after **3s** the page fades back.

Lives in `initNestedTips` (`index.html`). Separate from the cursor BH lens gag ([lens.md](./lens.md)); exits lens first if active.

## Trigger

| Condition | Result |
|-----------|--------|
| `showTip` opens a bubble with `depth >= 4` | `triggerTipSingularity()` |
| Already mid-singularity (`singularity.busy`) | Tips ignored; `scheduleHide` / `clearFrom` blocked so tips don’t vanish |
| `prefers-reduced-motion` | Skip animation; black void → restore after 3s |

## Timeline (motion on)

1. **Gather** (~4.2s) — No BH. Tips ease to midpoint with a slight tilt, shrinking to a speck; cursor stays normal.
2. **Birth** (~2s) — Only once tips are tiny: BH forms at the midpoint and engulfs them.
3. **Pull** (~26s) — Strong but slower gravity: ghosts drift in; large swallow radius + feed growth. Shrink only after **all** items are eaten.
4. **Yank** (if needed, ~2.8s) — Final hard pull so leftovers finish falling in.
5. **Shrink** (~1.6s) — BH eases to a tiny point and fades (no flash / outward sparks).
6. **Void + twinkle** — Full black (cursor hides here); **0.85s** later a cartoon 4-point far-away “ding” twinkle; restore after `SING_VOID_MS` (3000).

## Knobs

| Constant | Meaning |
|----------|---------|
| `SING_TRIGGER_DEPTH` | `4` → 5th tip |
| `SING_GATHER_MS` / `SING_BIRTH_MS` | Tip converge (~4200) / BH birth |
| `SING_PULL_MS` / `SING_YANK_MS` | Main pull (~26000) / cleanup yank |
| `SING_SHRINK_MS` | Point collapse |
| `SING_VOID_MS` | Black hold (3000) |

## Changelog

- **2026-11-26** — Cursor until blackout; tips shrink to a speck before BH forms; cartoon star twinkle 0.5s after void.
- **2026-11-26** — 5 deep; stronger pull; tips no longer dismiss mid-gag; shrink-to-point + twinkle (no explode).
- **2026-11-26** — Tips gather to midpoint before BH; 3s void.
- **2026-11-26** — Word-ghost pull; earlier 4-deep / 6-deep variants.

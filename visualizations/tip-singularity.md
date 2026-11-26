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

1. **Gather** (~7.8s) — No BH. Tips ease to midpoint; stay opaque; tip-layer raised above overlay.
2. **Birth** (~2s) — BH grows at midpoint through the stacked tips.
3. **Pull** (~16s) — Strong gravity: ghosts travel nearly the full distance to the hole; large swallow radius + feed growth. Shrink only after **all** items are eaten.
4. **Yank** (if needed, ~2.8s) — Final hard pull so leftovers finish falling in.
5. **Shrink** (~1.6s) — BH eases to a tiny point and fades (no flash / outward sparks).
6. **Void + twinkle** — Black screen; soft twinkle at the point; restore after `SING_VOID_MS` (3000).

## Knobs

| Constant | Meaning |
|----------|---------|
| `SING_TRIGGER_DEPTH` | `4` → 5th tip |
| `SING_GATHER_MS` / `SING_BIRTH_MS` | Tip converge / BH birth |
| `SING_PULL_MS` / `SING_YANK_MS` | Main pull / cleanup yank |
| `SING_SHRINK_MS` | Point collapse |
| `SING_VOID_MS` | Black hold (3000) |

## Changelog

- **2026-11-26** — 5 deep; stronger pull; tips no longer dismiss mid-gag; shrink-to-point + twinkle (no explode).
- **2026-11-26** — Tips gather to midpoint before BH; 3s void.
- **2026-11-26** — Word-ghost pull; earlier 4-deep / 6-deep variants.

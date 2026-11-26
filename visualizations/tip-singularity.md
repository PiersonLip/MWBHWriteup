# Tip-nest singularity gag

Easter egg when glossary tips nest **4 deep** (depths `0…3`). Open tip bubbles slowly converge on their shared midpoint; only then does a black hole form there. Page + tip copy lifts into **word ghosts** and drifts into the hole. Finish: flash + sparkles, **3s** black void, page fades back.

Lives in `initNestedTips` (`index.html`). Separate from the cursor BH lens gag ([lens.md](./lens.md)); exits lens first if active.

## Trigger

| Condition | Result |
|-----------|--------|
| `showTip` opens a bubble with `depth >= 3` | `triggerTipSingularity()` |
| Already mid-singularity (`singularity.busy`) | Tips ignored |
| `prefers-reduced-motion` | Skip animation; black void → restore after 5s |

## Timeline (motion on)

1. **Gather** (~7.8s) — No BH yet. All open `.tip-bubble`s ease toward the average of their centers (`is-sing-gather`), gently shrinking.
2. **Birth** (~2s) — BH appears at that midpoint (`is-sing-form`); tip bubbles squeeze into the seed and fade.
3. **Pull** (~14s) — Word/block ghosts from `.wrap` (+ leftover tip media) lift (`is-sing-lifted`) and fall into the fixed BH (ease-in pull + feed-on-eat).
4. **Finish** (~2.2s) — Remaining glyphs yank in; BH collapses.
5. **Flash / sparkle / void / return** — same as before (3s void).

BH never follows the cursor; anchor is `--sing-px/py` from the tip midpoint.

## DOM / CSS

| Id / class | Role |
|------------|------|
| `#tip-singularity` | Fixed overlay root (`z-index` 12000). |
| `#tip-sing-ghost` | Word/block ghosts after birth. |
| `#tip-sing-bh` | BH at tip midpoint (hidden until birth). |
| `html.is-sing-gather` | Tip converge; BH still hidden. |
| `html.is-sing-form` | BH visible / growing. |
| `html.is-sing-lifted` | Page/tip copy transparent; ghosts move. |

## Knobs

| Constant | Meaning |
|----------|---------|
| `SING_TRIGGER_DEPTH` | `3` → 4th tip |
| `SING_GATHER_MS` | Tip converge (~7800) |
| `SING_BIRTH_MS` | BH form after gather (~2000) |
| `SING_PULL_MS` | Page ghost-pull (~14000) |
| `SING_FINISH_MS` | Final yank (~2200) |
| `SING_VOID_MS` | Black hold (3000) |

## Changelog

- **2026-11-26** — Tips gather to midpoint first; BH forms only after converge (not on cursor/tip).
- **2026-11-26** — Word-ghost pull, trigger at 4 deep, slower timing.
- **2026-11-26** — Initial CSS scale swallow at 6 deep.

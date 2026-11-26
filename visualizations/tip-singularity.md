# Tip-nest singularity gag

Easter egg when glossary tips nest **6 deep** (depths `0…5`). A black hole forms on the deepest tip, pulls the tip stack and the whole page into a point, vanishes with a flash + sparkles, holds on a black void for **5 seconds**, then the page fades back.

Lives in `initNestedTips` (`index.html`). Separate from the cursor BH lens gag ([lens.md](./lens.md)).

## Trigger

| Condition | Result |
|-----------|--------|
| `showTip` opens a bubble with `depth >= 5` | `triggerTipSingularity(bubble)` |
| Already mid-singularity (`singularity.busy`) | Tips ignored |
| `prefers-reduced-motion` | Skip pull/flash; black void → restore after 5s |

Depth is 0 for a page tip; each nest inside a `.tip-bubble` adds 1. Six open tips in a chain → boom.

## Timeline (motion on)

1. **Form** (~0.5s) — BH appears on the tip (`is-sing-form`).
2. **Pull** (~1.9s) — `.wrap` + `#tip-layer` spiral/scale into `--sing-x/y`; BH grows (`is-sing-pull`).
3. **Collapse** — BH shrinks to a point (`is-sing-collapse`); white flash + spark particles (`is-sing-flash`, `is-sing-spark`); tips cleared.
4. **Void** — full black (`is-sing-void`) for `SING_VOID_MS` (5000).
5. **Return** — void fades, page opacity restores (`is-sing-return` / `is-sing-return-show`); classes cleaned in `finishSingularity()`.

## DOM / CSS

| Id / class | Role |
|------------|------|
| `#tip-singularity` | Fixed overlay root (`z-index` 12000). |
| `#tip-sing-bh` | Stationary tip BH (photon ring + horizon). |
| `#tip-sing-sparks` | Sparkle dots flying outward at flash. |
| `#tip-sing-flash` | Full-screen white flash. |
| `#tip-sing-void` | Black hold screen. |
| `html.is-singularity` (+ phase classes) | Orchestrates transforms / visibility. |
| `--sing-x` / `--sing-y` | Transform origin (CSS px). |
| `--sing-px` / `--sing-py` | BH + spark anchor. |

## Knobs

| Constant | Meaning |
|----------|---------|
| `SING_TRIGGER_DEPTH` | `5` → 6th tip |
| `SING_VOID_MS` | Black-screen hold (5000) |

If the cursor lens gag is active, singularity calls `exitPinnedLens()` first.

## Changelog

- **2026-11-26** — Initial: 6-deep tip nest → BH swallow, flash/sparkle, 5s void, page restore.

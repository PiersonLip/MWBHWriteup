# Tip-nest singularity gag

Easter egg when glossary tips nest **4 deep** (depths `0…3`). A black hole forms on the deepest tip; page + tip copy lifts into **word ghosts** (same idea as the lens gag) and slowly drifts into the singularity. When leftovers finish collapsing: flash + sparkles, **5s** black void, then the page fades back.

Lives in `initNestedTips` (`index.html`). Separate from the cursor BH lens gag ([lens.md](./lens.md)); exits lens first if active.

## Trigger

| Condition | Result |
|-----------|--------|
| `showTip` opens a bubble with `depth >= 3` | `triggerTipSingularity(bubble)` |
| Already mid-singularity (`singularity.busy`) | Tips ignored |
| `prefers-reduced-motion` | Skip ghosts; black void → restore after 5s |

Depth is 0 for a page tip; each nest inside a `.tip-bubble` adds 1. Four open tips in a chain → boom.

## Timeline (motion on)

1. **Form + lift** (~2.2s) — BH appears on the tip; ghosts built from `.wrap` + `#tip-layer`; real text/media go transparent (`is-sing-form`, `is-sing-lifted`).
2. **Pull** (~14s) — RAF drifts ghosts toward the fixed singularity; near words fall in first; BH grows from pull + feed-on-eat (ease-in so it starts gentle).
3. **Finish** (~2.2s) — Remaining glyphs yank in; BH collapses (`is-sing-collapse`).
4. **Flash / sparkle** — white flash + outward sparks; tips cleared; ghosts destroyed.
5. **Void** — full black (`is-sing-void`) for `SING_VOID_MS` (5000).
6. **Return** — void fades, page opacity restores; `finishSingularity()` cleans classes.

## DOM / CSS

| Id / class | Role |
|------------|------|
| `#tip-singularity` | Fixed overlay root (`z-index` 12000). |
| `#tip-sing-ghost` | Word/block ghosts (reuses `.bh-ghost-word` / `.bh-ghost-block`). |
| `#tip-sing-bh` | Stationary tip BH (photon ring + horizon); scale driven in JS. |
| `#tip-sing-sparks` | Sparkle dots at flash. |
| `#tip-sing-flash` / `#tip-sing-void` | Flash + black hold. |
| `html.is-singularity.is-sing-lifted` | Page/tip copy → transparent; media opacity 0; ghosts visible. |
| `--sing-px` / `--sing-py` | BH + spark anchor. |

## Knobs

| Constant | Meaning |
|----------|---------|
| `SING_TRIGGER_DEPTH` | `3` → 4th tip |
| `SING_FORM_MS` | BH form / soft start (~2200) |
| `SING_PULL_MS` | Main ghost-pull duration (~14000) |
| `SING_FINISH_MS` | Final yank into the hole (~2200) |
| `SING_VOID_MS` | Black-screen hold (5000) |

Ghost builder shares `appendGhostWordsFrom(..., { items })` with the lens gag.

## Changelog

- **2026-11-26** — Word-ghost pull (lens-style), trigger at 4 deep, much slower form/pull/finish.
- **2026-11-26** — Initial: 6-deep tip nest → CSS scale swallow, flash/sparkle, 5s void.

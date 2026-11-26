# Common-envelope tip viz (`data-viz="common-envelope"`)

## Purpose

Tip-bubble schematic of a **common envelope**: two distinct stellar **cores** orbiting inside one shared hydrogen **envelope**, with labels. Soft glow + gentle core motion.

## Wiring

- Glossary: `vault/Glossary/common envelope.md` (`viz: common-envelope`)
- Tip system: `data-viz="common-envelope"` → `.tip-has-viz` / `.tip-ce-viz` / `.ce-tip-canvas`
- `paintCommonEnvelopeTip` / `ensureCeTipAnim`
- Nested [[envelope]] tip still uses `viz: envelope` (single-star cutaway)

## Changelog

- 2026-11-26: Initial two-core + shared envelope tip viz.

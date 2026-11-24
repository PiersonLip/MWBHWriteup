# Envelope tip viz (`data-viz="envelope"`)

## Purpose

Tip-bubble concentric star: dense **core** inside a larger hydrogen **envelope**, with labels. Soft glow pulse only.

## Wiring

- Glossary: `vault/Glossary/envelope.md` (`viz: envelope`)
- Nested from [[common envelope]] tip text via `tipViz`
- Tip system: `data-viz="envelope"` → `.tip-has-viz` / `.tip-env-viz` / `.env-tip-canvas`
- `paintEnvelopeTip` / `ensureEnvTipAnim`

## Changelog

- 2026-11-24: Initial core + envelope cutaway tip viz.

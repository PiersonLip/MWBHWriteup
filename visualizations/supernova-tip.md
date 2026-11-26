# Supernova tip viz (`data-viz="supernova"`)

## Purpose

Looping schematic of a **core-collapse supernova**: quiet massive star → brief collapse/flash → expanding ejecta shell with filaments → compact remnant glow. Caption cycles with the phase.

## Wiring

- Glossary: `vault/Glossary/supernova.md` (`viz: supernova`; aliases supernovae / SN)
- Tip system: `data-viz="supernova"` → `.tip-has-viz` / `.tip-sn-viz` / `.sn-tip-canvas`
- `paintSupernovaTip` / `ensureSnTipAnim` (~7.2s loop)

## Changelog

- 2026-11-26: Initial supernova tip viz.

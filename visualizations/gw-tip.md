# Gravitational-wave tip viz (`data-viz="gw"`)

## Purpose

Tip-bubble **3D spacetime mesh** (microlensing-style wire grid): twin BH wells + outgoing quadrupole strain; orbiting binary on the sheet. Drag to orbit, scroll to zoom, fullscreen (top-right).

## Wiring

- Glossary: `vault/Glossary/Gravitational-wave.md` (`viz: gw`) and `LIGO-Virgo-KAGRA.md` (`viz: gw`)
- Tip system: `tipViz` map + `data-viz="gw"` → `.tip-has-viz` / `.tip-gw-viz` / `.gw-tip-canvas` / `.tip-gw-fs`
- State: `gwTipState` (yaw / pitch / zoom / drag); `paintGwTip` / `bindGwTipCanvas` / `ensureGwTipAnim`

## Changelog

- 2026-11-24: Initial 2D tip viz; replaced with pannable 3D mesh + binary.
- 2026-11-24: Outgoing wave phase, larger mesh, slower inspiral, fullscreen button.

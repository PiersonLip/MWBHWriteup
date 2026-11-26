# Milky Way components tip viz (`data-viz="mw-components"`)

## Purpose

Tip-bubble edge-on schematic of the classic Galactic stellar structure: central **bulge**, thin **disk**, and sparse spherical **halo**, with labels. Soft halo pulse only.

## Wiring

- Glossary: `vault/Glossary/3 components of the Milky Way.md` (`viz: mw-components`)
- Nested from the galaxy-chapter footnote about POSYDON’s MW model vs the standard three components
- Tip system: `data-viz="mw-components"` → `.tip-has-viz` / `.tip-mw-viz` / `.mw-tip-canvas`
- `paintMwComponentsTip` / `ensureMwTipAnim`

## Changelog

- 2026-11-26: Initial bulge + disk + halo tip viz.

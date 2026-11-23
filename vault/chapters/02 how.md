---
id: how
label: "02 · Methods"
title: "Fancy binaries, simple Galaxy"
---

# Fancy binaries, simple Galaxy

*02 · Methods*

> Edit the blocks below. Interactive figure guts stay on the site; only captions / titles / hints sync.

:::prose
POSYDON evolves single stars and binaries from the [ZAMS]{tip: Zero-age main sequence. The initial common birth-state of a star, when it first begins hydrogen fusion in its core} using pre-computed MESA grids. The main ("fiducial") run throws **10 million binaries** at solar [metallicity]{tip: How metal-rich the gas is (where metals are everything heavier than helium). More metals means stronger stellar winds.}, then scales the results up to a Milky Way-ish galaxy (~6×10¹⁰ M☉ of stars, steady star formation for 10 Gyr). "Today" means: anything that still has a black hole in it at 10 Gyr.

Some stuff stays locked: a Kroupa-like [IMF]{tip: Initial mass function. How common stars of different birth masses are. Heavier stars are rarer.} for the primary stars, POSYDON's wind and mixing setup, and the usual α<sub>CE</sub>-λ<sub>CE</sub> [common envelope]{tip: A phase of binary star evolution where both stars share one giant envelope. The drag caused by the stars orbiting through this envelope greatly reduces their orbits, sometimes leading to mergers} recipe. Across twelve models, they flip the knobs that actually rearrange the BH census:
:::

:::timeline
- **Initial binaries**: Moe & Di Stefano (2017) period/mass-ratio/eccentricity correlations, versus a simpler Sana+12 + flat-q setup.
- **Core collapse**: Fryer delayed engine as the default, plus Sukhbold+16 and Patton+20 options that can still make low-mass BHs.
- **Natal kicks**: Disberg log-normal NS kicks, then scaled for BHs by mass, fallback, full NS-like, or zero. There's also a Hobbs Maxwellian version.
- **Common-envelope efficiency**: α<sub>CE</sub> = 1.0 (default), 0.5, and 0.1.
- **Metallicity**: Z☉, 0.1 Z☉, and 0.01 Z☉. Winds (and that ~13 M☉ bump) care a lot about this.
:::

:::prose
When they want to talk about observations, they drop the synthetic systems into a Milky Way model and integrate orbits with *gala*, updating velocities whenever a compact object is born. Full survey selection effects are left for later. This paper is about the intrinsic population, plus a first look at where that population sits in observable space.
:::

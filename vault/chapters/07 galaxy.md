---
id: galaxy
label: 05 · Galactic embedding
title: Embedding the black holes into our Milky Way
---

# Embedding the black holes into our Milky Way

*05 · Galactic embedding*

> Edit the blocks below. Interactive figure guts stay on the site; only captions / titles / hints sync.

:::prose
[[POSYDON]]'s simulations of binary evolution tell you what a system *is*. To actually talk about observations with [[Gaia]] or [[Roman]], we need to know *where* it is. To do that, we take the systems from POSYDON and embed them into a mock Milky Way[^1]. 

What we do is first draw a birth location and time in the Milky Way for the binary. Based on this location and time, we can get an estimate of what the metallicity should be. From this metallicity, we find a suitable match from the POSYDON simulation. After we have our binary, we then put it on a roughly circular orbit around our Milky Way and use [[gala]] to integrate the orbit. Then, whenever a [[compact object]] forms[^2] in our POSYDON simulation, the system's velocity gets updated for mass loss kick and the natal kick.
:::


:::timeline
- **Birth place & time**: Draw a random location and birth time in our model MW.
- **Metallicity from place**: Predict the local [[metallicity]] for that birth site and time.
- **Match a POSYDON binary**: Match a simulated binary whose evolution fits the metallicity.
- **Put it on a Galactic orbit**: Put the binary onto a roughly circular Milky Way orbit and integrate with [[gala]].
- **Kick when a compact object forms**: At [[core collapse]], update the velocity for mass loss and the [[natal kick]].
- **Bound or disrupted**: If the pair stays bound, keep integrating them together; if the kick unbinds them, follow each star on its own.
:::



:::callout
**For the visualization below:** birth in the disk → quiet evolution on a near-circular orbit → supernova kick unbinds the pair → BH is ejected → present-day positions. 
:::

:::figure
id: gal-figure
cap: Interactive · Schematic of paper §II.3
title: A disrupted binary's path through the Milky Way
hint: Phases: birth → pre-supernova → kick → BH and companion paths.
:::

[^1]: To model the Milky Way we split it into three components; these are different from the standard 3 components of the MW (bulge, disk, halo). Instead we model two types of disk (a high metallicity and low metallicity) and the bulge. We can largely exclude the halo, as while there *are* stars there, they form an incredibly small fraction of the whole population.

[^2]: Meaning one of the stars in the binary goes supernova.

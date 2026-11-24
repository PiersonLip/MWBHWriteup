---
id: galaxy
label: "05 · Galactic embedding"
title: "Drop the black holes into a real Galaxy"
---

# Drop the black holes into a real Galaxy

*05 · Galactic embedding*

> Edit the blocks below. Interactive figure guts stay on the site; only captions / titles / hints sync.

:::prose
[[POSYDON]]'s simulation of binary evolution tells you what a system *is*. To actually talk about [[Gaia]] or [[Roman]], we need to know *where* it is. To do that, we take the systems from POSYDON and put them into a Milky Way model with multiple parts that each have their rate of star-formation and metallicity[^1].

What we do is first draw a random birth location and time in the Milky Way for the binary. Based on this location and time, we can get an estimate of what the metallicity would be. From this metallicity, we find a suitable match from the POSYDON simulation. After we have our binary, we then put in on a roughly circular orbit around our Milky Way and use [[gala]] to integrate the orbit.
:::

:::timeline
- **Birth place & time**: Draw a random location and birth time in our model MW.
- **Metallicity from place**: Predict the local [[metallicity]] for that birth site and time.
- **Match a POSYDON binary**: Match a simulated binary whose evolution fits the metallicity.
- **Seat it on a Galactic orbit**: Put the binary onto a roughly circular Milky Way orbit and integrate with [[gala]].
- **Kick when a compact object forms**: At [[core collapse]], update the velocity for mass loss and the [[natal kick]].
- **Bound or disrupted**: If the pair stays bound, keep integrating them together; if the kick unbinds them, follow each star on its own.
:::

:::prose
Whenever a compact object forms in our POSYDON simulation[^2], the systems velocity gets updated both for the mass loss and the [[natal kick]]. If the binary stays bound, the pair keeps moving together. If the system is disrupted, we then treat each stars as its own thing.
:::

:::callout
**In the toy path below:** birth in the disk → quiet evolution on a near-circular orbit → supernova kick that unbinds the pair → BH and companion drift apart → present-day positions. Drag to rotate. Hit replay to watch it again.
:::

:::figure
id: gal-figure
cap: Interactive · Schematic of paper §II.3
title: A disrupted binary through the Milky Way
hint: Pick an example, then drag to orbit and scroll to zoom a bit. Phases: birth → pre-SN → kick → BH and companion paths.
:::

[^1]: To model the milky way we split it into three components, these are different then the standard 3 components of the MW (bulge, disk, halo). Instead we model two types of disk (a high metallicity and low metallicity) and the bulge. We can largely exlude the halo, as while there *are* stars there, they form an incredibly small fraction of the whole population

[^2]: i.e. one of the stars in the binary goes supernova

---
id: galaxy
label: "07 · Galactic embedding"
title: "Drop the black holes into a real Galaxy"
---

# Drop the black holes into a real Galaxy

*07 · Galactic embedding*

> Edit the blocks below. Interactive figure guts stay on the site; only captions / titles / hints sync.

:::prose
Binary evolution alone tells you what a system *is*. To talk about Gaia or Roman, you also need to know *where* it is. The paper takes POSYDON survivors and seeds them into a Milky Way model (low-α disk, high-α disk, central component), each with its own star-formation history and metallicity mix.

For every birth site they draw a formation time, position, and metallicity, then match it to the nearest POSYDON metallicity track. The system starts on a roughly circular orbit with a bit of random velocity scatter. From there, [[gala]] integrates the path forward in time.

Whenever POSYDON says a compact object forms, the Galactic velocity gets updated for mass loss and the [[natal kick]] (rotated from the binary frame into Galactocentric coordinates). If the binary stays bound, the pair keeps moving together. If it disrupts, the two pieces fly on their own from that moment on.
:::

:::callout
**In the toy path below:** birth in the disk → quiet evolution on a near-circular orbit → supernova kick that unbinds the pair → BH and companion drift apart → present-day positions. Drag to rotate. Hit replay to watch it again.
:::

:::figure
id: gal-figure
cap: Interactive · Schematic of paper §II.3
title: One disrupted binary through the Milky Way
hint: Pick an example, then drag to orbit (tilt for edge-on) and scroll to zoom a bit. Phases: birth → pre-SN → kick → BH and companion paths.
:::

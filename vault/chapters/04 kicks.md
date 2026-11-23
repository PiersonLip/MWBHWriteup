---
id: kicks
label: "04 · Natal kicks & disruption"
title: "A kick decides who stays together"
---

# A kick decides who stays together

*04 · Natal kicks & disruption*

> Edit the blocks below. Interactive figure guts stay on the site; only captions / titles / hints sync.

:::prose
When a star goes boom, two things mess with the orbit. Symmetric mass loss shifts the center of mass (the [Blaauw effect]{tip: Even without an asymmetric kick, dumping mass suddenly can unbind or widen a binary. Named after Adriaan Blaauw.}). Asymmetries can also give the remnant an extra [natal kick]{tip: An extra velocity shove a newborn neutron star or black hole can get from an asymmetric supernova.}. Add those up and you get the post-supernova orbital energy. If that energy is positive, the binary is done. Everyone flies free.

Neutron star kicks are somewhat pinned down by pulsar motions. The fiducial model draws from the Disberg et al. log-normal (peak around 150 to 200 km/s). Black hole kicks? Much mushier. The paper's default assumes the same kick *momentum* as for neutron stars, so heavier remnants get slower kicks:
:::

:::eq
*v<sub>BH</sub> = v<sub>NS</sub> · M<sub>NS</sub> / M<sub>BH</sub>* · [fallback]{tip: Material that falls back onto the newborn compact object. More fallback usually means a weaker kick in these models.}: *v<sub>kick</sub> = (1 − f<sub>fb</sub>) · v<sub>NS</sub>*
:::

:::prose
The extremes are useful bookends. Full NS-like kicks smash most binaries apart. Zero BH kicks keep almost everyone bound and let detached systems stretch out. Fallback-reduced kicks are kinder to massive direct-collapse remnants, which helps the ~13 M☉ wind feature show up among survivors.

Disruption is a big reason so many BHs are single, and why low-mass BHs are especially easy to unbind (they get the bigger kicks under inverse-mass scaling). Play with it below. Widen the orbit, crank the kick, or flip to NS-like kicks and watch the pair come undone.
:::

:::figure
id: kick-presets
cap: Interactive · Instantaneous post-SN 2-body orbit
title: Natal kick: bound or disrupted?
hint: The loop shows the pre-SN orbit, the collapse, then whatever happens after.
:::

---
id: why
label: "01 · Motivation"
title: "We're about to find a lot more black holes"
---
# We're about to find a whole lot more black holes

*01 · Motivation*

> Edit the blocks below. Interactive figure guts stay on the site; only captions / titles / hints sync.

:::prose
The Milky Way has **hundreds of millions** of stellar-mass[^1] [[black holes]][^census]. Yet almost none of them are visible. Until recently we were only aware of the bright ones sitting in [[X-ray binaries]] (a few dozen with solid mass measurements), plus the ones that are detected via [[Glossary/Gravitational-wave|gravitational waves]] by [[LIGO-Virgo-KAGRA|LIGO/Virgo/KAGRA]].

However, that is soon to change. So far [[Gaia]] has already confirmed three quiet black holes with bright companions and [[Roman]] should detect hundreds. [[Gaia DR4]] is expected to have dozens more measured BH binaries. Thus the question is quickly shifting from *"can we find them?"* to *"how did they get here?."*

And we can't answer that by just counting the corpses of stars. Most massive stars[^2] grow up intertwined with a partner in [[binary stars|binary systems]]. These relationships are tumultuous, with things like [[mass transfer]], [[common envelope]], mergers, and [[supernova]] kicks all deciding whether a black hole ends up alone or paired, massive or light, close-by or far away. A lot of simulation codes approximate these processes, however, we use [[POSYDON]] instead, which allows us to use incredibly accurate [[MESA]] simulations.
:::

:::callout
**The basic idea:** model the black holes that we would see today, trace them back to how they formed, vary the physics to see what works best, then predict Gaia and Roman might actually see.
:::

[^census]: Order-of-magnitude census estimates the amount stellar-mass black holes in the Milky Way to land around ~10⁸, we specifically find 4×10⁸ (or 400 million).

[^1]: Whenever I say "stellar" it simply means "star-like." Here it means black holes that have masses that are on the same scale/order of magnitude as stars

[^2]: largely considered as 8 or more times the mass of our sun


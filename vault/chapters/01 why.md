---
id: why
label: "01 · Motivation"
title: "We're about to find a lot more black holes"
---
# We're about to find a whole hell of a lot more black holes

*01 · Motivation*

> Edit the blocks below. Interactive figure guts stay on the site; only captions / titles / hints sync.

:::prose
The Milky Way should have **hundreds of millions** of stellar-mass black holes. Yet almost none of them are visible. Until recently we were only aware of bright ones sitting in [X-ray binaries]{tip: A binary where a black hole (or neutron star) steals gas from a companion. This in-falling gas heats up and shines in X-rays.} (a few dozen with solid mass measurements), plus whatever [LIGO/Virgo/KAGRA]{tip: Gravitational-wave detectors. They catch black hole mergers outside our Galaxy.} finds far away.

That's changing fast. [Gaia]{tip: ESA's space observatory that measures the precise positions and motions of stars. Great at finding quiet black holes tugging on a visible companion.} already confirmed three sleepy black holes with bright companions (Gaia BH1, BH2, BH3). [Roman]{tip: NASA's Nancy Grace Roman Space Telescope. Expected to find large quanties of black holes through gravitational microlensing.} should [microlens]{tip: When a massive object briefly bends and brightens light from a background star. The light curve can reveal the lens mass even if the lens is dark.} hundreds more. Gaia DR4 is expected to add dozens of astrometric BH binaries. So the fun question is shifting from "find me one cool system" to "what does the whole population look like?"

You can't answer that by just counting corpses. Most massive stars grow up with a roommate. Stuff like [mass transfer]{tip: One star dumps gas onto the other through the inner Lagrange point when it fills its Roche lobe.}, [common envelope]{tip: A phase of binary star evolution where both stars share one giant envelope. The drag caused by the stars orbiting through this envelope greatly reduces their orbits, sometimes leading to mergers}s, mergers, and supernova kicks decide whether a black hole ends up alone or paired, heavy or light, tight or wide. A lot of older population codes approximate that with fitting formulae. This paper uses [POSYDON]{tip: A binary population synthesis code built on detailed MESA stellar evolution grids.} instead, which leans on detailed [MESA]{tip: Modules for Experiments in Stellar Astrophysics. A highly accurate simulation code which simulates the evolution of single or binary stars.} binary grids.
:::

:::callout
**The basic idea:** take today's Galactic black holes, trace them back to how they formed, poke the uncertain physics to see what sticks, then ask (at a first-pass level) what Gaia and Roman might actually notice.
:::

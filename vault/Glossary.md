# Glossary

Hover tips used on the site. Edit carefully — re-export may reshuffle.

## Blaauw effect

Even without an asymmetric kick, dumping mass suddenly can unbind or widen a binary. Named after Adriaan Blaauw.

## common envelope

A messy phase where both stars share one giant envelope. The orbit usually shrinks a lot, or the stars merge.

### From layman writeup

<!-- source: laymanPaperWriteup/content · Common Envelope.md -->

## Common Envelope

A stage in [[Binary Stars|binary star evolution]] where where star engulfs its binary pair in its envelope. This is most common when one star evolves into the giant phase. Happens on the timescale of $\sim10^3$ yr

This process very commonly leads to in-spiraling and merger, as the orbital motion of one of the stars through the others leads to friction, shrinking the orbit. However, the energy dissipated into the shell from the loss of GPE can actually cause the ejection of said shell, created a low period system.

Very difficult to simulate due to the many magnitude range in both timescale and distance.

# Onset and Main Phases of CE Evo

Onset of CE is believed to be connected with *one of the following situations*
- runaway RLOF
- occurrence of Darwin instability
- Expansion of the [[accretor|accreting star]]

- [[mass transfer]] from a massive donor to a less massive causes an ***shrinking*** of the orbital period and the system, which would eventually lead to one star being engulfed by the other
- If the sum of spin angular moment is greater then a third of the total orbital angular momentum, ($|\vec{J_{1}}| + |\vec{J_{2}}| > 1/3 |\vec{L}|$), then there will be a violent shrinking of the orbit due to tidal forces.
- If the accretor cannot hold onto all of the in-falling material, it will swell up, fill its Roche lobe, and the system will become a contact binary

## Phases

- loss of co-rotation
- plunge-in
- slow (self-regulating) spiral-in
- envelope ejection

## Asides

- This can also happen if the star has a large enough planet orbiting around it, producing low-mass He WD

## Common Envelope ejection

- Whether not the envelope will be ejected is dependent on how good the system is at converting the GPE into KE, this added KE can then eject the envelope
- This can be described as the efficiency $\alpha_{CE}$ of converting orbital energy $\Delta E_{orb}$
 $$E_{bind} = \alpha_{CE}\Delta E_{orb}$$

- Ability to eject a CE depends heavily on the evolutionary status of the donor at the onset of CE
- Separation post CE ejection is about 100-1000x smaller than at onset
$$
E_{bind} \equiv -\frac{GM_{donor} M_{env}}{\lambda R_{donor}}
$$
- $\lambda$ various heavily on stellar mass and evolutionary status
- For low max systems the envelopes of the donors are typically ejected, as $|E_{bind}|$ is typically quite small
- Many [[HMXB]]s with NSs will not survive CE and hence DNS mergers are rare, although these do theoretically form Thorne-Zytkov objects

## core collapse

The endgame of a massive star: the iron core collapses and you get a neutron star, a black hole, or sometimes nothing.

## DCO

Double compact object: BH-BH, BH-NS, NS-NS, or similar pairs. If they are tight enough, gravitational waves can merge them.

### From layman writeup

<!-- source: laymanPaperWriteup/content · compact object.md -->

# compact object

white dwarfs, neutron stars or [[black hole|BHs]]

## Detached

Not transferring mass right now. The two objects orbit quietly without an accretion disk lighting up.

## fallback

Material that falls back onto the newborn compact object. More fallback usually means a weaker kick in these models.

## Gaia

ESA's space observatory that measures precise positions and motions of stars. Great for finding quiet black holes tugging on a visible companion.

### From layman writeup

<!-- source: laymanPaperWriteup/content · Gaia DR4.md -->

sorta a wacky one, this is a data release from the [Gaia mission](https://en.wikipedia.org/wiki/Gaia_(spacecraft)). It is a massive upcoming data release containing a ludicrous amount of data on various stars over time

## gala

A Python package for Galactic dynamics. The paper uses it to integrate orbits in a Milky Way potential.

## IMF

Initial mass function. How common stars of different birth masses are. Heavier stars are rarer.

## LIGO/Virgo/KAGRA

Gravitational-wave detectors. They catch black hole mergers outside our Galaxy.

### From layman writeup

<!-- source: laymanPaperWriteup/content · LIGO.md -->

# LIGO

Two arrays in two parts of the country used to detect [[GW|gravitational waves]]

<!-- source: laymanPaperWriteup/content · GW.md -->

# Gravitational Waves

- Ripples in spacetime created by relative acceleration of massive objects.

### Observational Properties in BBHs

- Using a GW obs one can obtain the spins and masses of merging BHs
- Spins have a magnitude (speed of rotation) and direction (axis of rotation)

## mass transfer

One star dumps gas onto the other through the inner Lagrange point when it fills its Roche lobe.

### From layman writeup

<!-- source: laymanPaperWriteup/content · mass transfer.md -->

# Mass Transfer

The process in [[Binary Stars|binary stars]] where mass is transferred between a [[donor]] and an [[accretor]]. This can happen through many processes, including [[RLO|Roche Lobe Overflow]], wind accretion, and contact binaries.

![[HMXB.jpg# normal]]

## Notes

- [[mass transfer]] through $L_1$ does not majority effect angular momentum, however, transfer through $L_2$ does, causing a shrinkage in separation, and typically mergers
- Different ways of modeling the transfer, depending on how you treat angular momentum with respect to the transfer
- Orbit widens if the [[donor]] is less massive then [[accretor]], and shrinks if the [[donor]] is more
- [[mass transfer]] onto NS and [[black hole|BH]] are limited by the [[Eddington Limit]]
- However, mass transferred off of the donor is at the rate of the evolution of its envelope
- mass transfer off of the donor is much greater (2 to 4 orders of magnitude) then the maximum accretion rate thus, the bulk of the mass will be blown away

## Stability Criteria

- Depends on the response of the star losing mass as well as the RL
- more likely to detect it if the mass transfer is stable
- orbit always expands for $q < 1$ and always shrinks when $q = 1.28$
- Depends on whether the donor contracts or swells upon starting to transfer mass
- Donors with radiative envelopes ([[Case A RLO]]) or slightly convective envelopes (early [[Case B RLO]]) will typically either shrink or stay the same radius

Unstable counterpart: [[runaway-RLOF|runaway RLOF]]

## MESA

Modules for Experiments in Stellar Astrophysics. The workhorse 1D stellar structure code behind POSYDON's grids.

## metallicity

How metal-rich the gas is (everything heavier than helium). Higher Z usually means stronger stellar winds.

## microlens

When a massive object briefly bends and brightens light from a background star. The light curve can reveal the lens mass even if the lens is dark.

### From layman writeup

<!-- source: laymanPaperWriteup/content · Microlensing.md -->

# Microlensing

A method used to find free-floating / [[Isolated Black Hole|isolated]] [[black hole|BHs]], namely ones that aren't shining in X-rays.

For isolated BHs, the important properties are basically
- Mass
- Spin
- Position
- Velocity

**Almost all isolated BHs form in higher order magnitude systems (i.e. binaries, tertiary, quads, etc etc)**

## How do we find free floating BHs?

### Microlensing!

- Around $\approx 1000 \text{yr}$
- Heavily dependent on [[natal-kick|natal kick]] velocity

Best to look towards regions where the star density is the highest, *but* where you can still resolve individual stars, namely the galactic bulge.
![[Scott_Gaudi__single_lens_animation.gif|1000]]
![[Gravitational_lens.gif# normal|1000]]

Green is the Einstein radius, as given by...
$$
\theta_{E} = \sqrt{ kM\pi_{rel} }
$$
Where M is the lens mass and pi is the relative distance between lens and source.

However, cant glean massive amount of info from said events, as you only get duration and magnitude of the light curve. So no mass info.
## [[Roman Space Telescope|Roman]]
---

See also: [[Gravitational Lensing]]

<!-- source: laymanPaperWriteup/content · Gravitational Lensing.md -->

# Gravitational Lensing

Warping of light due to the effects of gravity in accordance with [[GR]]. This is most prominent in very high mass regions, such as galaxy clusters.

Produces **MUCH** stronger signal then if the object wasn't being "lensed", hence allowing us to look farther and deeper into the universe.

For finding free-floating / isolated black holes specifically, see [[Microlensing]].

## natal kick

An extra velocity shove a newborn neutron star or black hole can get from an asymmetric supernova.

### From layman writeup

<!-- source: laymanPaperWriteup/content · natal-kick.md -->

# Natal Kick

A `kick` imparted on the object born from a SNe from the SN itself. This is due to asymmetric mass-loss, causing the star to be pushed in a direction.

## pair-instability gap

A predicted desert in BH masses where pair production blows stars apart before they can make a remnant in that range.

## POSYDON

A binary population synthesis code built on detailed MESA stellar evolution grids, not just quick analytic recipes.

### From layman writeup

<!-- source: laymanPaperWriteup/content · POSYDON Notes.md -->

# POSYDON
https://posydon.org/

The main binary population synthesis framework we use. It allows us to simulate millions of stars, binary and single, evolving over the course of billions of years, each with their own masses and [[metallicity|metallicities]].

This technique is incredibly useful as it allows us find differnet channels of evolution

For a more in depth explanation, see: [[POSYDON Paper|POSYDON instrument paper]]

<!-- source: laymanPaperWriteup/content · POSYDON Paper.md -->

# POSYDON: A General-Purpose Population Synthesis Code with Detailed Binary-Evolution Simulations

Fragos et al. 2023 · [DOI](https://doi.org/10.3847/1538-4365/ac90c1) · [posydon.org](https://posydon.org)

## Abstract

Most massive stars are members of a binary or a higher-order stellar systems, where the presence of a binary companion can decisively alter their evolution via binary interactions. Interacting binaries are also important astrophysical laboratories for the study of [[compact object]]. Binary population synthesis studies have been used extensively over the last two decades to interpret observations of compact-object binaries and to decipher the physical processes that lead to their formation. Here, we present [[POSYDON Notes|POSYDON]], a novel, publicly available, binary population synthesis code that incorporates full stellar-structure and binary-evolution modeling, using the MESA code, throughout the whole evolution of the binaries. The use of POSYDON enables the self-consistent treatment of physical processes in stellar and binary evolution, including: realistic mass-transfer calculations and assessment of stability, internal angular-momentum transport and tides, stellar core sizes, mass-transfer rates and orbital periods. This paper describes the detailed methodology and implementation of POSYDON, including the assumed physics of stellar- and binary-evolution, the extensive grids of detailed single- and binary-star models, the post-processing, classiﬁcation and interpolation methods we developed for use with the grids, and the treatment of evolutionary phases that are not based on pre-calculated grids. The ﬁrst version of POSYDON targets binaries with massive primary stars (potential progenitors of neutron stars or [[black hole]]) at solar metallicity.

## Roche-lobe overflow

When a star expands past the gravitational teardrop it can fill without dumping mass onto its companion.

### From layman writeup

<!-- source: laymanPaperWriteup/content · RLO.md -->

# Roche Lobe Overflow

The process of [[mass transfer]] in a binary system between a [[donor]] and [[accretor]] star. This is due to the [[donor]] star overflowing its roche lobe.

Types include
- Conservative Roche lobe overflow
- Case A RLO
- Case B RLO

<!-- source: laymanPaperWriteup/content · Case A RLO.md -->

# Case-A-RLO

[[RLO]] during donor hydrogen core burning (Meaning main-sequence)

<!-- source: laymanPaperWriteup/content · Case B RLO.md -->

# Case-B-RLO

This is [[RLO]] where the donor star is *post* hydrogen core burning. Ex. hydrogen *shell* burning

<!-- source: laymanPaperWriteup/content · runaway-RLOF.md -->

# runaway RLOF

Unstable [[RLO|RLO]] [[mass transfer]] which leads to eventual mergers

## Roman

NASA's Nancy Grace Roman Space Telescope. Expected to catch lots of black holes through gravitational microlensing.

### From layman writeup

<!-- source: laymanPaperWriteup/content · Roman Space Telescope.md -->

Roman space telescope, launched recently, pretty much a MUCH better hubble. See https://en.wikipedia.org/wiki/Nancy_Grace_Roman_Space_Telescope

## stable mass transfer

Mass transfer that stays under control instead of running away into a common envelope.

## Wolf-Rayet

Hot, helium-rich stars that have already lost their hydrogen envelopes. They drive fierce winds.

### From layman writeup

<!-- source: laymanPaperWriteup/content · WR-star.md -->

# WR star

Wolf-Rayet star.
A helium star of mass They are genally so massive (typically more than $∼25M_\odot$) that it sheds its hydrogen layer due to stellar [[winds]]. It may also shed its helium layer as well.

## X-ray binaries

A binary where a black hole (or neutron star) steals gas from a companion. The gas heats up and shines in X-rays.

### From layman writeup

<!-- source: laymanPaperWriteup/content · X-ray Binary.md -->

## X-ray binary

A type of [[Binary Stars|binary system]] where due to the process of [[mass transfer]] onto a [[compact object]] x-rays are producing, making the system bright in x-ray emission.  These systems are incredibly important for the detection of [[black hole|black holes]], as the energy release serves as a sort of beacon of where to look.

<!-- source: laymanPaperWriteup/content · HMXB.md -->

# HMXB

High mass [[X-ray Binary|x-ray binary]]. This means that the [[donor]] star is *more* massive then the [[accretor]].

<!-- source: laymanPaperWriteup/content · LMXB.md -->

## LMXB

A type of [[X-ray Binary]] where the [[donor|donor star]] is less massive then the [[accretor]], which is a [[compact object]].

## ZAMS

Zero-age main sequence: the starting line, when a star first settles into hydrogen burning.

### From layman writeup

<!-- source: laymanPaperWriteup/content · ZAMS.md -->

# ZAMS

Zero age main sequence
This is a star which is has literally just started on the main seqeunce. Hence `zero-age'

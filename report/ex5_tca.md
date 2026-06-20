# Exercise 5 — Temporal Concept Analysis (optional, 2 points)

This exercise is self-contained: it reads `data/wine_sample_200.csv` and
imports (does not modify) functions from `ex2_prepare_context.py`. Nothing
from Exercises 1-4 was changed.

## 1. Framing — and its honest limitation

The wine dataset has no real time dimension: no vintage, no repeated
measurement of the same wine. Per `CLAUDE.md`'s fallback plan, quality tier
(Low -> Medium -> High) is used as a **simulated time axis** — "stages of
development" — not real chronological time. This needs to be stated
plainly: no wine actually transitions between tiers; these are different
wines.

A sharper consequence, already proven in Exercise 4: Y is a strict object
partition (no wine belongs to more than one tier). So **no individual wine
can have a classical life track** — there is no persisting object to trace.
The adaptation made here: track **concepts** (attribute combinations)
across the tier sequence instead of individual wines, and define life-track
events — birth, death, refinement, split, merge, stability — for concepts.
This mirrors how Exercise 4 handled its own structural surprise (the
degenerate condition-implication family): name the limitation precisely,
then find the closest legitimate substitute rather than forcing the
original definition to apply where it doesn't.

## 2. Setup

The same three per-tier dyadic contexts from Exercise 4 are rebuilt here
independently (not sharing in-memory state, to keep this exercise
self-contained) — and their lattice sizes match exactly, a useful
cross-check: K_Low (8 wines, 43 concepts), K_Medium (165 wines, 4,781
concepts), K_High (27 wines, 599 concepts).

**Matching rule between consecutive stages**: concepts are matched by
*intent* (attribute combination) via set inclusion, restricted to **minimal
supersets** (the closest direct continuations, not every possible superset
— with Medium's lattice nearly 100x Low's size, "every superset" would
explode combinatorially and say nothing about real structure):

- **stable**: exactly one minimal superset, identical to the original
- **refined**: exactly one minimal superset, strictly larger (persists, gains attributes)
- **split**: 2+ minimal supersets (forks into multiple specific successors)
- **died**: zero supersets (no continuation at all)
- **born**: a next-stage concept with no subset at all in the previous stage

Only concepts with a real (nonempty) extent are used — every formal context
has a trivial "bottom" concept with intent = every attribute when its extent
is empty (a logical bookkeeping artifact, not a real combination), and that
would trivially match everything if included.

## 3. Validating the method before trusting the result

Both transitions came back with **zero splits**, which is exactly the kind
of result that should be double-checked rather than reported at face value.
The matching function was tested against two hand-built cases with known
answers: a genuine fork (`{a}` matching both `{a,b}` and `{a,c}`) correctly
returns both matches, and a chain (`{a}` matching `{a,b}` but not the larger
`{a,b,c}`) correctly returns only the minimal one. The logic is sound, so
**zero splits is a real structural property of this particular wine
context**, not a bug — every concept that survives into the next stage
refines along a single deterministic path rather than forking. This is
specific to this binary/ordinal-scaled context, not a general law of TCA.

## 4. Results

| Transition | Stable | Refined | Split | Died | Born |
|---|---|---|---|---|---|
| Low -> Medium | 23 | 13 | 0 | 6 | 3,666 |
| Medium -> High | 364 | 2,681 | 0 | 1,735 | 0 |

**Low -> Medium** is dominated by **birth**: Medium's lattice (4,780 real
concepts) is so much richer than Low's (42) that the overwhelming majority
of Medium combinations have no antecedent in Low at all — unsurprising
given Low has only 8 wines and very little combinatorial variety to begin
with. Of Low's 42 real concepts, more than half (23) carry over completely
unchanged, 13 persist with an added attribute, and 6 simply have no
continuation.

**Medium -> High** is dominated by **refinement and death**, with **zero
births** — every High-tier combination already existed in some form in
Medium (Medium's 4,780 concepts comfortably cover everything High's 598
need). 1,735 of Medium's combinations (36%) don't survive into High at all,
while 2,681 (56%) persist by gaining further attributes — consistent with
High being a narrower, more specific, more demanding profile than Medium.

## 5. Concrete life tracks

**A combination that dies going from Low to Medium**:
`{alcohol>=9, chlorides=high_salt, citric_acid_absent, density=heavy,
fixed_acidity>=low(6), pH>=basic(3.4), residual_sugar=off_dry,
sulphates>=low(0.4), volatile_acidity>=high(0.7), ...}` — note
`volatile_acidity>=high(0.7)`, a known wine-fault indicator. This exact
profile, present among the worst (Low) wines, has no continuation at all
once you move to Medium — chemically sensible: the specific fault pattern
that helps drag a wine down to Low doesn't reappear as a defining
combination among better wines.

**A combination that refines from Low to Medium**: a Low-stage profile
gains exactly one new attribute on its path into Medium — `alcohol>=11`.
This is the **fourth independent place in this project** alcohol's
quality-driving role has surfaced (after Exercise 1's decision tree,
Exercise 2's nested Quality x Alcohol relationship, and Exercise 4's
High-only stable intent) — here showing up as literally the attribute a
concept must *gain* to survive into a better quality stage.

**A combination that dies going from Medium to High**: a profile combining
`high_chlorides`, `density=heavy`, `pH=neutral_range`, and the full free/total
SO2 range — a "heavily processed, salty, sulfited" profile that simply
doesn't appear among the 27 High wines.

## 6. What this adds to the rest of the project

Exercise 4 already showed *which* concepts are stable vs. tier-specific as
a single three-way snapshot comparison. This exercise reframes the same
underlying lattices through a TCA lens — walking the sequence stage by stage
rather than comparing all three at once — and the directionality that adds
is the main payoff: **going toward better quality is mostly refinement and
death, not birth**. Nothing fundamentally new appears at the High tier; what
characterizes High is which Medium-stage combinations *survive* (by gaining
specific attributes like higher alcohol) and which simply don't make it.
That's a meaningfully different statement than "High has its own unique
concepts," and it's only visible by treating the tiers as an ordered
sequence rather than three unordered buckets.

## 7. Limitations

- The time axis is simulated (quality tier standing in for time), not real
  chronological data — stated upfront and not to be forgotten when reading
  the results above.
- Life tracks here are at the **concept level**, not the **object level**,
  because no wine persists across tiers (proven in Exercise 4). This is a
  deliberate, documented substitution, not the textbook definition of a TCA
  life track.
- The "zero splits" finding and the asymmetry between the two transitions
  are partly artifacts of the very different lattice sizes per tier (43 vs.
  4,781 vs. 599 concepts, driven by the very different sample sizes: 8 vs.
  165 vs. 27 wines) rather than a clean chemistry signal alone — this is
  flagged rather than overclaimed as a discovery about wine chemistry.

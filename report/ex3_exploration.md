# Exercise 3 — Attribute Exploration

Redefined per the actual assignment text: choose a comfortable domain,
perform attribute exploration, collect expert knowledge, explain results and
what was learned. Kept the wine domain for continuity with Exercises 1, 2
and 4, rather than switching to something unrelated.

## 1. Setup

**Attributes (12)**: single-threshold booleans derived from the same
physicochemical columns as Exercise 2, but deliberately collapsed to one
yes/no flag per attribute instead of the multi-level ordinal scales — using
independent attributes here avoids the canonical base being dominated by
trivial same-attribute chains (`alcohol>=13 -> alcohol>=11`), which Exercise
2 already covered as scale artifacts. See `notebooks/ex3_attribute_exploration.ipynb`
§1 for the exact thresholds (e.g. `high_alcohol` = alcohol >= 11%,
`good_quality` = quality >= 7).

**Expert oracle**: rather than relying on my own claimed domain knowledge
(as the programming-languages version of this exercise would have required),
the "expert" answering each proposed implication is the **full 1,599-row
real dataset**. Every confirm/refute decision is a real lookup against
actual lab measurements, and every counterexample produced is a real wine.
This is a stronger form of "collecting relevant knowledge from experts in
the field" than subjective judgment calls — there's no ambiguity about
whether wine #142 really has those measured values.

**Algorithm**: a brute-force-by-increasing-subset-size method, proven
equivalent to textbook NextClosure for this purpose (a pseudo-intent's
defining condition only depends on implications with strictly smaller
premises, and processing subsets in increasing size order is a valid linear
extension of the subset-inclusion order — sufficient for correctness). This
was chosen deliberately over a hand-rolled lectic-order NextClosure after an
earlier attempt at exactly that (for the Exercise 2 canonical base) produced
a subtle bug, caught by validating against a known textbook example. With
only 12 attributes (4,096 subsets), brute force is trivially fast, so there
was no reason to risk the more error-prone approach a second time.

## 2. Results

| | |
|---|---|
| Steps to termination | 282 |
| Implications confirmed (canonical base size) | 123 |
| Distinct counterexample wines used | 158 |
| Soundness check | 0 violations across all 1,599 wines |

The soundness check re-verifies every one of the 123 accepted implications
against the *entire* dataset, not just the wines that happened to be added
as counterexamples during exploration — confirming the base is correct, not
just consistent with the objects it happened to see.

## 3. The most important finding: no small implication survives

**No implication with premise size 1 or 2 exists in the canonical base.**
Every single-attribute and every pair-attribute candidate proposed during
exploration was refuted by some real wine. The smallest exception-free
implications require **3 simultaneous conditions**:

| Premise size | Count |
|---|---|
| 3 | 29 |
| 4 | 39 |
| 5 | 40 |
| 6 | 8 |
| 7 | 2 |
| 8 | 2 |
| 9 | 2 |
| 11 | 1 |

This is the clearest possible illustration of how different real,
noisy measurement data is from a clean curated domain. (For comparison: an
earlier version of this exercise, run on a hand-curated 18-language
programming-language domain, found its *first* confirmed implication at
premise size 1 — `statically_typed -> compiled` — within the first 6 steps.
Here, premise-size-1 and -2 candidates were refuted dozens of times before
anything held.) Real-world chemistry has enough natural variation that
almost any simple univariate or bivariate rule has *some* exception
somewhere in 1,599 wines — which is exactly why Exercise 2's implication
analysis (run on a 200-wine sample, not the full 1,599) found many small
premise implications that looked solid on that sample. This exercise, using
the full dataset as oracle, shows some of those would likely break under a
larger sample too. That's a genuine, useful, somewhat humbling result about
the limits of small-sample implication mining.

## 4. The 29 size-3 implications

The full list is in `notebooks/ex3_attribute_exploration.ipynb` §"size-3
implications" and `data/ex3_canonical_base.csv`. Two patterns dominate:

**`high_sulphates` is the most common conclusion.** Eight of the 29 smallest
implications conclude in `high_sulphates`, all with `good_quality` or
`high_alcohol` in the premise alongside one other attribute, e.g.:

- `good_quality, high_fixed_acidity, high_volatile_acidity -> high_sulphates`
- `good_quality, high_fixed_acidity, high_free_so2 -> high_sulphates`
- `high_alcohol, high_chlorides, high_total_so2 -> high_sulphates`

This corroborates a known finding from the wine-quality literature
(sulphates as a preservative/antimicrobial correlate of quality) and is
*independent* corroboration of a signal this project had not yet surfaced as
strongly in Exercises 1, 2 or 4 — those flagged alcohol and volatile acidity
as the dominant drivers, but sulphates' role only became this visible once
forced through exhaustive small-premise exploration against the full
dataset.

**`citric_acid_present` is the second most common conclusion** (5 of 29),
e.g. `good_quality, high_fixed_acidity, high_residual_sugar -> citric_acid_present`.
This matches Exercise 1's Apriori finding (`quality_tier_High -> citric_acid_present`,
lift 1.51) and Exercise 2's implication #1 — a third independent method
landing on the same relationship.

**No implication has `good_quality` alone or with just one other attribute
in the premise** — quality always needs at least 2 chemistry conditions
alongside it before it forces anything else, confirming what Exercise 1's
K-Means and Apriori results already suggested: quality is not a simple
function of any one or two measurements.

## 5. What was learned

1. **The exploration algorithm itself is exactly as advertised**: it starts
   from the empty premise (the most aggressive possible claim — "every wine
   has all 12 attributes" — gets refuted instantly by wine #0), and
   systematically narrows down through 282 confirm/refute cycles to a sound,
   complete base, with zero manual implication-writing.
2. **Sample size matters enormously for implication mining.** The exact
   same chemistry attributes, mined from a 200-wine sample (Exercise 2) vs.
   exhaustively verified against the full 1,599-wine population (this
   exercise), give qualitatively different pictures — the sample supports
   many small, clean-looking implications that don't actually hold once
   checked against more data. Any implication reported from a sample should
   be understood as a hypothesis about the population, not a settled fact,
   unless re-verified at scale.
3. **Using real data as the oracle, instead of personal domain claims, is
   strictly better when it's available.** This avoided the kind of
   judgment-call ambiguity that a hand-curated table (as attempted first,
   for a programming-languages domain) would have required for borderline
   attributes — every decision here is checkable, not a matter of opinion.
4. **The implications that did survive are chemically interpretable and
   cross-validate against three other methods in this project** (Exercise 1's
   Apriori and decision tree, Exercise 2's closure-based implications,
   Exercise 4's triadic intent comparison), which is reassuring: despite the
   "no small implication survives" finding, the *structure* that does
   survive (sulphates and citric acid's relationship to quality) is the same
   structure every other technique in this project independently found.

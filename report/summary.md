# Knowledge Discovery — Summary Report

Condensed synthesis of `report/ex1_first_layer.md`, `report/ex2_toscana.md`,
`report/ex3_exploration.md`, `report/ex4_triadic.md`, and `report/ex5_tca.md`.
Each exercise applied a different KD/FCA technique to the same UCI Wine
Quality (red) dataset; this report pulls out what each contributed and where
they agree.

## Dataset

1,599 red wines, 11 physicochemical attributes + a 3-8 quality score,
discretised throughout into Low (3-4) / Medium (5-6) / High (7-8) tiers. A
200-wine stratified sample was used for the FCA work (Exercises 2 and 4);
Exercises 1 and 3 used the full 1,599 rows.

## Exercise 1 — First-layer KD (clustering, Apriori, decision tree)

- **K-Means (k=3,4,5)** on standardised chemistry: weak silhouette scores
  across all three (0.189, 0.172, 0.190) that barely move with k — no
  natural cluster count in the chemistry alone. Crosstabbing every cluster
  against the real quality tier shows every cluster at every k is
  majority-Medium (Medium is 82% of the data); none isolates a pure Low or
  High group. **Chemistry-only clustering does not recover quality.** The
  k=3 cluster centers are still chemically coherent and interpretable on
  their own terms: cluster 0 (722 wines, low fixed acidity/citric acid,
  high volatile acidity/pH — "volatile, unstable"), cluster 1 (502 wines,
  high fixed acidity/citric acid/sulphates, low volatile acidity/pH —
  "robust, well-preserved"), cluster 2 (375 wines, high free/total SO2,
  higher sugar, lower alcohol — "heavily sulfited, sweeter").
- **Apriori** (support>=0.1, confidence>=0.6) on 39 one-hot binned items:
  2,199 frequent itemsets, 7,800 rules total, but **0 rules conclude purely
  in `quality_tier_Low` or `quality_tier_High`** — both are minority classes
  (3.9% and 13.6%) and `min_support=0.1` requires >=160/1,599 wines, a bar
  neither rare class clears combined with any other single item. 925 rules
  conclude in `quality_tier_Medium` alone, but their best lift is only ~1.17
  (mostly restate the 82% base rate). The one genuinely interesting result
  came from reversing the direction: `quality_tier_High -> citric_acid>=0.25`
  (confidence 78.8%, **lift 1.51**) — High-quality wines are 51% more likely
  than average to have detectable citric acid.
- **Decision tree** (depth 4): 87.4% train / 82.8% test accuracy. Top splits
  are **alcohol** (<=11.45) and **volatile acidity** (<=0.34), both
  recurring at multiple depths — e.g. a wine with alcohol>11.45,
  fixed_acidity<=11.65 and a low pH/sulphates split reaches a High leaf,
  while volatile_acidity>1.01 with low fixed acidity reaches a Low leaf.

## Exercise 2 — ToscanaJ conceptual information system

- 12 original attributes scaled onto a 200-wine stratified sample: mostly
  ordinal "increasing, include bounds" (e.g. alcohol at 9/11/13%, sulphates
  at 0.4/0.6/0.8), dichotomic single-cut scales for citric acid, chlorides
  and density, and an interordinal scale for pH (3.1/3.4) — chosen
  specifically so the acidic and basic sides of pH could both be expressed,
  which a one-sided ordinal scale would have lost. Result: 33 binary
  attributes, full concept lattice has **10,212 concepts**.
- **Caveat documented in the report itself**: the ToscanaJ exports turned
  out to be single-scale chains (e.g. just the Fixed Acidity 4-node chain),
  not true nested diagrams — confirmed by the object counts in each PNG
  exactly matching the Python-computed bucket counts for that one scale
  alone. The two required nested relationships (Quality x Alcohol, pH x
  Fixed Acidity) were instead computed as real cross-tabulations on the same
  200-wine sample — mathematically the same information a correct nested
  diagram encodes, just computed directly rather than read off a
  (non-existent) diagram. The Quality x Alcohol table shows Medium-quality
  wines concentrated at 9-11% alcohol (120/165) while Good-quality wines
  split toward the higher 11-13% band (16 of 25) — the same upward shift the
  Ex1 tree's top split also captures.
- 249 implications extracted (premise size <=2, sound and complete for that
  size): 229 data-induced, 15 trivial (conclude in a universal attribute —
  `alcohol>=9` and `sulphates>=low(0.4)` hold for literally all 200 sampled
  wines), 5 pure scale artifacts. Five implications were discussed in depth:
  `citric_acid_absent -> volatile_acidity>=low` (support 100/200),
  `density=heavy -> fixed_acidity>=low` (93/200), `total_so2>=medium ->
  free_so2>=low` (35/200, expected since free SO2 is a subset of total SO2
  by definition), `pH<=acidic -> fixed_acidity>=low AND free_so2>=low`
  (21/200), and a 2-attribute nuance with only 11/200 support — high
  volatile acidity only co-occurs with *at least* acceptable quality when
  paired with medium-or-higher fixed acidity and dry sugar, a relationship
  invisible to any single univariate scale.
- pH and fixed acidity are nearly mutually exclusive at the extremes: 90% of
  the 20 most-acidic-pH wines have fixed acidity in the two highest bins,
  while 90% of the 52 most-basic-pH wines have it in the two lowest bins.

## Exercise 3 — Attribute exploration (wine domain, full dataset as oracle)

- 12 independent boolean attributes (single-threshold versions of the Ex2
  scales — e.g. `high_alcohol` = alcohol>=11%, `good_quality` = quality>=7),
  deliberately not the multi-level ordinal scales, to avoid the canonical
  base being dominated by trivial same-attribute chains. The "expert"
  answering each proposed implication was the **full 1,599-row dataset
  itself** — every confirm/refute decision a real lookup, every
  counterexample a real wine, not a subjective domain claim.
- The exploration algorithm itself was a deliberate departure from textbook
  lectic-order NextClosure: a brute-force-by-increasing-subset-size method,
  proven equivalent for correctness (a pseudo-intent's defining condition
  only depends on strictly-smaller premises, and size order is a valid
  linear extension of subset inclusion) and chosen specifically because an
  earlier hand-rolled lectic-order attempt (for Exercise 2) produced a
  subtle bug, caught only by validating against a known textbook example.
  With 12 attributes (4,096 subsets), brute force is instant, so there was
  no reason to risk the fragile approach twice.
- 282-step exploration -> **123-implication canonical base**, using 158
  distinct real wines as counterexamples, verified sound (0 violations)
  by re-checking every accepted implication against all 1,599 wines.
- **Key finding**: no implication with premise size 1 or 2 survives against
  the full dataset, even though Exercise 2's 200-wine sample supported many
  such implications. Smallest surviving implications need 3 simultaneous
  conditions (29 of the 123; the distribution then rises to 39 at size 4,
  40 at size 5, tapering to a single size-11 implication). This is a direct,
  concrete demonstration that sample-size matters: implications mined from
  a sample are hypotheses, not settled facts, until checked at scale — the
  exact same chemistry attributes give a qualitatively different picture
  depending on whether 200 or 1,599 wines back the claim.
- Among the 29 size-3 implications, `high_sulphates` is the most common
  conclusion (8/29, e.g. `good_quality, high_fixed_acidity,
  high_volatile_acidity -> high_sulphates`) and `citric_acid_present` the
  second most common (5/29) — sulphates' role here is a finding *not* as
  visible in Exercises 1/2/4, which had emphasized alcohol and volatile
  acidity instead. No implication has `good_quality` with fewer than 2
  other attributes in its premise, reinforcing Ex1's clustering result that
  quality isn't a simple function of one or two measurements.

## Exercise 4 — Triadic knowledge discovery

- Triadic context: 200 wines (G) x 30 chemistry-only attributes (M, the
  quality-derived attributes excluded since quality is now the condition)
  x {Low, Medium, High} quality tier (B), with each wine incident under
  exactly its own tier — Y is a strict partition of objects across
  conditions, which shapes every other result in this exercise.
- Per-tier dyadic slices: K_Low (8 wines -> 43 concepts), K_Medium (165 wines
  -> 4,781 concepts), K_High (27 wines -> 599 concepts) — concept count
  scales roughly with object count and heterogeneity.
- **Triconcepts reduce to the three per-tier dyadic lattices**: proved
  (a nonempty-extent triconcept can't span two tiers since no wine belongs
  to both) and then verified computationally — all 599 High-tier concepts
  check out as valid triconcepts `(A,B,{"High"})`, and 0 remain valid once C
  is widened to two tiers, exactly as the proof predicts. This required
  catching and fixing a logic bug in the first version of the verification
  code itself (it checked "tier is a member of C" rather than "tier equals
  every element of C"), a useful reminder that even verification code needs
  verifying.
- **Condition implications (`b1 ->_A b2`) degenerate structurally**: because
  no wine belongs to two tiers, this family is either vacuously true (no
  witness in b1 — e.g. `Low ->_{alcohol>=13} b2` is true for any b2, since
  zero Low wines have alcohol>=13) or false for every b2 != b1 whenever b1
  has any witness (e.g. `citric_acid_present` has witnesses in all three
  tiers, making every cross-tier condition implication on it false). Proved
  and demonstrated with concrete examples — a genuine modeling lesson about
  how the choice of incidence relation determines which implication
  families are even observable; only attribute and object implications
  carried real information under this particular Y.
- **Attribute implications** *are* tier-specific and informative: of 191
  High-tier implications (premise <=2), 163 do not hold under the same
  premise in Medium — e.g. `fixed_acidity>=medium ->_High citric_acid_present`
  holds under High but the same premise only forces `fixed_acidity>=low` and
  `alcohol>=9` under Medium.
- **Object implications**: Low tier has zero subset-pairs among its 8 wines
  (chemically scattered, not cohesive, unlike Medium's 318 pairs and High's
  5); a representative High-tier pair shows two wines identical except one
  has `alcohol>=11`.
- Stable (tier-universal) vs. tier-specific concepts: only 4 intents are
  shared across all three tiers (out of 43+4,781+599), while 232 are unique
  to High alone; the representative High-only intent is characterised by
  `alcohol>=11` — the same attribute Exercise 1's tree and Exercise 2's
  nested relationship already flagged, a third independent confirmation.

## Exercise 5 — Temporal Concept Analysis (optional)

- The dataset has no real time dimension, so quality tier (Low -> Medium ->
  High) was used as a **simulated time axis**, explicitly flagged as a
  simplification rather than real chronological data. A sharper consequence,
  building directly on Exercise 4's proof that no wine belongs to more than
  one tier: no individual wine can have a classical life track (there's no
  persisting object to trace). The adaptation: track **concepts** (attribute
  combinations) across the tier sequence instead of individual wines,
  matching by intent (minimal-superset set inclusion) rather than by shared
  objects — the same kind of honest reframing Exercise 4 used for its own
  degenerate implication family.
- Rebuilt Exercise 4's three per-tier lattices independently as a
  self-contained cross-check; sizes matched exactly (43 / 4,781 / 599
  concepts for Low/Medium/High).
- Classified each concept's transition into the next stage as stable /
  refined / split / died / born. Both transitions came back with **zero
  splits** — validated against hand-built toy cases (a known fork and a
  known chain) before trusting this as a real finding rather than a bug:
  every surviving concept refines along one deterministic path, it never
  forks.
- **Low -> Medium** (42 real Low concepts): 23 stable, 13 refined, 6 died,
  and 3,666 *born* — Medium's lattice is so much richer than Low's tiny
  8-wine basis that most Medium combinations have no antecedent at all.
- **Medium -> High** (4,780 real Medium concepts): 364 stable, 2,681
  refined, 1,735 died, and **zero born** — every High-tier combination
  already existed in some form in Medium; High is characterised by which
  Medium combinations *survive* (typically by adding `alcohol>=11`), not by
  anything new.
- A concrete died example: a Low-tier profile combining
  `volatile_acidity>=high(0.7)` (a known fault indicator) with several other
  attributes has no continuation into Medium at all — the specific fault
  pattern that drags a wine down to Low doesn't reappear among better wines.
  A concrete refined example: a Low-stage profile's only change on the path
  into Medium is gaining `alcohol>=11` — the **fourth** independent place in
  this project alcohol's quality-driving role has surfaced.

## Cross-method convergence

The most valuable result of running five independent techniques on the same
data is what they agree on, since each discovers structure in a structurally
different way (a greedy supervised tree; closure-based implications on a
sample; exhaustive implications on the full population; triadic intent
comparison; concept-level life tracks over a simulated timeline):

| Finding | Ex1 | Ex2 | Ex3 | Ex4 | Ex5 |
|---|---|---|---|---|---|
| Alcohol drives quality upward | tree's top split | nested Quality x Alcohol table | — | High-only intent's discriminator | the attribute gained by the refined Low->Medium example |
| Volatile acidity's effect is conditional, not univariate | tree needs multiple VA splits | 2-attribute implication nuance | — | — | its presence marks a profile that dies out, not refines |
| Citric acid presence linked to "good chemistry" / quality | Apriori reverse rule (lift 1.51) | implication #1 | size-3 implications (5/29) | — | — |
| Sulphates linked to quality | — | — | dominant in size-3 implications (8/29) | — | — |
| Quality is not a simple function of 1-2 attributes | weak K-Means separation | — | no premise-size <=2 implication exists | object implications need >=2 conditions | High concepts are refinements/survivors, not new births |

Five different methods landing on the same handful of chemical drivers
(alcohol, volatile acidity, citric acid, sulphates) is meaningful
cross-validation — it wasn't built in by construction, since each exercise's
pipeline has no knowledge of the others' results.

## Honest limitations

- Exercise 2's nested ToscanaJ diagrams were not achieved as true multi-scale
  nestings; substituted with directly-computed cross-tabulations (documented
  in that report, not hidden).
- Exercise 2's implications were mined from a 200-wine sample; Exercise 3
  shows several similarly-shaped small implications do not survive against
  the full 1,599-wine population — Exercise 2's findings should be read as
  sample-level observations, not population-level facts.
- Exercise 4's condition-implication family is structurally uninformative
  given how the triadic incidence was defined (a property of the modeling
  choice specified in `CLAUDE.md`, not a bug).
- Exercise 5's time axis is simulated (quality tier standing in for time),
  and its life tracks are at the concept level, not the object level,
  because no wine persists across tiers (the same partition fact Exercise 4
  proved) — a deliberate, documented substitution, not the textbook
  definition of a TCA life track.

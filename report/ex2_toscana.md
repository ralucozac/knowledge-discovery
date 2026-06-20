# Exercise 2 — ToscanaJ Conceptual Information System

## 1. Method note on the diagrams

ToscanaJ's GUI did not end up producing true nested line diagrams in this
session — each diagram exported (`toscana/diagrams/*.png`) shows a single
scale's chain rather than two scales nested together. Rather than discuss
diagrams that don't show what they're labeled to show, the nesting
relationships below (Quality×Alcohol, pH×Fixed Acidity) are computed
directly as cross-tabulations on the same 200-wine sample (`data/wine_sample_200.csv`)
that Elba's scales were built from. This is the same information a correctly
nested diagram would encode — a nested diagram's node count is exactly the
size of the conjunction of the outer and inner concept's extents — just
computed in pandas instead of read off the ToscanaJ canvas.

This is corroborated, not contradicted, by the exported single-scale
diagrams: every object count in `lattice_main.png`, `nested_quality_alcohol.png`,
and `nested_pH_acidity.png` matches the Python-computed bucket counts exactly
(e.g. the Quality scale's `>=8` node shows 2 objects, matching the 2
"excellent" wines counted in `ex2_implications.ipynb`). That agreement is
the actual evidence the 12 Elba scales are defined correctly — it's just
evidence for the *scales*, not for *nesting*, since nesting never happened.

## 2. Scale justification

All scales use the **ordinal, increasing, include-bounds** generator in
Elba except pH (interordinal). Thresholds were chosen from the attribute
inventory in `CLAUDE.md` §2 and verified against the 200-wine sample
distribution (`notebooks/ex2_prepare_context.ipynb`):

| Attribute | Scale type | Thresholds | Why |
|---|---|---|---|
| Fixed acidity | ordinal | 6, 8, 10 g/L | Splits the sample into roughly even quartile-like bands (5/101/50/44 wines) |
| Volatile acidity | ordinal | 0.3, 0.5, 0.7 g/L | 0.7+ is the conventional "fault" threshold for vinegar taint |
| Citric acid | ordinal, 1 cut (dichotomic) | 0.25 g/L | Below this is treated as chemically negligible / "absent" |
| Residual sugar | ordinal | 4, 12 g/L | Standard dry / off-dry / sweet wine-industry cutoffs |
| Chlorides | ordinal, 1 cut (dichotomic) | 0.08 g/L | Splits the sample roughly in half (99/101) |
| Free SO2 | ordinal | 6, 15, 30 mg/L | Legal/sensory thresholds for sulfite preservation |
| Total SO2 | ordinal | 20, 60, 100 mg/L | Mirrors the free-SO2 bands at the equivalent total-SO2 scale |
| Density | ordinal, 1 cut (dichotomic) | 0.997 g/cm³ | ~water density; separates "light" from "heavy"/sugar-rich wines |
| pH | interordinal | 3.1, 3.4 | Symmetric band around the sample's typical pH (3.0-3.6) |
| Sulphates | ordinal | 0.4, 0.6, 0.8 g/L | Splits the sample into thirds |
| Alcohol | ordinal | 9, 11, 13 %vol | Matches Exercise 1's discretisation, enabling direct comparison |
| Quality | ordinal | 5, 7, 8 | Reproduces the Low/Medium/Good/Excellent tiers used throughout |

A wrong scale here would be, e.g., using a **nominal** scale on alcohol —
that would treat 9% and 13% as unrelated categories and destroy the
"more alcohol implies more of X" implications found below. Ordinal scaling
is what makes those implications expressible at all.

## 3. Concept lattice

The full derived context (200 wines × 33 binary attributes after scaling)
produces a concept lattice of **10,212 concepts** (`notebooks/ex2_implications.ipynb`).
This is too large to interpret node-by-node, which is exactly the motivation
for nested diagrams (decompose the big lattice into a handful of smaller,
readable ones) — and exactly why getting the nesting step working in
ToscanaJ matters for any future iteration of this report.

The four single-scale diagrams that *did* export correctly are simple
4-node (or 3-node, for pH) chains — the expected shape for an ordinal scale,
confirming each scale's chain structure: `top -> >=t1 -> >=t2 -> >=t3`.

## 4. Nested relationship 1 — Quality (outer) × Alcohol (inner)

| Quality \ Alcohol | <9% | 9-11% | 11-13% | >=13% | row total |
|---|---|---|---|---|---|
| <5 (Low) | 0 | 7 | 1 | 0 | 8 |
| 5-6 (Medium) | 0 | 120 | 43 | 2 | 165 |
| 7 (Good) | 0 | 8 | 16 | 1 | 25 |
| >=8 (Excellent) | 0 | 0 | 1 | 1 | 2 |

**Interpretation.** No wine in the sample has alcohol below 9% — alcohol's
"low" bin is empty here, a fact worth flagging on its own (the threshold of
9% sits below the entire sample's range, so it contributes no information;
the same was true for `alcohol>=9` showing up as a universal attribute in
the implications notebook). Within the informative bins, **higher alcohol
shifts the quality distribution up**: Medium-quality wines are concentrated
in 9-11% (120/165 = 73%), but Good-quality wines are split almost evenly
between 9-11% and 11-13% (8 vs 16, i.e. the *majority* of Good wines are in
the higher alcohol band), and the only Excellent wine with alcohol data
above 11% sits at >=13%. This is a data-induced relationship, not a scale
artifact — alcohol and quality were scaled completely independently.

## 5. Nested relationship 2 — pH (outer) × Fixed Acidity (inner)

| pH \ Fixed acidity | <6 | 6-8 | 8-10 | >=10 | row total |
|---|---|---|---|---|---|
| <3.1 (acidic) | 0 | 2 | 3 | 15 | 20 |
| 3.1-3.4 (neutral) | 1 | 56 | 42 | 29 | 128 |
| >=3.4 (basic) | 4 | 43 | 5 | 0 | 52 |

**Interpretation.** This is the cleanest implication-shaped pattern in the
whole context: **no wine with pH >= 3.4 has fixed acidity >= 10**, and
**no wine with pH < 3.1 has fixed acidity < 6**. Both extremes of the pH
scale are essentially mutually exclusive with the corresponding extreme of
fixed acidity — exactly what should be expected chemically (fixed acidity
is one of the main determinants of pH), but the diagram/table makes the
*size* of the effect visible: at pH >= 3.4, fixed acidity bunches in the
two lowest bins (4+43 = 47 of 52 wines, 90%), while at pH < 3.1, it bunches
in the two highest bins (3+15 = 18 of 20 wines, 90%). This mirrors implication
#4 in §6 below.

## 6. Implications

249 implications with premise size ≤ 2 were extracted in
`notebooks/ex2_implications.ipynb` (method: closure under the context's
derivation operators, sound and complete for premises of size 1-2 — see
that notebook for why the full Duquenne-Guigues base was not computed).
Classification: 5 pure scale artifacts, 15 trivial (conclude in a universal
attribute), 229 data-induced.

Five data-induced implications selected for discussion (support = number of
wines satisfying the premise, out of 200):

1. **`citric_acid_absent -> volatile_acidity>=low(0.3)`** (support 100/200).
   Wines with no detectable citric acid never fall into the lowest
   volatile-acidity bin. Citric acid is sometimes added to buffer
   acidity/flavour; its absence co-occurring with higher volatile acidity is
   a real chemistry link, not a byproduct of scaling.

2. **`density=heavy -> fixed_acidity>=low(6)`** (support 93/200). Heavier
   wines (density >= 0.997) are never below the lowest fixed-acidity
   threshold. Density rises with dissolved solids (sugar, acids), so this
   dependency is plausible and the two attributes were scaled completely
   independently of each other.

3. **`total_so2>=medium(60) -> free_so2>=low(6)`** (support 35/200). Once
   total SO2 passes 60 mg/L, free SO2 is always at least 6 mg/L too. Free
   SO2 is a subset of total SO2 by definition, so *some* relationship is
   expected — the informative part is the specific threshold crossing,
   which says something about the binding/free SO2 equilibrium in this
   sample.

4. **`pH<=acidic(3.1) -> fixed_acidity>=low(6) AND free_so2>=low(6)`**
   (support 21/200). The most acidic wines are never in the lowest
   fixed-acidity bin (expected from §5 above), but the co-occurrence with
   free SO2 >= 6 is the more interesting part — it suggests winemakers in
   this sample add at least a baseline of free SO2 to already-stable
   (low-pH) wines rather than skipping sulfite addition.

5. **`fixed_acidity>=medium(8), volatile_acidity>=high(0.7) -> quality>=acceptable(5), residual_sugar=dry`**
   (support 11/200). High volatile acidity (often a fault indicator,
   usually linked to *lower* quality) still always co-occurs with at least
   "acceptable" quality here, provided fixed acidity is also medium-or-above
   and the wine is dry. This 2-attribute-premise nuance — volatile acidity
   alone isn't damning if balanced by fixed acidity and low sugar — is
   invisible from any single univariate scale.

Implications driven by very small premise support (e.g. those generated by
the 2 "excellent"-quality wines, which trivially "imply" almost everything
else they happen to share) are excluded from this list even though they
hold formally — with n<=4 they aren't statistically reliable, and that
caveat belongs in any reading of `data/ex2_implications.csv`.

## 7. Comparison with Exercise 1

The Exercise 1 decision tree (`notebooks/ex1_decision_tree.py`) splits first
on **alcohol** (<=11.45 vs >) and **volatile acidity** (<=0.34) at the top
two levels, with both attributes recurring throughout the tree. This matches
both the Exercise 2 findings directly:

- §4 shows alcohol shifting the quality distribution upward, the same
  direction of effect the tree encodes by branching most of its high-quality
  leaves into the `alcohol > 11.45` side.
- §6 implication 5 shows volatile acidity's effect on quality is not
  univariate — it depends on fixed acidity and sugar — which is exactly why
  the decision tree needs multiple volatile-acidity splits at different
  depths (`<=0.34`, `<=1.01`) combined with other attributes, rather than a
  single clean threshold.

The agreement between an ML model trained on the full 1,599-row dataset and
an FCA-style implication analysis on a 200-row sample is itself a useful
sanity check: both pipelines, run independently, converge on the same two
attributes (alcohol, volatile acidity) as the dominant drivers of quality.

## 8. Outstanding work

- True nested line diagrams (multi-scale) were not achieved in ToscanaJ in
  this session — see §1. If this is revisited, the cross-tabulations in §4-5
  should be re-derived from an actual nested diagram and checked against the
  numbers reported here.
- The 5 implications above are a curated subset of 229; the full table is
  in `data/ex2_implications.csv` for anyone wanting to explore further (e.g.
  premises involving sulphates or total SO2 that weren't discussed here).

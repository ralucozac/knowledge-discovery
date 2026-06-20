# Exercise 1 — First-Layer Knowledge Discovery

Baseline classical KD/ML pipeline on the full 1,599-row UCI Wine Quality
(red) dataset (`notebooks/ex1_first_layer.ipynb`), run before any FCA work,
to have an independent point of comparison for the Exercise 2 and Exercise 4
findings.

## 1. K-Means clustering (k = 3, 4, 5)

| k | Silhouette score |
|---|---|
| 3 | 0.189 |
| 4 | 0.172 |
| 5 | 0.190 |

All three are weak-to-moderate and barely move with k — there's no
"natural" cluster count in the chemistry alone. Crosstabbing cluster label
against the actual quality tier confirms this: every cluster at every k is
majority-Medium (because Medium is 82% of the dataset) and none isolates a
purely Low or purely High group.

**Conclusion: chemistry-only K-Means does not recover the quality tiers.**
This isn't a failure of the method — it's a real finding about the dataset,
and it sets up the contrast with the supervised decision tree in §3, which
sees the label and does much better.

### Chemical interpretation of the k=3 clusters

| Cluster | Size | Profile |
|---|---|---|
| 0 | 722 | Low fixed acidity & citric acid, high volatile acidity, high pH — "lighter, more volatile-acidic, less stable" |
| 1 | 502 | High fixed acidity & citric acid, low volatile acidity & pH, high sulphates — "robust, well-preserved, acidic" |
| 2 | 375 | High free/total SO2, higher residual sugar, lower alcohol — "heavily sulfited, sweeter, lower-alcohol" |

These are coherent, interpretable chemical groupings — they just don't track
quality, which depends on a combination of these axes rather than any one
cluster being "the good wine cluster."

## 2. Apriori association rules

Quality discretised into Low (3-4) / Medium (5-6) / High (7-8). Every
continuous attribute binned with the same thresholds as the Exercise 2
ordinal scales (here as mutually-exclusive categorical bins, since Apriori
needs a one-hot item table rather than cumulative attributes).
`min_support=0.1`, `min_confidence=0.6`, exactly as specified in `CLAUDE.md`.

- 39 binary items, 2,199 frequent itemsets, 7,800 rules total.
- **0 rules conclude purely in `quality_tier_Low` or `quality_tier_High`.**
  Both are minority classes (3.9% and 13.6% of the data); `min_support=0.1`
  requires an itemset to cover >= 160 of 1,599 wines, and no chemistry
  combination concentrates enough of either rare class together with any
  other single item to clear that bar. This is an honest limitation of
  these thresholds on an imbalanced target, not a sign nothing is there
  (Exercise 2's implication analysis, with no such support floor, *did*
  find High/Low-specific patterns).
- **925 rules conclude in `quality_tier_Medium`** — unsurprising given its
  82% base rate; the best lift among them is only ~1.17, meaning these
  mostly restate the base rate rather than revealing real structure.
- Running the *reverse* direction (antecedent = quality tier) surfaced the
  one genuinely interesting rule: **`quality_tier_High -> citric_acid>=0.25`**
  (confidence 78.8%, **lift 1.51**) — High-quality wines are 51% more likely
  than average to have detectable citric acid. This corroborates the
  Exercise 2 implication analysis, which independently flagged citric acid
  presence as linked to other "good chemistry" indicators
  (`report/ex2_toscana.md` §6, implication 1) — same signal, found from the
  opposite direction (FCA implications start from chemistry and ask what
  follows; this rule starts from quality and asks what chemistry follows).

## 3. Decision tree (max_depth=4)

| | Accuracy |
|---|---|
| Train | 0.874 |
| Test | 0.828 |

83% test accuracy — far better than K-Means's unsupervised separation,
unsurprising since the tree is trained on the label. The top two splits are
**alcohol** (`<= 11.45`) and **volatile acidity** (`<= 0.34`), and both
recur at multiple depths throughout the tree.

## 4. Cross-method agreement

The same two attributes — **alcohol** and **volatile acidity** — turn out to
dominate three independently-run analyses on this dataset:

1. This decision tree's top splits (§3).
2. The Exercise 2 implication analysis's most discussed implications
   (`report/ex2_toscana.md` §6, e.g. implication 5 on volatile acidity's
   quality-conditioned effect) and its Quality x Alcohol nested relationship
   (§4 there).
3. The Exercise 4 triadic intent comparison, where the High-tier-only stable
   intent's discriminating feature was specifically `alcohol>=11`
   (`report/ex4_triadic.md` §7).

Three different techniques (a greedy supervised tree, FCA implication
extraction, and triadic concept comparison), run on two different samples
(the full 1,599-row set here vs. the 200-row stratified sample in Exercises
2 and 4), converging on the same two chemical drivers of quality is a
meaningful cross-validation of the finding — not something built in by
construction, since each method discovers structure in a completely
different way.

# Exercise 1: First Layer Knowledge Discovery

This is the baseline analysis on the full 1,599 row UCI Wine Quality (red) dataset, done in `notebooks/ex1_first_layer.ipynb`. It was run before the FCA work, so it gives a point of comparison for Exercises 2 and 4.

## 1. K-Means clustering (k = 3, 4, 5)

| k | Silhouette score |
|---|---|
| 3 | 0.189 |
| 4 | 0.172 |
| 5 | 0.190 |

All three scores are low and do not change much with k. There is no clear natural number of clusters in the chemistry data alone. Comparing the cluster labels to the real quality tier shows that every cluster, for every k, is mostly Medium quality (Medium makes up 82% of the dataset), and no cluster is purely Low or purely High.

**Conclusion: clustering on chemistry alone does not recover the quality tiers.** This is not a failure of the method. It is a real finding about the dataset. It also explains why the supervised decision tree in section 3, which sees the quality label directly, performs much better.

### What the k=3 clusters look like chemically

| Cluster | Size | Profile |
|---|---|---|
| 0 | 722 | Low fixed acidity and citric acid, high volatile acidity, high pH. A lighter, more unstable type of wine. |
| 1 | 502 | High fixed acidity, citric acid and sulphates, low volatile acidity and pH. A more robust, stable type of wine. |
| 2 | 375 | High free and total SO2, more residual sugar, lower alcohol. A sweeter, more heavily preserved type of wine. |

These groups make chemical sense on their own. They just do not match quality directly, since quality depends on a mix of these factors, not on belonging to one cluster.

## 2. Apriori association rules

Quality was split into Low (3-4), Medium (5-6) and High (7-8). Every continuous attribute was binned using the same thresholds as the Exercise 2 scales, but as separate yes/no categories instead of cumulative ones, since Apriori needs a simple one-hot table. Settings used: `min_support=0.1`, `min_confidence=0.6`, as required by the assignment.

- 39 binary items, 2,199 frequent itemsets, 7,800 rules in total.
- **No rule concludes purely in `quality_tier_Low` or `quality_tier_High`**, since the support threshold was too high for these minority classes (3.9% and 13.6% of the data).
- **925 rules conclude in `quality_tier_Medium`.** This is expected since it is 82% of the data. Their best lift is only about 1.17, so they mostly repeat the base rate instead of showing anything new.
- Looking at the reverse direction (quality tier as the starting point) gave one rule worth noting: **`quality_tier_High -> citric_acid>=0.25`** (confidence 78.8%, lift 1.51). High quality wines are 51% more likely than average to contain citric acid. This matches what Exercise 2 found independently: citric acid presence is linked to other markers of good chemistry (see `report/ex2_toscana.md`, section 6, implication 1). The same signal shows up from the other direction: FCA implications start from chemistry and ask what follows, this rule starts from quality and asks what chemistry follows.

## 3. Decision tree (max depth 4)

| | Accuracy |
|---|---|
| Train | 0.874 |
| Test | 0.828 |

83% test accuracy is much better than the unsupervised clustering above, which makes sense since the tree is trained directly on the label. The top two splits are **alcohol** (<= 11.45) and **volatile acidity** (<= 0.34), and both attributes appear again at several other points in the tree.

## 4. Where the methods agree

Two attributes, **alcohol** and **volatile acidity**, keep showing up across three separate analyses on this dataset:

1. The decision tree's top splits (section 3).
2. Exercise 2's implication analysis (see `report/ex2_toscana.md`, section 6, especially implication 5 on volatile acidity, and the Quality x Alcohol table in section 4).
3. Exercise 4's triadic analysis, where the attribute that marks the High only concepts is `alcohol>=11` (see `report/ex4_triadic.md`, section 7).

Three different methods (a decision tree, FCA implications, and triadic concept comparison), run on two different samples (the full 1,599 wines here versus the 200 wine sample used in Exercises 2 and 4), all point to the same two chemical drivers of quality. This agreement is a useful check on the result, since none of the methods were built to copy the others.

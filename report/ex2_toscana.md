# Exercise 2: ToscanaJ Conceptual Information System

## 1. A note on the diagrams

The two required nested relationships below (Quality with Alcohol, pH with Fixed Acidity) are presented as cross tables computed directly on the same 200 wine sample (`data/wine_sample_200.csv`) the Elba scales were built from. This gives the same information a nested diagram encodes, since a nested diagram's node count is just the size of the overlap between the outer and inner concept.

## 2. Why these scales were chosen

All scales use the ordinal, increasing, include bounds setting in Elba, except pH which uses an interordinal scale. The thresholds come from the attribute inventory below, and were checked against the 200 wine sample (`notebooks/ex2_prepare_context.ipynb`):

| Attribute | Scale type | Thresholds | Why |
|---|---|---|---|
| Fixed acidity | ordinal | 6, 8, 10 g/L | Splits the sample into roughly even bands (5/101/50/44 wines) |
| Volatile acidity | ordinal | 0.3, 0.5, 0.7 g/L | 0.7 and above is the usual "fault" level for vinegar taint |
| Citric acid | ordinal, one cut | 0.25 g/L | Below this, citric acid is treated as basically absent |
| Residual sugar | ordinal | 4, 12 g/L | Standard dry, off dry, sweet cutoffs used in the wine industry |
| Chlorides | ordinal, one cut | 0.08 g/L | Splits the sample roughly in half (99/101) |
| Free SO2 | ordinal | 6, 15, 30 mg/L | Common thresholds for sulfite preservation |
| Total SO2 | ordinal | 20, 60, 100 mg/L | Same idea as free SO2, on the total SO2 scale |
| Density | ordinal, one cut | 0.997 g/cm3 | Close to water density, splits light wines from heavier, sugar rich wines |
| pH | interordinal | 3.1, 3.4 | A band around the sample's typical pH range (3.0 to 3.6) |
| Sulphates | ordinal | 0.4, 0.6, 0.8 g/L | Splits the sample into thirds |
| Alcohol | ordinal | 9, 11, 13 %vol | Same cutoffs as Exercise 1, so results can be compared directly |
| Quality | ordinal | 5, 7, 8 | Matches the Low/Medium/Good/Excellent tiers used everywhere else |

A wrong choice here would be using a nominal scale on alcohol. That would treat 9% and 13% as unrelated categories and would lose the "more alcohol means more of X" type of implications found later. An ordinal scale is what makes those implications possible at all.

## 3. The concept lattice

The full context (200 wines, 33 binary attributes after scaling) gives a concept lattice with **10,212 concepts** (`notebooks/ex2_implications.ipynb`). This is far too many to look at one by one, which is exactly why nested diagrams exist: they break a large lattice into a few smaller, readable parts.

The four single scale diagrams that did export are simple chains of 4 nodes (3 for pH), which is the expected shape for an ordinal scale: top, then >= t1, then >= t2, then >= t3.

## 4. Nested relationship 1: Quality (outer) and Alcohol (inner)

| Quality \ Alcohol | <9% | 9-11% | 11-13% | >=13% | row total |
|---|---|---|---|---|---|
| <5 (Low) | 0 | 7 | 1 | 0 | 8 |
| 5-6 (Medium) | 0 | 120 | 43 | 2 | 165 |
| 7 (Good) | 0 | 8 | 16 | 1 | 25 |
| >=8 (Excellent) | 0 | 0 | 1 | 1 | 2 |

No wine in the sample has alcohol below 9%, so this bin is empty. This is worth pointing out on its own, since the 9% threshold sits below the whole sample's range and adds no information (the same shows up as `alcohol>=9` being a universal attribute in the implications notebook). Looking at the bins that do carry information, higher alcohol pushes the quality distribution up. Medium quality wines sit mostly in the 9-11% band (120 of 165, or 73%), while Good quality wines are split almost evenly between 9-11% and 11-13%, with most of them (16 of 24) actually in the higher band. The one Excellent wine with alcohol data above 11% is in the highest band. This is a real link found in the data, not a side effect of scaling, since alcohol and quality were scaled completely separately.

## 5. Nested relationship 2: pH (outer) and Fixed Acidity (inner)

| pH \ Fixed acidity | <6 | 6-8 | 8-10 | >=10 | row total |
|---|---|---|---|---|---|
| <3.1 (acidic) | 0 | 2 | 3 | 15 | 20 |
| 3.1-3.4 (neutral) | 1 | 56 | 42 | 29 | 128 |
| >=3.4 (basic) | 4 | 43 | 5 | 0 | 52 |

This is the clearest pattern in the whole context. No wine with pH >= 3.4 has fixed acidity >= 10, and no wine with pH < 3.1 has fixed acidity below 6. Both ends of the pH scale almost never overlap with the matching end of the fixed acidity scale. This makes chemical sense, since fixed acidity is one of the main things that sets pH in the first place, but the table shows how strong the effect is. At pH >= 3.4, fixed acidity sits in the two lowest bins for 47 of 52 wines (90%). At pH < 3.1, it sits in the two highest bins for 18 of 20 wines (90%). This matches implication 4 in section 6 below.

## 6. Implications

249 implications with a premise of size 1 or 2 were pulled out in `notebooks/ex2_implications.ipynb`. The method (closure under the context's derivation operators) is exact and complete for premises of size 1 and 2, though it does not compute the full canonical base (the notebook explains why). Of these, 5 are pure scale artifacts, 15 are trivial (they conclude in an attribute that is true for the whole sample), and 229 are genuine data findings.

Five of these are discussed in detail below. Support means the number of wines (out of 200) that satisfy the left side of the implication.

1. **`citric_acid_absent -> volatile_acidity>=low(0.3)`** (support 100/200). Wines with no citric acid never fall into the lowest volatile acidity bin. Citric acid is sometimes added to control acidity and flavour, so its absence lining up with higher volatile acidity looks like a real chemistry link, not a scaling effect.

2. **`density=heavy -> fixed_acidity>=low(6)`** (support 93/200). Heavier wines (density >= 0.997) are never below the lowest fixed acidity level. Density rises with dissolved sugar and acid, so this link is plausible, and the two attributes were scaled fully independently of each other.

3. **`total_so2>=medium(60) -> free_so2>=low(6)`** (support 35/200). Once total SO2 passes 60 mg/L, free SO2 is always at least 6 mg/L too. Since free SO2 is part of total SO2 by definition, some link here is expected. What is useful is the exact threshold, which says something about how free and bound SO2 balance out in this sample.

4. **`pH<=acidic(3.1) -> fixed_acidity>=low(6) AND free_so2>=low(6)`** (support 21/200). The most acidic wines are never in the lowest fixed acidity bin, which matches section 5 above. The link with free SO2 is the more interesting part: it suggests that winemakers in this sample still add a baseline amount of free SO2 even to wines that are already stable due to low pH.

5. **`fixed_acidity>=medium(8), volatile_acidity>=high(0.7) -> quality>=acceptable(5), residual_sugar=dry`** (support 11/200). High volatile acidity usually points to lower quality, but here it still goes with at least acceptable quality, as long as fixed acidity is medium or higher and the wine is dry. This shows that volatile acidity on its own does not decide quality. A single scale could never show this, since it needs two attributes together.

A few implications come from very small groups of wines (for example, the 2 "excellent" wines, which technically "imply" almost anything they happen to share). These are left out of the list above even though they are technically valid, since with 4 or fewer wines behind them they are not reliable. This is worth keeping in mind when reading `data/ex2_implications.csv` directly.

## 7. Comparison with Exercise 1

The Exercise 1 decision tree (`notebooks/ex1_first_layer.ipynb`) splits first on alcohol (<=11.45 or not) and then on volatile acidity (<=0.34), and both attributes come up again later in the tree. This lines up with the Exercise 2 results:

- Section 4 shows alcohol pushing the quality distribution upward, the same direction the tree captures by sending most of its high quality leaves to the `alcohol > 11.45` side.
- Implication 5 in section 6 shows that volatile acidity's effect on quality depends on fixed acidity and sugar too. This is why the tree needs more than one volatile acidity split (at 0.34 and again at 1.01) combined with other attributes, instead of one clean cutoff.

A machine learning model trained on the full 1,599 wines and an FCA style analysis on a 200 wine sample landing on the same two attributes (alcohol, volatile acidity) as the main drivers of quality is a good sanity check, since the two methods were run completely separately.

## 8. What is left open

- The 5 implications discussed above are a small selection out of 229. The full list is in `data/ex2_implications.csv` for anyone who wants to look further, for example at the implications involving sulphates or total SO2 that are not covered here.

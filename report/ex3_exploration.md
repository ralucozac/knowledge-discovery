# Exercise 3: Attribute Exploration

The original assignment text for this exercise says to pick a domain we feel comfortable with, run attribute exploration on it, collect expert knowledge, and explain what was learned. The wine domain was kept here, to stay connected with Exercises 1, 2 and 4 instead of switching to something unrelated.

## 1. Setup

**Attributes (12)**: simple yes/no versions of the same chemistry columns used in Exercise 2, but using one flag per attribute instead of the multi-level scales. This avoids the result being full of trivial same-attribute chains (like `alcohol>=13 -> alcohol>=11`), which Exercise 2 already covered as scale artifacts. See section 1 of `notebooks/ex3_attribute_exploration.ipynb` for the exact cutoffs, for example `high_alcohol` means alcohol >= 11%, and `good_quality` means quality >= 7.

**Expert oracle**: instead of relying on personal claims about wine chemistry, the "expert" that answers each proposed implication here is the **full 1,599 row dataset**. Every yes or no decision is a real lookup against actual lab measurements, and every counterexample is a real wine. This is a stronger way to "collect knowledge from experts in the field" than personal judgment, since there is no doubt about whether wine #142 really has those values.

**Algorithm**: a method that checks all subsets in order of increasing size, which gives the same result as the standard NextClosure algorithm for this purpose. The reasoning is that whether a set counts as a new implication only depends on implications with a smaller premise, and checking subsets from smallest to largest respects that order. This approach was chosen instead of writing a NextClosure version by hand, after an earlier attempt at that (for the Exercise 2 base) had a hidden bug, found only by testing it against a known textbook example. With just 12 attributes (4,096 subsets), the simpler method runs almost instantly, so there was no reason to risk the same kind of bug again.

## 2. Results

| | |
|---|---|
| Steps to termination | 282 |
| Implications confirmed (size of the final base) | 123 |
| Distinct counterexample wines used | 158 |
| Soundness check | 0 violations across all 1,599 wines |

The soundness check goes back over all 123 accepted implications and checks them against the whole dataset, not only the wines that were used as counterexamples along the way. This confirms the base is actually correct, not just consistent with the wines it happened to see during the run.

## 3. The main finding: no small implication survives

**No implication with a premise of size 1 or 2 made it into the final base.** Every single attribute and every pair of attributes that was proposed got refuted by some real wine. The smallest implications that hold without exception need 3 conditions at once:

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

This shows clearly how different real, noisy measurement data is from a clean, hand built domain. For comparison, an earlier version of this exercise, run on a small hand built set of 18 programming languages, found its first confirmed implication (`statically_typed -> compiled`) at premise size 1, within the first 6 steps. Here, size 1 and size 2 candidates were refuted again and again before anything held. Real wine chemistry has enough natural variation that almost any simple rule with one or two conditions has some exception among 1,599 wines. This is also why Exercise 2, which only used a 200 wine sample, found many small implications that looked solid there. This exercise, using the full dataset, shows that some of those would likely break if checked against more wines. That is a useful, if slightly humbling, lesson about the limits of mining implications from a sample.

## 4. The 29 implications with premise size 3

The full list is in `notebooks/ex3_attribute_exploration.ipynb` and in `data/ex3_canonical_base.csv`. Two patterns stand out.

**`high_sulphates` is the most common result.** Eight of the 29 smallest implications conclude in `high_sulphates`, usually with `good_quality` or `high_alcohol` in the premise plus one more attribute, for example:

- `good_quality, high_fixed_acidity, high_volatile_acidity -> high_sulphates`
- `good_quality, high_fixed_acidity, high_free_so2 -> high_sulphates`
- `high_alcohol, high_chlorides, high_total_so2 -> high_sulphates`

This matches what is already known in the wine quality literature, where sulphates act as a preservative linked to quality. It is also a new signal for this project: Exercises 1, 2 and 4 had mostly pointed to alcohol and volatile acidity, and sulphates only became this visible once every small combination was checked against the full dataset.

**`citric_acid_present` is the second most common result** (5 of 29), for example `good_quality, high_fixed_acidity, high_residual_sugar -> citric_acid_present`. This matches the Apriori result from Exercise 1 (`quality_tier_High -> citric_acid_present`, lift 1.51) and implication 1 from Exercise 2. That makes three separate methods landing on the same link.

**No implication has `good_quality` together with just one other attribute.** Quality always needs at least 2 other conditions before it forces anything else. This matches what the K-Means and Apriori results in Exercise 1 already suggested: quality is not a simple function of one or two measurements.

## 5. What was learned

1. **The exploration algorithm works as it should.** It starts from the empty premise, the strongest possible claim ("every wine has all 12 attributes"), which is refuted right away by the first wine. From there it works through 282 confirm or refute steps to reach a correct, complete base, with no implication written by hand.
2. **Sample size matters a lot for mining implications.** The same chemistry attributes give a different picture depending on whether they are checked against 200 wines (Exercise 2) or all 1,599 (this exercise). The smaller sample supports many clean looking implications that do not actually hold once more data is added. Any implication found on a sample should be treated as a guess about the full population, not a fact, unless it is checked at full scale.
3. **Using real data as the expert, instead of personal claims, works better when the data is available.** It avoids the kind of judgment call that a hand built table (as tried first, for programming languages) would need for unclear attributes. Every decision here can be checked, it is not a matter of opinion.
4. **The implications that did survive make chemical sense and match three other methods in this project** (the Apriori rules and decision tree from Exercise 1, the implications from Exercise 2, and the triadic comparison from Exercise 4). Even though no small implication survives, the pattern that does survive, the link between sulphates and citric acid with quality, is the same pattern every other method in this project found on its own.

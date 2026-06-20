# Exercise 5: Temporal Concept Analysis (optional, 2 points)

This exercise stands on its own. It only reads `data/wine_sample_200.csv` and imports (without changing) functions from `ex2_prepare_context.py`. Nothing from Exercises 1 to 4 was changed.

## 1. The setup, and its honest limit

The wine dataset has no real time dimension, no vintage, no repeated measurement of the same wine. As a fallback, quality tier (Low, then Medium, then High) is used as a stand in for time, treated as "stages of development", not real chronological time. This needs to be said plainly: no wine actually moves between tiers, these are simply different wines.

There is a sharper problem too, already proven in Exercise 4: each wine belongs to exactly one tier, with no overlap. So **no single wine can have a classic life track**, since there is no object that exists across more than one stage to follow. The fix used here is to track **concepts** (combinations of attributes) across the tier sequence instead of individual wines, and to define the usual life track events, birth, death, refinement, split, merge, staying stable, for these concepts instead. This follows the same idea used in Exercise 4 for its own surprise result (the condition implications that carried no information): name the limit clearly, then find the closest fair substitute instead of forcing the original idea to fit where it does not.

## 2. Setup

The same three per tier contexts from Exercise 4 are rebuilt here on their own (not reusing anything in memory, to keep this exercise self contained), and the lattice sizes match exactly, which is a good check: K_Low (8 wines, 43 concepts), K_Medium (165 wines, 4,781 concepts), K_High (27 wines, 599 concepts).

**Matching rule between stages**: concepts are matched by their attribute set, using set inclusion, but only the closest matches are kept (the smallest possible supersets, not every possible superset, since with Medium's lattice almost 100 times bigger than Low's, using every superset would explode and say nothing useful):

- **stable**: exactly one closest match, and it is identical to the original
- **refined**: exactly one closest match, but slightly bigger (the concept continues and gains attributes)
- **split**: 2 or more closest matches (one concept forks into several more specific ones)
- **died**: no match at all (nothing continues from it)
- **born**: a concept in the next stage that has no match at all in the previous stage

Only concepts with a real, non empty extent are used. Every formal context has a "bottom" concept with every attribute when its extent is empty, which is just a technical artifact, not a real combination, and it would match everything if it were included.

## 3. Checking the method before trusting the result

Both transitions came back with **zero splits**, and that kind of result should be checked carefully before being reported as fact. The matching function was tested on two simple, made up cases with known answers: a real fork (`{a}` matching both `{a,b}` and `{a,c}`) correctly gave both matches, and a chain (`{a}` matching `{a,b}` but not the bigger `{a,b,c}`) correctly gave only the smaller match. Since the method passes both checks, the zero splits result is a real property of this wine data, not a bug. Every concept that continues into the next stage does so along one single path, it never forks. This is specific to this particular binary, ordinal scaled context, not a general rule of TCA.

## 4. Results

| Transition | Stable | Refined | Split | Died | Born |
|---|---|---|---|---|---|
| Low to Medium | 23 | 13 | 0 | 6 | 3,666 |
| Medium to High | 364 | 2,681 | 0 | 1,735 | 0 |

**Low to Medium** is mostly about **birth**: Medium's lattice (4,780 real concepts) is so much bigger than Low's (42) that almost all Medium combinations have no match at all in Low. This makes sense, since Low only has 8 wines and very little variety to begin with. Of Low's 42 concepts, more than half (23) carry over unchanged, 13 continue with one extra attribute, and 6 simply stop there.

**Medium to High** is mostly about **refinement and death**, with **no new births at all**. Every High tier combination already existed in some form in Medium (Medium's 4,780 concepts already cover what High's 598 need). 1,735 of Medium's combinations (36%) do not survive into High, while 2,681 (56%) continue by gaining more attributes. This fits with High being a narrower, more specific group than Medium.

## 5. A few concrete examples

**A combination that dies between Low and Medium**: a profile combining `alcohol>=9, chlorides=high_salt, citric_acid_absent, density=heavy, fixed_acidity>=low(6), pH>=basic(3.4), residual_sugar=off_dry, sulphates>=low(0.4), volatile_acidity>=high(0.7)`, among other attributes. Note `volatile_acidity>=high(0.7)`, which is a known sign of a wine fault. This profile, found among the worst (Low) wines, has no continuation at all once we move to Medium. This makes chemical sense: the fault that helps push a wine down to Low does not show up again as a defining trait among better wines.

**A combination that gets refined between Low and Medium**: a Low stage profile gains exactly one attribute on its way into Medium, `alcohol>=11`. This matches alcohol's role as a driver of quality found elsewhere in this project (the decision tree in Exercise 1, the Quality and Alcohol table in Exercise 2, and the High only concept in Exercise 4). Here it shows up as the exact attribute a concept needs to gain in order to survive into a better quality stage.

**A combination that dies between Medium and High**: a profile with `high_chlorides`, `density=heavy`, `pH=neutral_range`, and high values across both free and total SO2, a "salty, heavily treated" type of wine. This profile simply does not appear among the 27 High wines.

## 6. What this adds on top of Exercise 4

Exercise 4 already showed which concepts stay the same and which are specific to one tier, but as a single comparison across all three tiers at once. This exercise looks at the same lattices step by step instead, moving from Low to Medium and then Medium to High, and that order is what adds something new: **moving toward better quality is mostly about things surviving or dying out, not about new things appearing**. Nothing really new shows up at the High tier. What makes High different is which Medium stage combinations manage to survive, usually by gaining something like higher alcohol, and which ones do not. That is a different statement than just saying "High has its own unique concepts," and it only becomes visible once the tiers are treated as an ordered sequence instead of three separate groups.

## 7. Limitations

- Life tracks here are at the level of concepts, not individual wines, since no wine exists across more than one tier (shown in Exercise 4). This is a deliberate substitute, not the standard definition of a TCA life track.
- The zero splits result, and the difference between the two transitions, are partly caused by how different the three lattices are in size (43 versus 4,781 versus 599 concepts, coming from very different sample sizes of 8, 165 and 27 wines), not purely a clean signal about wine chemistry. This is stated clearly rather than overstated as a discovery.

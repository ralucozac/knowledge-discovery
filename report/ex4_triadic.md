# Exercise 4: Triadic Knowledge Discovery

## 1. The triadic structure

- **Objects (G)**: the 200 sampled wines, the same sample used in Exercise 2.
- **Attributes (M)**: the 30 chemistry only binary attributes from the Exercise 2 context. The 3 quality based attributes are left out, since quality tier is now the condition. Keeping them in M too would let B be guessed directly from M, which would turn the triadic structure back into a dyadic one.
- **Conditions (B)**: quality tier, Low, Medium or High, the same 3 tier split used in Exercise 1 (Low 3-4, Medium 5-6, High 7-8).
- **Incidence (Y)**: a triple (wine, property, tier) is in Y if the wine has that property and the wine's own quality tier matches that tier. This gives 2,732 triples in total (see section 1 of `notebooks/ex4_triadic.ipynb`).

One thing to state clearly from the start: every wine belongs to exactly one tier, so Y splits the wines into three separate groups with no overlap. No wine is counted under more than one tier. This single fact explains almost everything below, including why one of the three implication families ends up carrying no information. This is not a flaw in how the context was set up. The assignment calls for exactly this kind of incidence rule, and finding and showing this effect is a useful result on its own, not something to hide.

## 2. The three dyadic slices

| Tier | Wines | Concepts in K_tier |
|---|---|---|
| Low | 8 | 43 |
| Medium | 165 | 4,781 |
| High | 27 | 599 |

The number of concepts grows roughly with the number of wines. Medium has about 20 times more wines than Low, but about 110 times more concepts, which shows how much more structure a larger and more varied sample produces.

## 3. Triconcepts

**Claim**: since Y splits the wines into three separate groups, any triconcept `(A, B, C)` with a non empty `A` must have `C` containing exactly one tier. The real triconcepts match up exactly with the formal concepts of that tier's own dyadic slice. In other words, `(A, B, {tier})` is a triconcept exactly when `(A, B)` is a formal concept of `K_tier`.

**Why this is true**: if `A` is not empty and `C` contains two different tiers, then every wine in `A` would need to belong to both tiers at once, which cannot happen, since each wine has only one tier. So `C` can only ever have one tier in it when `A` is not empty. With one tier in `C`, the triadic incidence is just the dyadic slice for that tier.

This was checked directly in the notebook (section 3) by testing the maximality condition, instead of writing a full triadic version of NextClosure. Given the argument above, a general triadic algorithm would just be solving a problem that already reduces to three normal dyadic lattices. All 599 High tier concepts pass the check as valid triconcepts `(A, B, {"High"})`, and none of them stay valid once `C` is widened to include Medium as well, which matches the claim exactly.

A first version of this check had a mistake. It tested whether a wine's tier was one of the tiers in `C`, instead of checking that the tier matched every tier in `C`. This wrongly showed some triconcepts as valid when they should not have been. The mistake was caught and fixed before trusting the result, and the corrected version now matches the proof above.

## 4. Implication family 1: attribute implications (A1 implies A2 under tier C)

This means: under tier C, having property A1 means also having property A2. These were computed using the same closure method as Exercise 2, run separately for each tier (exact and complete for premises of size 1 or 2):

| Tier | Implications found (premise size 1 or 2) |
|---|---|
| Low | 155 |
| Medium | 200 |
| High | 191 |

**Example** (a real tier specific result, not a fact true everywhere):

`fixed_acidity>=medium(8)` implies `citric_acid_present`, under the High tier.

This holds for High wines: every High wine with fixed acidity of 8 or more also has detectable citric acid. The same starting point under Medium only leads to `{alcohol>=9, fixed_acidity>=low(6), fixed_acidity>=medium(8), sulphates>=low(0.4)}`, so citric acid is not guaranteed there. 163 such differences between High and Medium were found in total. This is the kind of result triadic analysis is meant to find: a chemistry link that only holds once the wines are limited to the best tier.

## 5. Implication family 2: condition implications (b1 implies b2 under property set A)

This means: wines that have property set A in tier b1 also have it in tier b2. Written out: for every wine g and every property m in A, if (g, m, b1) is in Y then (g, m, b2) is also in Y.

**This family carries no real information here.** Since (g, m, b1) being in Y already means the wine's tier is b1, and the other side would need the same wine's tier to be b2, this cannot happen when b1 and b2 are different. So for any A:

- the implication is **true by default** for every b2, if no wine in tier b1 has property set A
- the implication is **false** for every b2 other than b1, if even one wine in tier b1 has property set A

This was checked with two examples:

| A | Low implies b2 | Medium implies b2 | High implies b2 |
|---|---|---|---|
| `alcohol>=13` (rare, 4 out of 200 overall) | true by default (0 wines) | false (2 wines) | false (2 wines) |
| `citric_acid_present` (common, 100 out of 200) | false (3 wines) | false (77 wines) | false (20 wines) |

**What this means**: choosing "the wine's own tier" as the condition makes this kind of implication useless in practice, since almost every non empty property set ends up false everywhere except trivially when b1 equals b2. This comes directly from how the assignment defines the incidence relation, not from a mistake in the setup. It is worth saying clearly that a different setup, where wines could appear under more than one condition (for example, the same object observed at different times, closer to what Exercise 5 does), would make this type of implication actually useful. For this particular triadic structure, only families 1 and 3 give real information.

## 6. Implication family 3: object implications (g1 implies g2 under tier C)

This means: wine g1's properties are a subset of wine g2's properties, within tier C. Unlike family 2, this works fine here, since it only ever compares two wines inside the same tier.

| Tier | Object implication pairs found |
|---|---|
| Low | 0 |
| Medium | 318 |
| High | 5 |

**Example** (High tier): wine 6 (14 properties) has a property set that is fully contained in wine 12's (15 properties). The only extra property wine 12 has is `alcohol>=11`. These are two High quality wines that are almost identical chemically, except one has more alcohol.

**Low has zero pairs.** With only 8 wines and 30 attributes, no two Low tier wines have one set of properties fully contained in another, they are too different from each other. This is a finding on its own: the Low tier, the 8 lowest scoring wines in the sample, is not a chemically uniform group, unlike Medium and High, where this kind of relationship is common (318 and 5 pairs, once adjusted for how many wines are in each tier).

## 7. Concepts that stay the same versus concepts that are tier specific

| | Count |
|---|---|
| Found in all 3 tiers | 4 |
| Found only in High | 232 |
| Found only in Medium | 4,396 |
| Found only in Low | 17 |

A concept found in **all three tiers**: `{alcohol>=9, fixed_acidity>=low(6), free_so2>=low(6), sulphates>=low(0.4), volatile_acidity>=low(0.3), volatile_acidity>=medium(0.5)}`. This combination of basic thresholds shows up no matter the quality, so it looks like a property of typical red wine chemistry in general, not something that tells tiers apart.

A concept found **only in High**: `{alcohol>=9, alcohol>=11, free_so2>=low(6), sulphates>=low(0.4)}`. The part that stands out is `alcohol>=11`, which matches what the decision tree in Exercise 1 found and what the table in Exercise 2 (section 4 of `report/ex2_toscana.md`) showed: higher alcohol pushes quality up. Seeing the same signal here, through a completely different method, comparing triadic concepts instead of tree splits or a cross table, supports the same result.

## 8. Summary

Of the three triadic implication types covered in this exercise, two of them, attribute and object implications, gave real, tier specific results. The third, condition implications, was shown to carry no real information given how the conditions were defined here, and this was proven directly rather than ignored. The triconcept structure reduces cleanly to three separate dyadic lattices because of the same reason: each wine only belongs to one tier. Because of this, no custom triadic algorithm was needed, just the argument above plus a direct check.

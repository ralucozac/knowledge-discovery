# Exercise 4 — Triadic Knowledge Discovery

## 1. Triadic structure

- **Objects (G)**: the 200 sampled wines (same sample as Exercise 2).
- **Attributes (M)**: the 30 chemistry-only binary attributes from the
  Exercise 2 derived context (the 3 quality-derived attributes are excluded —
  quality tier is now the condition, so keeping it in M as well would make B
  derivable from M and collapse the triadic structure back to dyadic).
- **Conditions (B)**: quality tier `{Low, Medium, High}`, the same 3-tier
  split as Exercise 1 (Low 3-4, Medium 5-6, High 7-8).
- **Incidence (Y)**: `(wine, property, tier) ∈ Y` iff the wine has that
  property **and** the wine's own quality tier equals `tier`. 2,732 triples
  total (`notebooks/ex4_triadic.ipynb`, §1).

**Structural consequence, stated up front**: every wine belongs to exactly
one tier, so Y is a strict partition of objects across conditions — no wine
is incident under more than one tier. This single fact explains almost every
result below, including why one of the three implication families turns out
to be uninformative. It is not a flaw in the construction; CLAUDE.md
specifies exactly this incidence rule, and the degeneracy it produces is
itself a useful thing to have discovered and demonstrated rather than missed.

## 2. Dyadic slices

| Tier | Wines | Concepts in K_tier |
|---|---|---|
| Low | 8 | 43 |
| Medium | 165 | 4,781 |
| High | 27 | 599 |

Concept count scales roughly with object count, as expected — Medium has
~20x the wines of Low and ~110x the concepts, reflecting how much more
combinatorial structure a larger, more heterogeneous sample exposes.

## 3. Triconcepts

**Claim**: because Y is a strict object-tier partition, every triconcept
`(A, B, C)` with nonempty `A` has `|C| = 1`, and the nontrivial triconcepts
correspond exactly to the formal concepts of the matching tier's dyadic
slice — i.e. `(A, B, {tier})` is a triconcept iff `(A, B)` is a formal
concept of `K_tier`.

**Proof sketch**: if `A` is nonempty and `C` contains two distinct tiers
`c1 != c2`, then `A x B x C ⊆ Y` requires every `g ∈ A` to be incident
under *both* `c1` and `c2` simultaneously — impossible, since each wine has
exactly one tier. So `|C| <= 1` for any nonempty-`A` triconcept. With
`|C| = 1`, the incidence reduces exactly to the dyadic slice for that tier.

This was verified computationally (§3 of the notebook) by direct maximality
checks rather than implementing a general triadic NextClosure — given the
structural argument above, a full triadic exploration algorithm would be
solving a problem that's already been reduced to three ordinary dyadic
lattices. All 599 High-tier formal concepts check out as valid triconcepts
`(A, B, {"High"})`, and 0 of them remain valid once `C` is widened to
`{"High", "Medium"}`, confirming the claim exactly.

*(A first version of this check had a logic bug — it tested whether a wine's
tier was a member of C rather than requiring the tier to equal every element
of C — which spuriously "confirmed" violations of the very claim it was
supposed to verify. Caught and fixed before relying on the result; the
corrected check now agrees with the proof.)*

## 4. Implication family 1 — Attribute implications `A1 ->_C A2`

"Under tier C, property A1 entails A2." Computed via the Exercise 2 closure
method, run independently per tier (sound and complete for premise size ≤ 2):

| Tier | Implications found (premise ≤ 2) |
|---|---|
| Low | 155 |
| Medium | 200 |
| High | 191 |

**Worked example** (genuinely tier-conditioned, not a global fact):

> `fixed_acidity>=medium(8) ->_High citric_acid_present`

holds under the High tier (every High wine with fixed acidity ≥ 8 also has
detectable citric acid), but the same premise under Medium only closes to
`{alcohol>=9, fixed_acidity>=low(6), fixed_acidity>=medium(8), sulphates>=low(0.4)}`
— citric acid presence is **not** forced in Medium. 163 such High-vs-Medium
discrepancies were found in total. This is exactly the kind of
tier-conditioned knowledge triadic analysis is meant to surface: a chemistry
relationship that only holds once you restrict to the best wines.

## 5. Implication family 2 — Condition implications `b1 ->_A b2`

"Wines with property-set A in tier b1 also have it in tier b2." Formally:
`forall g, forall m in A: (g,m,b1) ∈ Y => (g,m,b2) ∈ Y`.

**This family degenerates under our incidence relation.** Since
`(g,m,b1) ∈ Y` already requires `tier(g) = b1`, and (for `b1 != b2`) the
consequent requires `tier(g) = b2` for the *same* g — impossible for any
wine that actually satisfies the premise. The implication is therefore:

- **vacuously true** for all `b2` whenever no wine in tier `b1` satisfies `A`
- **false** for every `b2 != b1` whenever at least one wine in tier `b1`
  satisfies `A`

Verified with two examples:

| A | Low ->_A b2 | Medium ->_A b2 | High ->_A b2 |
|---|---|---|---|
| `alcohol>=13` (rare, 4/200 globally) | vacuously true (0 witnesses) | false (2 witnesses) | false (2 witnesses) |
| `citric_acid_present` (common, 100/200) | false (3 witnesses) | false (77 witnesses) | false (20 witnesses) |

**Takeaway**: choosing "the wine's own tier" as the triadic condition makes
condition implications structurally uninformative — almost every nonempty
attribute set yields `false` everywhere except trivially `b1=b2`. This is a
direct consequence of the assignment's specified incidence rule, not a
modeling error on our part, but it's worth flagging explicitly: a different
incidence definition where conditions are not mutually exclusive per object
(e.g. "objects observed across multiple time periods", which is closer to
Exercise 5's setup) would make this implication family meaningful. For this
particular triadic structure, only families 1 and 3 carry real information.

## 6. Implication family 3 — Object implications `g1 ->_C g2`

"Wine g1's properties are a subset of g2's, within tier C." Unlike family 2,
this is well-defined and informative here, since it only ever compares two
wines *within the same tier*.

| Tier | Object-implication pairs found |
|---|---|
| Low | 0 |
| Medium | 318 |
| High | 5 |

**Worked example** (High tier): wine 6 (14 properties) has a property set
that is a strict subset of wine 12's (15 properties) — the only attribute
wine 12 has beyond wine 6 is `alcohol>=11`. Two High-quality wines that are
chemically almost identical except one has more alcohol.

**Low has zero pairs** — with only 8 wines and 30 attributes, no two
Low-tier wines have a clean subset relationship; they're chemically too
scattered. This is itself a finding: the Low tier (the 8 worst wines in the
sample) is not a chemically cohesive group, unlike Medium and High where
subset relationships are common (318 and 5 pairs respectively, scaled by
tier size).

## 7. Stable vs. tier-specific concepts

| | Count |
|---|---|
| Intents common to all 3 tiers | 4 |
| Intents unique to High | 232 |
| Intents unique to Medium | 4,396 |
| Intents unique to Low | 17 |

A representative **stable** (tier-universal) intent:
`{alcohol>=9, fixed_acidity>=low(6), free_so2>=low(6), sulphates>=low(0.4), volatile_acidity>=low(0.3), volatile_acidity>=medium(0.5)}`
— this combination of baseline thresholds shows up regardless of quality,
meaning it's a property of "typical red wine chemistry" rather than
something quality-discriminating.

A representative **High-only** intent:
`{alcohol>=9, alcohol>=11, free_so2>=low(6), sulphates>=low(0.4)}` — the
`alcohol>=11` component is the discriminating piece, consistent with
Exercise 1's decision tree and Exercise 2's nested-relationship finding
(§4 of `report/ex2_toscana.md`) that higher alcohol shifts the quality
distribution upward. Seeing it reappear here, in a completely different
analysis (triadic intent comparison vs. decision-tree splits vs. cross-tab),
is a third independent confirmation of the same signal.

## 8. Summary

Of the three triadic implication families CLAUDE.md asks for, two
(attribute and object implications) produced genuine, tier-specific
knowledge; the third (condition implications) was shown to degenerate
structurally given how the conditions were defined, and that degeneracy was
proven rather than glossed over. The triconcept structure reduces cleanly to
three per-tier dyadic lattices because of the same partition property —
which also means no custom triadic algorithm was needed, just the structural
argument plus a direct verification.

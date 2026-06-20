# CLAUDE.md — Knowledge Discovery Project

This file is the single source of truth for this project. Read it fully before doing anything.
It covers the assignment, dataset, exercise plan, tech stack, and folder layout.

---

## 1. Assignment overview

**Course**: Knowledge Discovery (MSc, Computer Science)
**Goal**: Apply Formal Concept Analysis (FCA) and related techniques to a real dataset,
producing a written report and working artefacts (ToscanaJ project, code, cross-tables).

### Exercises in scope (1–5)

| # | Topic | Points | Status |
|---|-------|--------|--------|
| 1 | Dataset selection + first-layer KD (clustering, rules, decision trees) | — | todo |
| 2 | ToscanaJ conceptual information system (scales, lattice, implications) | 3 | todo |
| 3 | Attribute exploration (canonical implication base from domain expert) | 1 | todo |
| 4 | Triadic knowledge discovery | 2 | todo |
| 5 | Temporal Concept Analysis (TCA) — optional | 2 | todo |

**Total in scope: 8 points.** The assignment awards the total as the final mark; solve carefully.

### Key constraints from the assignment text
- ToscanaJ requires an **older Java version** — Java 8 is known to work.
- Each exercise needs a **detailed written discussion**, not just outputs.
- Scale choices must be **justified**; a wrong scale produces a misleading diagram.
- Separate **scale-artifact implications** (trivial, follow from scale structure alone)
  from **data-induced implications** (the interesting ones).

---

## 2. Dataset choice

**Dataset: UCI Wine Quality** (or a similar Kaggle alternative)
- Source: https://archive.ics.uci.edu/dataset/186/wine+quality
- File: `winequality-red.csv` (1,599 rows × 12 columns)
- Licence: public domain / CC BY 4.0

### Why this dataset

| Criterion | Fit |
|-----------|-----|
| Many-valued attributes | 11 physicochemical attributes (continuous) + 1 quality score (ordinal 3–8) |
| Mix of scale types | Ordinal (quality, alcohol), interordinal (pH, acidity ranges), dichotomic (high/low sugar) |
| Domain knowledge available | Wine chemistry is well-documented; implications are checkable |
| Size | 1,599 rows — large enough to be interesting, small enough for ToscanaJ after sampling |
| Triadic extension | Slice by quality tier (low/medium/high) as the third dimension for Ex. 4 |
| Temporal extension | Vintage year (if using the extended dataset) for Ex. 5 |

### Preprocessing plan
- Keep ~200 rows for ToscanaJ (sample stratified by quality score; full dataset for ML step).
- Round continuous values to meaningful bins before scaling (e.g. alcohol → low/medium/high).
- Export the 200-row subset as `data/wine_toscana.sql` for Elba import.
- Keep the full 1,599-row CSV as `data/winequality-red.csv` for the ML step.

### Attribute inventory

| Attribute | Type | Planned scale |
|-----------|------|---------------|
| fixed acidity | continuous | ordinal (≥ low, ≥ medium, ≥ high) |
| volatile acidity | continuous | ordinal (≥ low, ≥ medium, ≥ high) |
| citric acid | continuous | dichotomic (present / absent, threshold 0.25) |
| residual sugar | continuous | ordinal (dry / off-dry / sweet) |
| chlorides | continuous | dichotomic (low-salt / high-salt) |
| free sulfur dioxide | continuous | ordinal (3 bins) |
| total sulfur dioxide | continuous | ordinal (3 bins) |
| density | continuous | dichotomic (light / heavy, threshold 0.997) |
| pH | continuous | interordinal (≤ acidic, neutral range, ≥ basic) |
| sulphates | continuous | ordinal (3 bins) |
| alcohol | continuous | ordinal (≥ 9%, ≥ 11%, ≥ 13%) |
| quality | integer 3–8 | ordinal (≥ 5 = acceptable, ≥ 7 = good, ≥ 8 = excellent) |

---

## 3. Exercise plan

### Exercise 1 — First-layer knowledge discovery

**Goal**: Extract a baseline layer of knowledge using classical KD/ML techniques before FCA.

Steps:
1. Load `data/winequality-red.csv` with pandas.
2. Run K-Means clustering (k=3, 4, 5) — interpret clusters as quality tiers.
3. Discretise `quality` into Low (3–4), Medium (5–6), High (7–8); run Apriori for association rules
   with min_support=0.1, min_confidence=0.6.
4. Train a Decision Tree (max_depth=4) to predict quality tier; extract rules from the tree.
5. Document findings in `report/ex1_first_layer.md`.

Output files: `notebooks/ex1_first_layer.ipynb`, `report/ex1_first_layer.md`

---

### Exercise 2 — ToscanaJ conceptual information system (3 points)

**Goal**: Build a full FCA pipeline on the wine dataset using ToscanaJ.

Steps:
1. **Prepare derived context** (`notebooks/ex2_prepare_context.ipynb`):
   - Apply the scale definitions from the attribute inventory above.
   - Produce `data/wine_toscana.sql` (HSQLDB-compatible INSERT statements, 200 rows).
   - Verify scale-closed sets are correct (a row with alcohol=14% must also have ≥11% and ≥9%).

2. **Elba (scale editor)**:
   - Open Elba → File > New → Embedded DBMS → load `wine_toscana.sql`.
   - Create scales for each attribute using the planned scale types.
   - For ordinal scales use "increasing, include bounds" mode.
   - For pH use "both, increasing side includes bounds" (interordinal).
   - Save project as `toscana/wine.toscana`.

3. **ToscanaJ (diagram navigation)**:
   - Generate the concept lattice for the full derived context.
   - Create at least **two nested line diagrams**:
     - Outer: quality tier / Inner: alcohol level
     - Outer: pH range / Inner: fixed acidity
   - Export both diagrams as PNG to `toscana/diagrams/`.

4. **Implication analysis** (`notebooks/ex2_implications.ipynb`):
   - Extract all implications from the derived context.
   - Tag each as "scale artifact" or "data-induced".
   - Focus discussion on data-induced ones (these are the knowledge gems).

5. **Report** (`report/ex2_toscana.md`):
   - Justify every scale choice.
   - Interpret each concept node in the main lattice.
   - List and discuss at least 5 non-trivial implications.
   - Compare findings with Exercise 1 results.

Output files: `data/wine_toscana.sql`, `toscana/wine.toscana`, `toscana/diagrams/*.png`,
`notebooks/ex2_prepare_context.ipynb`, `notebooks/ex2_implications.ipynb`, `report/ex2_toscana.md`

---

### Exercise 3 — Attribute exploration (1 point)

**Goal (redefined from the original assignment text)**: Choose a set of
attributes from any domain the solver is comfortable with, perform attribute
exploration on it, and collect/simulate the relevant expert knowledge,
explaining the results and what was learned — rather than following a fixed
recipe.

**Chosen domain**: Programming languages and their type-system / paradigm
properties (computer science domain, well-suited to acting as the domain
expert solo).

**Attribute set** (12 attributes, kept from the original plan since it
already provides a well-balanced, interesting set):

| Attribute | Meaning |
|-----------|---------|
| `statically_typed` | Types checked at compile time |
| `strongly_typed` | No implicit coercions between incompatible types |
| `compiled` | Has a compiled execution mode (not only interpreted) |
| `garbage_collected` | Automatic memory management |
| `object_oriented` | Supports classes and inheritance |
| `functional` | First-class functions, supports higher-order patterns |
| `logic_paradigm` | Supports logic/constraint programming |
| `concurrent_primitives` | Built-in concurrency (goroutines, actors, channels, etc.) |
| `null_safe` | Type system prevents null pointer errors by design |
| `pattern_matching` | Structural pattern matching in the language |
| `macro_system` | Hygienic or procedural macros |
| `memory_manual` | Manual memory management (malloc/free or ownership) |

**Expert oracle**: since this is solo work, "the expert" is a hand-curated
ground-truth table (`notebooks/ex3_attribute_exploration.ipynb`) over an
18-language pool (Python, Java, C++, Haskell, Rust, Go, Prolog, Kotlin,
Swift, TypeScript, Erlang, Lisp, C, Scala, OCaml, Elixir, Clojure, C#), with
explicit, documented judgment-call rules for the ambiguous attributes
(`compiled`, `strongly_typed`, `concurrent_primitives`, `null_safe`,
`pattern_matching`, `macro_system`) so the "expert" answers consistently.

Steps:
1. Start with an empty formal context; implement the attribute exploration
   loop directly (no external FCA library needed — at 12 attributes a
   brute-force-by-increasing-subset-size approach is exact and trivially
   fast, and avoids the bug risk of a hand-rolled lectic-order NextClosure).
2. For each proposed implication, query the oracle: confirm, or refute with
   a real counterexample language.
3. Continue until the algorithm terminates with the canonical base; verify
   soundness by re-checking every accepted implication against the full
   18-language oracle.
4. Document the full exploration transcript, the results, and what was
   learned (including about the limits of forcing soft software-engineering
   concepts into strict boolean attributes) in `report/ex3_exploration.md`.

Output files: `notebooks/ex3_attribute_exploration.ipynb`, `report/ex3_exploration.md`

---

### Exercise 4 — Triadic knowledge discovery (2 points)

**Goal**: Analyse the wine dataset as a triadic context.

**Triadic structure**:
- **Objects (G)**: wine samples (200-row subset)
- **Attributes (M)**: binarised chemical properties (same as derived context from Ex. 2)
- **Conditions (B)**: quality tier — `{Low, Medium, High}`
- **Incidence (Y)**: (wine, property, tier) ∈ Y iff the wine has that property AND belongs to that tier

This answers: "Which chemical properties cluster together specifically within each quality tier,
and which hold universally across all tiers?"

Steps:
1. Build the triadic cross-table (`notebooks/ex4_triadic.ipynb`).
2. Extract the three dyadic slices K_Low, K_Medium, K_High and compute their concept lattices.
3. Find triconcepts: maximal (A, B, C) with A × B × C ⊆ Y.
4. Find examples of all three implication families:
   - Attribute: A₁ →_C A₂ ("under tier C, property A₁ entails A₂")
   - Condition: b₁ →_A b₂ ("wines with properties A in tier b₁ also have them in tier b₂")
   - Object: g₁ →_C g₂ ("wine g₁'s properties are a subset of g₂'s within tier C")
5. Compare per-tier lattices: which concepts are stable across all tiers vs. tier-specific?
6. Report in `report/ex4_triadic.md`.

Output files: `notebooks/ex4_triadic.ipynb`, `report/ex4_triadic.md`

---

### Exercise 5 — Temporal Concept Analysis (2 points, optional)

**Goal**: Investigate temporal evolution of wine quality knowledge.

**Approach**: Use the full wine dataset grouped by year (if extended dataset available),
or simulate a temporal context by treating quality tier as a proxy time axis:
Low → Medium → High as "stages of quality development".

Steps:
1. Build a temporal sequence of dyadic contexts (one per time/quality stage).
2. Track concept life tracks: birth, death, split, merge of concepts across the sequence.
3. Discuss what the temporal evolution reveals about the domain.
4. Report in `report/ex5_tca.md`.

---

## 4. Tech stack

### Python environment
```
python >= 3.10
pandas
numpy
scikit-learn        # K-Means, Decision Tree, preprocessing
mlxtend             # Apriori / association rules
concepts            # FCA — pip install concepts
# OR: fcapy        # alternative FCA library
matplotlib
seaborn
jupyter
```

Install all with:
```bash
pip install pandas numpy scikit-learn mlxtend concepts matplotlib seaborn jupyter
```

### ToscanaJ
- Download: https://toscanaj.sourceforge.net
- Requires: **Java 8** (Java 11+ breaks ToscanaJ's Swing UI)
- Run Elba (scale editor): `run-elba.bat` (Windows) or `runelba.sh` (Linux/macOS)
- Run ToscanaJ (viewer): `run-toscana.bat` or `runtoscana.sh`
- DB backend: embedded HSQLDB — no external DB server needed
- Project file format: `.toscana` (XML)

### Java 8 setup (if needed)
```bash
# macOS (Homebrew)
brew install --cask temurin8

# Linux
sudo apt install openjdk-8-jdk

# Set JAVA_HOME for ToscanaJ only
export JAVA_HOME=$(/usr/libexec/java_home -v 1.8)  # macOS
```

### FCA libraries (Python)
```python
# 'concepts' library — minimal, good for small contexts
import concepts
c = concepts.Context.fromstring("""
       |has_fur|can_fly|has_fins|
Cat    |   X   |       |       |
Bat    |   X   |   X   |       |
Salmon |       |       |   X   |
""")
print(c.lattice)

# 'fcapy' — more complete, supports implications and exploration
from fcapy.context import FormalContext
from fcapy.lattice import ConceptLattice
```

---

## 5. Folder structure

```
knowledge-discovery/
│
├── CLAUDE.md                    ← this file
│
├── data/
│   ├── winequality-red.csv      ← raw dataset (1,599 rows, from UCI)
│   ├── wine_sample_200.csv      ← stratified sample for ToscanaJ
│   └── wine_toscana.sql         ← HSQLDB INSERT statements for Elba
│
├── notebooks/
│   ├── ex1_first_layer.ipynb    ← clustering, assoc. rules, decision tree
│   ├── ex2_prepare_context.ipynb← scale application → derived context → SQL
│   ├── ex2_implications.ipynb   ← extract + classify implications
│   ├── ex3_attribute_exploration.ipynb ← interactive exploration loop
│   └── ex4_triadic.ipynb        ← triadic context + triconcepts
│
├── toscana/
│   ├── wine.toscana             ← ToscanaJ project file (save here from Elba)
│   └── diagrams/
│       ├── lattice_main.png
│       ├── nested_quality_alcohol.png
│       └── nested_pH_acidity.png
│
├── report/
│   ├── ex1_first_layer.md
│   ├── ex2_toscana.md
│   ├── ex3_exploration.md
│   ├── ex4_triadic.md
│   └── ex5_tca.md               ← optional
│
└── requirements.txt
```

---

## 6. Workflow order

```
1. Download data → data/winequality-red.csv
2. ex1 notebook  → first-layer KD, document findings
3. ex2 notebook  → prepare derived context, generate SQL
4. Elba          → load SQL, define scales, save wine.toscana
5. ToscanaJ      → navigate lattice, export diagrams
6. ex2 notebook  → extract implications, classify them
7. ex3 notebook  → attribute exploration on programming languages
8. ex4 notebook  → build triadic context, find triconcepts + implications
9. Write reports → one .md per exercise
```

---

## 7. FCA quick reference for Claude Code

### Formal context
A triple K = (G, M, I) where G = objects, M = attributes, I ⊆ G×M = incidence.
`(g, m) ∈ I` means "object g has attribute m".

### Derivation operators
```
A' = { m ∈ M | ∀g ∈ A : (g,m) ∈ I }   # attributes shared by all objects in A
B' = { g ∈ G | ∀m ∈ B : (g,m) ∈ I }   # objects that have all attributes in B
```

### Formal concept
A pair (A, B) where A' = B and B' = A. A = extent, B = intent.

### Many-valued context
A quadruple K = (G, M, W, I) where W = values and I ⊆ G×M×W (functional).
Write m(g) = w for (g, m, w) ∈ I.

### Conceptual scaling
For attribute m with value set W_m, define a scale S_m = (W_m, S_m, J_m).
The derived context K̇ uses pairs (m, s) as attributes:
`g I̊ (m,s)` iff `(m(g), s) ∈ J_m`

### Scale types
- **Nominal**: each value gets its own attribute (no ordering assumed)
- **Ordinal**: value w_i gets attributes {w_j | w_i ≤ w_j} — "at least w_i"
- **Interordinal**: combines ≤ and ≥ — expresses ranges
- **Dichotomic**: single binary condition (threshold)

### Triadic context
A quadruple K = (G, M, B, Y) where B = conditions, Y ⊆ G×M×B.
A triconcept is a maximal triple (A, B, C) with A×B×C ⊆ Y.

### Attribute implication
`A₁ →_C A₂` holds iff ∀g, ∀b ∈ C: (∀m ∈ A₁: (g,m,b) ∈ Y) ⇒ (∀m ∈ A₂: (g,m,b) ∈ Y)

### Canonical (Duquenne–Guigues) base
The unique minimal complete non-redundant implication base for a formal context.
Produced by the attribute exploration algorithm.

---

## 8. Common pitfalls to avoid

- **ToscanaJ + wrong Java**: use exactly Java 8. Higher versions break the UI silently.
- **Over-scaling**: more than ~10 scale attributes per original attribute → unreadable lattice.
- **Under-scaling**: nominal scale on an ordered attribute loses all ordering information.
- **Mixing trivial and non-trivial implications**: always separate scale-artifact implications
  (e.g. "alcohol ≥ 13% → alcohol ≥ 11%" from the ordinal scale) from data-induced ones.
- **Triadic notation**: triconcepts are (extent, intent, modus) — modus is the set of conditions.
  Don't confuse with dyadic (extent, intent).
- **SQL for HSQLDB**: HSQLDB uses `VARCHAR` not `TEXT`; column names are case-sensitive;
  use `CREATE TABLE` before `INSERT INTO`.
- **Empty context in exploration**: start attribute exploration with zero objects; add
  counterexamples one at a time as the algorithm requests them.

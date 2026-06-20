# A Real World Application of FCA: Wine Sensory Style with Concept Lattices

**Source**: Valente, C.C., Bauer, F.F., Venter, F., Watson, B., Nieuwoudt, H.H. (2018). "Modelling the sensory space of varietal wines: Mining of large, unstructured text data and visualisation of style patterns." *Scientific Reports*, 8, 4987. DOI: [10.1038/s41598-018-23347-w](https://doi.org/10.1038/s41598-018-23347-w). Open access, PMC5862899.

## 1. Motivation

Classic wine sensory science uses trained panels working from a fixed list of descriptors, tested on small numbers of wines, usually tens to a few hundred, since running expert panels is expensive and slow. This limits how broad or detailed the resulting sensory map can be. The authors asked a simple question instead: can a much richer sensory map be built for free, by mining the large amount of unstructured tasting notes that already exist in commercial wine guides, without running a new panel at all?

They looked at two South African white wines with very different amounts of existing research: **Sauvignon blanc** (well studied, used to check the method against known results) and **Chenin blanc** (much less studied, the variety they actually wanted to learn more about).

## 2. The data, and how it became a formal context

- **Source**: the John Platter Wine Guide, a yearly South African publication where 15 to 20 expert tasters write free text notes for thousands of commercial wines each year, with no fixed list of descriptors. Tasters use whatever words match their own impression.
- **Scale**: 2,746 Chenin blanc and 4,352 Sauvignon blanc wines (2008 to 2014), covering at least 85% of all commercial production of both varieties in South Africa during that time. This is a large, real, representative dataset, not a small lab sample.
- **From free text to attributes**: the raw notes (38,503 words for Chenin, 71,892 for Sauvignon) were cleaned. Stop words and non sensory phrases were removed, similar words were merged (for example "passion fruit" and "granadilla" became one descriptor), and repeated words within one wine's note were removed. This left 266 (Chenin) and 250 (Sauvignon) standard aroma descriptors. For the statistics part of the study, only descriptors used 50 or more times over the 7 years were kept, 39 per variety.
- **The formal context**: objects are individual wines, attributes are the standard sensory descriptors, and a wine is linked to a descriptor if that word appears in its tasting note. No scaling was needed here, unlike our wine project, where continuous chemistry values had to be turned into ordinal scales. Here the attributes were already naturally yes or no, since a word either shows up in a description or it does not.

## 3. What FCA actually added

The concept lattice was used as a visual map, not just as a calculation step. Wines and descriptors are both shown as nodes, with descriptor nodes placed higher when they apply to more wines, and lower when they are more specific. Two things about the lattice's shape were read directly from the picture:

- how far left or right a descriptor sits showed how strongly it tells the two varieties apart, descriptors common to both sit near the middle, descriptors specific to one variety sit toward the edges
- how high or low a descriptor sits showed how general or common it is

FCA was not used on its own. It was paired with three standard statistical methods, each answering something the lattice alone could not:

- **Multidimensional scaling (MDS)**, to show which descriptors tend to appear together in the same notes
- **Correspondence analysis (CA)**, to connect descriptors to wine style groups (unwooded dry, wooded dry, semi dry)
- **CART (classification trees)**, to turn this into clear rules for which descriptors point to which style

This combination is the interesting part of the method. The lattice gave structure and an easy to read picture, while the statistical methods gave testable, numeric claims. Neither one on its own would have given both.

## 4. Results

**Checking the method on Sauvignon blanc** (the well known variety, used as a sanity check): the lattice placed "capsicum" at the most Sauvignon specific point, and MDS found the same two sensory groups already known from past research, a herbal/green group (green peas, asparagus) and a fruity group (pineapple, guava, blackcurrant). Getting back a result that was already known, from a method that started from scratch, is strong evidence the method works.

**The new result on Chenin blanc** (the actual goal of the study): **complexity** turned out to be the main thing that separates different styles, going from fresh and crisp wines to more complex, wood influenced ones. CART turned this into clear rules: wines described with words like oak, rich, citrus, spice, vanilla, nuts, creamy, savoury and almond were correctly labelled "wooded" 73% of the time. Wines described with tropical, fresh, crisp, melon, peach, apple, floral and similar words were correctly labelled "unwooded" 56% of the time. This gave a new sensory model for a variety that did not have one before, without running a single new tasting panel.

## 5. Limits the authors mention, and one they do not

The paper is open about a few limits. Only aroma descriptors were used, taste and mouthfeel were left for later work. Turning full sentences into single standard words loses some detail, since two wines described in a similar spirit can end up tokenized differently. They also point out the general risk with this kind of data driven method, that patterns can be found that are not really there, which is exactly why they checked FCA against statistical methods instead of trusting the picture alone.

One thing they do not really discuss: the words used depend on what each taster chose to write, not directly on the wine's chemistry. Two wines that are chemically similar could still get different sensory descriptions just because two different tasters used different words for the same thing. This is a different kind of noise than the chemistry based attributes used in Exercises 1 to 5 in this project. It is worth pointing out, since the authors do not really treat it as a limitation, more as just how their data source works.

## 6. Why FCA fit this problem, and how it compares to our project

FCA fits this kind of problem for the same reason it fit ours: both cases involve many yes or no attributes shared across many objects, with no fixed idea in advance about which combinations matter. The two projects differ in one clear way though, where the binary attributes come from.

- In Exercises 1 to 5, every attribute started as a number (alcohol percent, pH, and so on) that had to be turned into an ordinal or yes/no attribute by hand, with thresholds chosen and explained (see `report/ex2_toscana.md`, section 2).
- In this paper, the attributes (the sensory words) were already naturally yes or no. No scaling was needed, but a harder text cleaning problem took its place.

Both projects also ran into the same lesson on their own: FCA alone was never the full method. In our project, it was paired with checking which implications were scale artifacts versus real findings (Exercise 2), checked again against a decision tree and Apriori (Exercise 1), and against a full exploration over the whole dataset (Exercise 3). In this paper, it was paired with MDS, CA and CART. In both cases, FCA's main job was the same: giving a clear, readable map of the attribute space, while the other methods supplied the numeric proof that the map alone could not.

## 7. Why this counts as a significant application

- **Real scale**: close to 7,000 wines, covering most of an entire country's commercial production of two varieties over 7 years, not a small test dataset.
- **Real impact**: it produced the first published sensory style model for Chenin blanc in South Africa, for a variety that had none before, using data that already existed instead of paying for new tasting panels.
- **Published and peer reviewed** in a major general science journal (*Scientific Reports*, part of Nature), not a small specialist FCA journal, which suggests the result was seen as important outside the FCA research community too.

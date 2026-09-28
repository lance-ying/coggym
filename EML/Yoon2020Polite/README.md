# Yoon, Tessler, Goodman, & Frank (2020) Polite speech emerges from competing social goals.

## Abstract
This dataset captures two behavioral tasks from Yoon et al. (2020) that study how polite language arises from competing communicative goals. Participants either judged whether a target utterance was literally true given a speaker's internal evaluation (Literal Semantics task) or predicted what a speaker would say given a stated social goal and a true evaluation (Speaker Production task). The experiments provide human judgments and production choices used to evaluate a probabilistic model of polite speech.

## Overview
- Converted two experiments from the original online materials: a literal-semantics judgment task (`exp1`) and a speaker-production task (`exp2`).
- Trial definitions are reconstructed from the original JavaScript/HTML and paper; per-participant randomized stimulus content (speaker names, context items) is instantiated deterministically and documented in experiment READMEs. The `exp2` option-order counterbalance is not frozen: it is the experiment's four between-participant conditions, as in the original interface.
- Human response data are included for both experiments using the available processed or raw data releases.

## Source Documents
*Open Mind* publishes this article and its supplementary materials as two separate documents, and both are needed to read this dataset:
- `paper.pdf`: the version of record — Yoon, Tessler, Goodman & Frank (2020), *Open Mind* 4:71-87, doi `10.1162/opmi_a_00035`. Printed folios 71-87, so PDF page *n* = folio *n* + 70. It documents `exp2` (§"Experiment: Speaker production task", article pp. 79-80).
- `supplement.pdf`: the published Supplementary Materials for the same DOI, 1-based pagination. It is the **only** document that describes `exp1` (§"Literal semantics task", supplement pp. 4-5) — the article gives only a bare `N = 51` and a pointer to this document ("see Supplemental Materials: Literal Semantic Task section").

## Directory Structure
- `exp1/`: Literal Semantics task (endorsement judgments of utterance truth given a 0-3 heart state). Documented in `supplement.pdf`, not in `paper.pdf`.
- `exp2/`: Speaker Production task (choose what the speaker would say given goal and true state). The paper's main experiment.

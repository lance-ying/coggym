# Levine et al. (2020) The logic of universalization guides moral judgment.

## Abstract
Levine, Kleiman-Weiner, Schulz, Tenenbaum, and Cushman propose a computational account of universalization in moral judgment and test it across multiple behavioral studies. Participants evaluate moral scenarios that involve threshold dynamics, interest levels, and collective action, with tasks ranging from explanation endorsements to moral permissibility and utility judgments. The study also extends to children to examine developmental continuity.

## Overview
- Converted six benchmark-eligible experiments corresponding to Studies 1-4
  in the main paper.
- Each experiment is in its own `exp*` folder with trial definitions, instructions, and human response data.
- Text-only stimuli are embedded directly in `trial.jsonl`; no external assets were required.

## Directory Structure
- `exp1/`: Study 1 explanation endorsement (12 vignettes x 4 explanations).
- `exp2/`: Study 2a moral judgments across 5 contexts x 2 interest conditions.
- `exp3/`: Study 2b threshold vs no-threshold fishing scenario.
- `exp4/`: Study 3 moral judgments and expected-utility judgments (two groups).
- `exp5/`: Study 4a moral judgments across varying numbers of interested parties.
- `exp6/`: Study 4b collective action curves with slider judgments.

# Tsvilodub et al. (2025) Non-literal Understanding of Number Words by Language Models.

## Abstract
This dataset standardizes the experimental materials used in Tsvilodub et al. (2025) to evaluate non-literal number interpretation in language models, grounded in human judgment data from Kao et al. (2014). The experiments probe (a) listener inferences about prices from utterances, (b) inferred speaker affect given state and utterance, and (c) priors over price distributions and affect. All prompts are represented as text-based stimuli with continuous probability judgments.

## Overview
- The active corpus includes exp1 (price inference from utterance, task 1b only) and exp3b (affect priors).
- Exp2 (affect from state and utterance) is excluded from the active corpus because its 1,226 stimulus cells are too sparsely rated for reliable item-level model–human comparison: the selected cells have a median of two human judgments, and 51 of 100 have at most two.
- Trial stimuli were reconstructed from `data/experiment_1_full.csv` and `data/experiment_3_full.csv` in the original repository.
- Human response data were mapped from `human_data/experiment1-raw.csv` and `human_data/experiment3b-raw.csv` (Kao et al., 2014).
- All active stimuli are text-only; each experiment includes an empty `assets/` folder as required.

## Directory Structure
- `exp1/`: Price inference from utterance. Each trial asks for the probability of 10 possible prices.
- `exp3b/`: Affect prior judgments.

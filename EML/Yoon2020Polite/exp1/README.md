# Yoon et al. (2020) Experiment 1: Literal Semantics Task.

## Abstract
Participants read short scenarios where a speaker's true evaluation of a product/performance is shown on a 0-3 heart scale. They then judge whether a target utterance (terrible/bad/good/amazing with or without negation) is literally true of that state by answering "Yes" or "No."

## Overview
- 35 trials total: 3 practice trials from the original code plus 32 main trials covering all 4 states x 8 utterances.
- Context items (13 domains) and speaker names are randomized in the original experiment; this conversion uses a deterministic instantiation for reproducibility.
- The original source contains hidden legacy slider UI, but the deployed live path presents only the yes/no literal-semantics judgment. The converted HEML matches that deployed behavior.
- Human data are sourced from `original_experiments/02_analysis/01_data/literal_semantics.csv`, which reflects filtered participants and excludes practice trials.

## Directory Structure
- `trial.jsonl`: 35 text-based trials (3 practice + 32 main), each with a heart-state display and a yes/no judgment.
- `config.json`: Metadata and experiment flow (instructions -> practice -> main trials).
- `instruction.jsonl`: One instruction screen plus three practice test trials.
- `human_data_ind.json` / `human_data_mean.json`: Trial-level response data for the main yes/no judgments; practice/test trials are omitted from the human comparison data.
- `assets/`: Empty (all stimuli are text-based in the original experiment).

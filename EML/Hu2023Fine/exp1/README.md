# Hu et al. (2023) Experiment 1: Contextual pragmatic interpretation tasks

## Abstract
374 participants from Floyd et al. (in prep) read short scenarios spanning seven pragmatic phenomena and selected the best interpretation from multiple-choice options. Items include literal distractors and pragmatic targets designed to probe error patterns. Demographic details were not reported in the source release.

## Overview
- 170 text-only trials across seven phenomena: Deceits (20), Indirect Speech (20), Irony (25), Maxims (20), Metaphor (20), Humour (25), Coherence Inference (40).
- One multiple-choice query per trial; option order follows the original materials (no per-participant randomization encoded).
- Human response data are included in `human_data_ind.json` and `human_data_mean.json` using counts (not proportions) per option.

## Directory Structure
- `trial.jsonl`: 170 scenario trials with multiple-choice interpretation queries.
- `config.json`: Experiment metadata and block structure (one block per phenomenon).
- `instruction.jsonl`: One instruction module per phenomenon, taken from the original materials.
- `human_data_ind.json` / `human_data_mean.json`: Participant responses (age and gender not reported; placeholders are used).

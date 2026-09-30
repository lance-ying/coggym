# Aboody et al. (2025) Experiment 2: Pirate-map knowledge inference.

## Abstract
Forty participants (after preregistered inclusion exclusions) viewed pirates choosing whether to fetch a map before searching an island for treasure. On each trial they rated how much the pirates already knew about the treasure location and how informative they believed the map was.

## Overview
- 18 image-based trials spanning island sizes, map travel costs, and map-seeking choices.
- Instructions cover the pirate task rules, a comprehension quiz, and a post-quiz recap before trials.
- Human-response data come from `original_experiments/Data/Experiment 2 Data_Participants.csv`, filtered to participants who passed the beginning inclusion checks and the two end-of-task inclusion trials (Attn1Xpirate > Attn1Xmap and Attn2Xpirate < Attn2Xmap).
- Trial presentation was randomized in the original experiment; `config.json` marks the trial block as randomized.
- The two inclusion trials and post-task questions (difficulty scaling and open-ended responses) are omitted from the converted flow as required.

## Directory Structure
- `trial.jsonl`: Trial definitions with pirate images and two knowledge sliders.
- `config.json`: Metadata and experiment flow (instructions + randomized trials).
- `instruction.jsonl`: Instruction pages and comprehension quiz.
- `human_data_ind.json` / `human_data_mean.json`: Individual and aggregated responses.
- `assets/`: Instruction and trial images (exp2-004.png to exp2-026.png).

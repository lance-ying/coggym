# Aboody et al. (2025) Experiment 1: Egg-hunt knowledge inference.

## Abstract
Forty participants (after preregistered inclusion exclusions) viewed paired egg fields and an agent's choice of which field to search. For each field (left and right), participants rated how much the agent already knew about the prize location on a 0-100 slider.

## Overview
- 19 image-based trials (final preregistered set) with two knowledge sliders per trial.
- Instructions cover the egg-hunt setup, a comprehension quiz, and a post-quiz recap before trials.
- Human-response data come from `original_experiments/Data/Experiment 1 Data_Participants.csv`, filtered to participants who passed the end-of-task inclusion trial (AttnCheck1_LEFT > AttnCheck1_RIGHT).
- Trial presentation was randomized in the original experiment; `config.json` marks the trial block as randomized.
- The final inclusion trial and post-task open-ended questions are omitted from the converted flow as required.

## Directory Structure
- `trial.jsonl`: Trial definitions with egg-hunt images and left/right knowledge sliders.
- `config.json`: Metadata and experiment flow (instructions + randomized trials).
- `instruction.jsonl`: Instruction pages and comprehension quiz.
- `human_data_ind.json` / `human_data_mean.json`: Individual and aggregated responses.
- `assets/`: Instruction and trial images (exp1-002.jpg to exp1-032.jpg).

# Gerstenberg et al. (2018) Experiment 1b: Inference (vision)

## Abstract
Forty-six participants (mean age 39; 21 female) viewed the final landing position of the ball and estimated which of three entry holes it was dropped from using only visual evidence. Participants distributed probability across holes; no audio cues were provided.

## Overview
- 40 inference trials plus 2 practice trials, all silent visual scenes showing the final resting spot.
- Stimuli depict the obstacles and landing location (`world_final_<id>.png`); silent demo videos illustrate typical trajectories.
- Responses use a `hole_probability` multi-slider (Hole 1–3) intended to total ~100%.
- Human-response files are populated for the 40 target trials from the original `experiment_2.db` release. Practice-trial responses are excluded from the comparison files.

## Directory Structure
- `trial.jsonl`: Practice and test inference trials referencing `world_final_<id>.png`.
- `config.json`: Metadata and randomized single-block flow over 40 trials.
- `instruction.jsonl`: Intro pages, silent demos, practice trials, and a comprehension quiz.
- `human_data_ind.json` / `human_data_mean.json`: Target-trial probability judgments and trial means for the 40 non-practice trials.
- `assets/`: Inference stimuli and silent demo videos.

# Gerstenberg et al. (2018) Experiment 1a: Prediction (vision)

## Abstract
Forty-five participants (mean age 37; 21 female) saw the Plinko machine with the starting hole visible and predicted where the ball would land using only visual information. The original task collected 10 clicks to express confidence over landing positions; here the response is captured with a single horizontal slider from left to right wall.

## Overview
- 120 prediction trials (40 worlds × 3 holes) plus 2 practice trials, all with silent stimuli.
- Stimuli show the entry hole and obstacle layout (`world_<id>_hole_<h>.png`); demo videos illustrate silent trajectories.
- Responses use the `landing_x` slider (0 left – 100 right) replacing the original multi-click confidence marking.
- Human-response files are populated for the 120 target trials from the original `prediction_long.csv` release. Raw click x-positions were normalized onto the converted 0-100 wall-to-wall scale. Practice-trial responses are excluded from the comparison files.

## Directory Structure
- `trial.jsonl`: Practice and test prediction trials referencing `world_<id>_hole_<h>.png`.
- `config.json`: Metadata and randomized single-block flow over 120 trials.
- `instruction.jsonl`: Intro pages, silent demo videos, two practice trials, and a comprehension quiz.
- `human_data_ind.json` / `human_data_mean.json`: Target-trial click distributions and mean landing positions for the 120 non-practice trials.
- `assets/`: Prediction stimuli and silent demo videos.

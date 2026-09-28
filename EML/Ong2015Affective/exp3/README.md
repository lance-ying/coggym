# Ong, Zaki, & Goodman (2015) Experiment 3: Cue integration with faces.

## Abstract
Four hundred sixty-five participants completed 10 trials each. On each trial, they saw either the wheel outcome, a face, or both (joint cues) and rated the player's emotions on eight 9-point Likert scales. Ten wheel scenarios and 18 face stimuli were used, with outcomes and faces randomly paired on joint-cue trials.

## Overview
- 10 wheel scenarios (subset of Experiment 1) paired with 18 face images.
- Outcome-only, face-only, and joint-cue trials were equally likely; occlusion flags indicate which cue was hidden.
- Human-response data come from `expt3data.csv` (465 participants, 4650 trials).

## Directory Structure
- `trial.jsonl`: Wheel descriptions plus face images when visible.
- `config.json`: Metadata and randomized block flow.
- `instruction.jsonl`: Task instructions (consent screens removed).
- `human_data_ind.json` / `human_data_mean.json`: Trial-level responses aggregated by cue combination.
- `assets/`: Face stimuli (`.bmp`) copied from the original experiment.

# Ong, Zaki, & Goodman (2015) Experiment 4: Cue integration with utterances.

## Abstract
One hundred fifty participants completed 10 trials each. On each trial, they saw either the wheel outcome, a verbal utterance, or both, and then rated the player's emotions on eight 9-point Likert scales. Ten wheel scenarios and 10 utterances were used, with outcomes and utterances randomly paired on joint-cue trials.

## Overview
- 10 wheel scenarios (same as Experiment 3) paired with 10 utterances.
- Outcome-only, utterance-only, and joint-cue trials were equally likely; occlusion flags indicate which cue was hidden.
- Human-response data come from `expt4data.csv` (150 participants, 1500 trials).

## Directory Structure
- `trial.jsonl`: Wheel descriptions plus utterances when visible.
- `config.json`: Metadata and randomized block flow.
- `instruction.jsonl`: Task instructions (consent screens removed).
- `human_data_ind.json` / `human_data_mean.json`: Trial-level responses aggregated by cue combination.
- `assets/`: Empty (utterances are text-only).

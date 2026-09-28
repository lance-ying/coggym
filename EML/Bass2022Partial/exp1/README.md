# Bass et al. (2022) Experiment 1: Physical conjunction fallacy judgments.

## Abstract
Sixty Mechanical Turk participants (mean age 38 years; 21 female) viewed short animated scenes involving a gray cannonball and a pink sphere above a grassy field with a hole. On each trial, participants rated the likelihood of a specified outcome on a 0-100 slider. Each of five blocks asked a different probability question (p(H&G), p(G), p(H), p(G|H), p(G|~H)) across 15 scenes. Block order was counterbalanced and scene order within blocks was randomized.

## Overview
- 75 main trials (15 scenes x 5 judgment types) with slider responses.
- Example videos and nine comprehension-check questions (across eight pages; questions 5 and 6 share a page) appear before the main task.
- Half of the trials in each block use horizontally mirrored videos, matching the Qualtrics flow.
- Human-response data are from the cleaned sheet in `FULLDATA_2021-09-03.xlsx` (N=60). Demographics (age, gender counts) follow the paper.

## Directory Structure
- `trial.jsonl`: 82 trials total (75 main trials plus 7 comprehension-check practice trials).
- `config.json`: Metadata and 12 counterbalanced block-order conditions.
- `instruction.jsonl`: Instruction pages, example videos, 7 comprehension-check test trials, and 1 comprehension quiz module.
- `human_data_ind.json` / `human_data_mean.json`: Individual and mean slider responses for the 75 main trials.
- `assets/`: Video stimuli (clips + mirrors), example videos, comprehension-check clips, and a schematic image.

## Notes
- The original survey randomized the order of scenes within each block and randomized comprehension-check order. Within-block scene randomization is encoded as enumerated per-condition sequences in `config.json` — 10 scene orderings for each of the 12 block-order conditions, 120 sequences in total. Comprehension-check order is **not** encoded: it is left fixed (`test_check1` … `test_check8`) as a documented simplification, because EML has no vocabulary for randomizing item order *within* an instruction block.
- Progress/break screens, consent, technical checks, and debriefing screens were excluded per conversion instructions.
- Slider endpoints are labeled `0%` and `100%`, matching all 273 slider questions in `Full_Experiment_1.qsf`; sliders start at 50 (`slider_config.default_value`), as stated in the paper ("starting position of 50"). Intermediate labels were not provided in the original survey.

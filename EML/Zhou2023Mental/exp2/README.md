# Zhou et al. (2023) Experiment 2: Selection, prediction, responsibility on friction-reduced towers.

## Abstract
129 Mechanical Turk participants (Mage = 36; 70 male, 59 female) repeated the three Experiment 1 tasks on 43 trials — 42 new towers generated with lower table friction, plus a catch trial reusing an Experiment 1 tower — so blocks could slide. Participants selected which red bricks would fall without the black brick, estimated how many would fall, or rated the black brick’s responsibility (0–100). The same catch-trial and exclusion criteria applied.

## Overview
- Forty-two friction-reduced tower images with varied black-brick placements, plus a reused Experiment 1 catch tower (43 trials per condition); three between-subject conditions (selection, prediction, responsibility).
- Practice physics animations and comprehension quiz identical to Experiment 1; randomized trial order within blocks.
- Catch trial reused for exclusion; demographics collected post-task.

## Directory Structure
- `trial.jsonl`: Selection, prediction, and responsibility trials referencing the friction-reduced stimuli.
- `config.json`: Metadata and three flows (selection, prediction, responsibility).
- `instruction.jsonl`: Instructions and comprehension quiz matching the new stimulus set.
- `human_data_ind.json` / `human_data_mean.json`: Individual and aggregated responses from the released R data.
- `assets/`: Tower images `exp2_*.png` for all trials.

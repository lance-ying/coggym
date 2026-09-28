# Zhou et al. (2023) Experiment 3: White-brick prediction and responsibility.

## Abstract
81 Mechanical Turk participants (Mage = 37.2; 49 male, 32 female) judged whether a highlighted white brick would fall if the black brick were removed and rated the black brick’s responsibility for keeping it on the table (0–100). The same 42 towers were used, plus an exclusion trial (43 trials in total), now focusing on a specific white brick atop the black brick. Prediction and responsibility conditions were between-subject.

## Overview
- Forty-two towers with a designated white brick, plus an exclusion trial (43 trials per condition); two between-subject conditions (prediction, responsibility).
- Practice simulations and comprehension quiz covered color and stability rules; trial order randomized.
- Exclusion catch trial where removal of the black brick clearly could not affect the white brick; demographics collected afterward.

## Directory Structure
- `trial.jsonl`: Prediction and responsibility trials targeting the white brick.
- `config.json`: Metadata and flows for prediction and responsibility conditions.
- `instruction.jsonl`: Instructions plus comprehension quiz about brick color and stability.
- `human_data_ind.json` / `human_data_mean.json`: Individual and aggregated responses from the released R data.
- `assets/`: Tower images `exp3_*.png` reused across conditions.

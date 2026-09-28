# Zhou et al. (2023) Experiment 1: Selection, prediction, responsibility.

## Abstract
121 Mechanical Turk participants (Mage = 34; 74 male, 47 female) viewed 42 stable towers of red and black bricks. Depending on condition, they either selected which red bricks would fall if the black brick were removed, estimated how many would fall on an integer slider, or rated the black brick’s responsibility for keeping the red bricks on the table on a 0–100 slider. A catch trial screened inattentive responses.

## Overview
- Forty-two tower images; each participant completed one of three conditions (selection, prediction, responsibility).
- Practice physics animations and a comprehension quiz preceded the main trials; order within each block was randomized.
- Catch trial with a solitary black brick was used for exclusion; demographic questions followed the task.

## Directory Structure
- `trial.jsonl`: Image-based trials for selection, prediction, and responsibility conditions.
- `config.json`: Metadata and three experiment flows (selection, prediction, responsibility).
- `instruction.jsonl`: Instruction text plus comprehension quiz about brick colors and stability.
- `human_data_ind.json` / `human_data_mean.json`: Individual and aggregated responses from the released R data.
- `assets/`: Tower images `exp1_*.png` used across trials and instructions.

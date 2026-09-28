# Jara-Ettinger & Rubio-Fernandez (2021) Experiment 2: Adapting inferences based on speaker style.

## Abstract
One hundred forty-five Mechanical Turk participants completed a five-trial coordination task with a virtual speaker named Michael, and 122 participants were retained after the original exclusion rule. Michael described blue shapes that varied in size, and participants inferred the referent, estimated how wordy Michael was, and on the final trial inferred Michael's blind spot. The original trackpad judgments are reconstructed here as paired x/y sliders with cumulative trial-screen images and a final blind-spot response pad.

## Overview
- Four between-subject speaker conditions are defined: Reliable, GradedReliable, GradedUnreliable, and Unreliable.
- Each condition contains five fixed sequential trials.
- The converted trial images preserve the original cumulative layout in which previous displays remain on screen.
- Referent and blind-spot judgments are stored on a 0 to 100 display scale with y increasing upward.
- Wordiness judgments are stored on a 0 to 100 slider scale anchored by Never, Sometimes, and Always.

## Directory Structure
- `trial.jsonl`: 20 condition-specific trials with continuous slider queries (`ref_x`, `ref_y`, `cg_x`, `cg_y`, `redundancy`).
- `config.json`: Four experimental conditions with fixed trial order.
- `instruction.jsonl`: Text instructions and a comprehension quiz describing the slider-based reconstruction.
- `human_data_ind.json` / `human_data_mean.json`: Continuous participant judgments from the processed CSV for included participants only.
- `assets/`: Cumulative trial-screen PNGs for all 20 condition-by-trial combinations.

## Conversion Notes
- The original trackpads are reconstructed as separate x and y sliders instead of categorical corner choices.
- Human data come from `Exp2_Participants.csv` after applying the study's inclusion criterion (`Include == "Y"`).
- The processed CSV already canonicalizes the original random stimulus rotations before analysis.

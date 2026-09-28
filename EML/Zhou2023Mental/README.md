# Zhou et al. (2023) Mental Jenga: A Counterfactual Simulation of Physical Support.

## Abstract
People judge whether one object supports another by mentally simulating what would happen if the supporting object were removed. Zhou et al. (2023) tested this counterfactual simulation account across three online experiments with stacked-brick scenes, asking participants either to select which bricks would fall, estimate how many would fall, or rate how responsible a black brick was for stability. Responsibility judgments tracked counterfactual fall predictions, supporting a simulation-based view of physical support.

## Overview
- Converted all three Mental Jenga experiments (selection, prediction, responsibility) into CogGym HEML with pre-rendered stimuli and anonymized human data.
- Trials reference tower images stored in each experiment’s `assets/` directory; queries use multi-select or slider formats aligned with the original psiTurk tasks.
- Human-response files include individual and mean data parsed from the released R datasets.

## Directory Structure
- `exp1/`: Experiment 1 with 42 towers and three conditions (selection, prediction, responsibility) on the original stable stimuli.
- `exp2/`: Experiment 2 with 43 trials (42 friction-reduced towers plus a catch trial reusing an Experiment 1 tower) and the same three conditions.
- `exp3/`: Experiment 3 with 43 trials (42 towers plus an exclusion trial) and two conditions (prediction and responsibility) focusing on whether a highlighted white brick would fall if the black brick were removed.

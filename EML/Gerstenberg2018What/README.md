# Gerstenberg et al. (2018) What happened? Reconstructing the past through vision and sound

## Abstract
Gerstenberg, Siegel, and Tenenbaum (2018) test how people integrate visual and auditory evidence to predict and infer a ball’s path through a Plinko-style machine. Across five experiments, participants either predict landing locations or infer the starting hole based on visual scenes, impact sounds, or both; one experiment hides the final landing position to probe cue integration under occlusion.

## Overview
- Converted Experiments 1a and 1b into CogGym’s HEML format with trials, configs, instructions, and asset links. Experiments 2a, 2b and 3 are not part of this dataset — no trial-level human data was released for them.
- Stimuli include rendered Plinko boards (`world_<id>_hole_<h>.png` for prediction, `world_final_<id>.png` for inference, `world_covered_<id>.png` for occluded inference) plus cover images and audio (`world_<id>_hole_<h>.wav` or `world_<id>.wav`).
- Human data files carry paper-reported participant metadata but no responses; the source package did not include trial-level judgments.

## Directory Structure
- `exp1a/`: Experiment 1a – prediction with vision only (120 prediction trials, 2 practice).
- `exp1b/`: Experiment 1b – inference with vision only (40 inference trials, 2 practice).

Not included: Experiment 2a (prediction, vision + sound), Experiment 2b (inference, vision + sound)
and Experiment 3 (inference with occluded final position).

# Jara-Ettinger & Rubio-Fernandez (2021) Quantitative mental state attributions in language understanding.

## Abstract
This study examines whether listeners make fine-grained inferences about a speaker's knowledge from simple referring expressions. Across three Mechanical Turk experiments, participants inferred intended referents and hidden visual information from what a virtual speaker said and how specifically they said it. The converted package restores continuous trackpad-style behavior for experiments 1 and 2 using paired x/y sliders and ruler-annotated trial images, while experiment 3 preserves the original image-based referent and knowledge judgments.

## Overview
- `exp1/`: Two-display colored-shape task with 28 base trials, two counterbalanced lists, and reconstructed x/y trackpad judgments for two referents plus the blind spot.
- `exp2/`: Five-trial sequential blue-shape task with four speaker-style conditions, cumulative multi-panel screens, reconstructed x/y trackpad judgments, and a wordiness slider.
- `exp3/`: Real-object image task with four Latin-square lists, discrete referent selection, and a certainty slider about the boxed object.

## Conversion Notes
- The original paper is `Science Advances, 7(47), eabj0970` with DOI `10.1126/sciadv.abj0970`.
- Experiments 1 and 2 now use continuous slider tags that align directly with the original processed data columns (`lref_x`, `lref_y`, `rref_x`, `rref_y`, `cg_x`, `cg_y`, `ref_x`, `ref_y`, `redundancy`).
- The original raw Exp1/Exp2 trackpads were rotation- and counterbalance-normalized by the authors' processing scripts; the converted human-data files use those canonical coordinates and rescale them to `0..100`, with y increasing upward.

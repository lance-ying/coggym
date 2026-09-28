# Jara-Ettinger & Rubio-Fernandez (2021) Experiment 1: Joint referent and belief inference.

## Abstract
Sixty Mechanical Turk participants (mean age 35.22 years) completed a coordination task with a virtual collaborator who had a blind spot in a pair of 2x2 colored-shape displays. On each trial, participants inferred the collaborator's intended referent in Display A, the intended referent in Display B, and the location of the blind spot. Responses were made with three 2D trackpads in the original experiment and are reconstructed here as paired x/y sliders; the Display A and Display B scale grids are overlaid directly on the trial displays, while the blind-spot judgment uses the same coordinate scale without an extra visual pad.

## Overview
- Twenty-eight base trial types are defined in `trial.jsonl`.
- Participants completed one of two counterbalanced 14-trial lists.
- The original experiment randomized trial order within each list and counterbalanced display rotation and left/right display order across participants.
- The converted human data use the processed CSV's canonical orientation and map responses onto a 0 to 100 display scale with y increasing upward.

## Directory Structure
- `trial.jsonl`: 28 base trials with six continuous slider queries (`lref_x`, `lref_y`, `rref_x`, `rref_y`, `cg_x`, `cg_y`).
- `config.json`: Two list conditions with randomized single-trial blocks after the instruction block.
- `instruction.jsonl`: Text instructions and a comprehension quiz describing the x/y slider reconstruction.
- `human_data_ind.json` / `human_data_mean.json`: Continuous participant judgments on the reconstructed 0 to 100 scale.
- `assets/`: Base trial images with Display A/B scale-grid overlays, original tutorial JPGs, and the supplemental PDF of stimuli.

## Conversion Notes
- The original 2D trackpads are reconstructed as separate x and y sliders rather than categorical corner choices.
- Human data were taken from `Exp1_Participants.csv`, which already corrects the original left/right counterbalancing, stimulus rotation, and trial-ID typos.
- Slider values are stored on a 0 to 100 scale. x increases from left to right, and y increases from bottom to top.

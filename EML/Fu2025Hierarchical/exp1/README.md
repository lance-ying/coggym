# Experiment 1: Point Density and Object Orientation

## Abstract

This experiment investigated human recognition of 3D point cloud objects under two manipulations: (1) varying point cloud sparsity (20-100% of points) and (2) presentation orientation (upright vs. inverted). The experiment used a between-subjects design for orientation and a within-subjects design for point density.

## Overview

- **Task**: 10-alternative forced choice object classification
- **Stimuli**: Rotating 3D point cloud objects displayed as animated GIFs
- **Conditions**:
  - Orientation: Upright vs. Inverted (between-subjects)
  - Point density: 20%, 30%, 40%, 50%, 60%, 80%, 100% (within-subjects, counterbalanced)
- **Categories**: Airplane, Bottle, Bowl, Chair, Cup, Lamp, Person, Piano, Stool, Table

## Participants

### Upright Condition
- **Recruited**: 56 participants from UCLA Subject Pool
- **Final sample**: 55 participants (1 excluded for reporting lack of seriousness)
- **Demographics**: 45 female, 11 male; Mean age = 19.8 years (SD = 1.4)

### Inverted Condition
- **Final sample**: 47 participants from UCLA Subject Pool
- **Demographics**: 40 female, 7 male; Mean age = 20.4 years (SD = 1.5)

### Total
- **102 participants**, **7,140 judgments**

## Procedure

1. Participants read instructions and completed a practice trial with a rotating plant point cloud
2. For the practice trial, participants had to select "Plant" to proceed; incorrect selections prompted a hint
3. In the main experiment, participants viewed 70 trials (7 objects × 10 categories)
4. Each object was shown at a different downsampling proportion (counterbalanced across participants)
5. Stimuli were displayed for 3 seconds before response options appeared
6. Trials were presented in randomized order
7. A rest break was provided halfway through

## Stimuli

Each stimulus is a GIF showing a rotating point cloud (10 degrees per frame, 10 fps, completing 360° rotation in 3.6 seconds). The point clouds were sampled from the ModelNet40 test set.

### File Structure
- `assets/upright/stimuli_1.gif` through `stimuli_70.gif`: Upright orientation
- `assets/inverted/stimuli_1.gif` through `stimuli_70.gif`: Inverted (upside-down) orientation
- `assets/example.gif`: Practice stimulus (plant)
- `assets/maximize_window.png`: Instruction image

## Results Summary

### Upright Condition
Human accuracy ranged from 86.2% (at 20% point density) to 95.3% (at 100% point density), demonstrating remarkable robustness to reduced point information.

### Inverted Condition
Human accuracy was lower than in the upright condition but remained well above chance level (10%), demonstrating adaptability to atypical viewpoints.

## Directory Contents

| File | Description |
|------|-------------|
| `config.json` | Experiment metadata and flow configuration |
| `trial.jsonl` | Trial definitions with stimuli and response options |
| `instruction.jsonl` | Instruction pages and practice trial |
| `human_data_ind.json` | Individual participant responses by trial type |
| `human_data_mean.json` | Aggregated mean responses and accuracy |
| `assets/` | Stimulus GIFs and instruction images |

## Data Notes

### Trial Type Organization

Human data is organized by trial type (`{condition}_prop{percentage}_{class}`) rather than by specific stimulus file ID, because:
1. The original experiment dynamically assigned which of the 7 objects from each category to show at each proportion level
2. The raw data records (proportion, class, choice, correct) without the stimulus file identifier

For example, `upright_prop80_chair` contains all responses from upright-condition participants who saw a chair at 80% point density.

### Experimental Conditions

The experiment uses two experimental conditions (`upright` and `inverted`) in `config.json`. In the original study, participants were randomly assigned to one condition.

## Key Experimental Parameters

- **Stimulus duration**: 3000ms (delay before response options appear)
- **Intertrial interval**: 500ms
- **Rest break**: After 35 trials
- **Response type**: 10 buttons labeled with object category names

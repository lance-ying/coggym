# Experiment 2: Lego-Like Voxelized Point Clouds

## Abstract

This experiment examined human recognition of 3D objects when local geometric features were disrupted while preserving global shape. Point clouds were converted to Lego-like voxelized representations at varying resolutions, analogous to reducing image resolution. The larger the voxel size, the lower the spatial resolution and the more "blocky" the appearance.

## Overview

- **Task**: 10-alternative forced choice object classification
- **Stimuli**: Rotating 3D voxelized point cloud objects displayed as animated GIFs
- **Conditions**: Voxel sizes of 0.01, 0.05, 0.1, and 0.2 (within-subjects, counterbalanced)
- **Categories**: Airplane, Bottle, Bowl, Chair, Cup, Lamp, Person, Piano, Stool, Table

## Participants

- **Final sample**: 60 participants from UCLA Subject Pool
- **Demographics**: 49 female, 9 male, 1 non-binary, 1 preferred not to say
- **Mean age**: 20.6 years (SD = 3.9)
- **Average completion time**: 6.3 minutes (SD = 2.3)

### Total
- **60 participants**, **2,240 judgments**

## Procedure

1. Participants read instructions explaining the Lego-like voxelized format
2. Completed a practice trial with a plant object
3. In the main experiment, participants viewed 40 trials (10 categories × 4 voxel sizes)
4. Each participant saw 4 random non-overlapping objects from each voxel size per category
5. Stimuli were displayed for 3 seconds before response options appeared
6. Trials were presented in randomized order

## Stimuli

### Voxelization Process
1. Point clouds were converted to voxel grid representations using the Open3D library
2. A voxel grid was superimposed over each point cloud
3. Voxel occupancy was determined by checking which voxels contain points
4. Points were uniformly sampled on the surface of the voxel grid
5. The resulting point cloud was normalized to center at origin and scale to fit within a unit sphere

### Voxel Sizes
- **0.01**: Minimal disruption, nearly original appearance
- **0.05**: Slight blockiness, still clearly recognizable
- **0.1**: Moderate blockiness, some detail loss
- **0.2**: Highly blocky, significant detail loss

### File Naming Convention
`{class}_{index}_voxel_{size}.mp4`

Example: `chair_3_voxel_0.1.mp4` = Chair object #3 at voxel size 0.1

(The original stimuli were animated GIFs, as the paper describes; the corpus
conversion re-encoded them to MP4.)

### File Structure
- `assets/*.mp4`: 160 voxelized point cloud stimuli (4 objects × 10 categories × 4 voxel sizes), all referenced by the flow
- `assets/example.mp4`: Practice stimulus (plant)

(Objects 5–7 of each category were never served and are not present; the 120
stimuli for objects 2–4 were restored in f5e0cb26b after an earlier pruning
pass removed them as unreferenced. `maximize_window.png` was removed by that
same pass and has not been restored.)

## Results Summary

| Voxel Size | Mean Accuracy | 95% CI |
|------------|---------------|--------|
| 0.01 | 93.8% | [91.8%, 95.8%] |
| 0.05 | 91.8% | [89.5%, 94.1%] |
| 0.1 | 84.3% | [81.3%, 87.3%] |
| 0.2 | 66.8% | [62.9%, 70.7%] |

Human performance remained high at smaller voxel sizes (0.01-0.05) with a gradual decline at larger voxel sizes, suggesting humans can effectively recognize objects even when local geometric features are disrupted, provided the global shape remains largely intact.

## Directory Contents

| File | Description |
|------|-------------|
| `config.json` | Experiment metadata and flow configuration |
| `trial.jsonl` | Trial definitions with stimuli and response options |
| `instruction.jsonl` | Instruction pages and practice trial |
| `human_data_ind.json` | Individual participant responses by trial type |
| `human_data_mean.json` | Aggregated mean responses and accuracy |
| `assets/` | Stimulus animations, re-encoded to MP4 (160 stimuli) |

## Data Notes

### Trial Type Organization

Human data is organized by trial type (`lego_voxel{size}_{class}`) representing the 40 unique combinations of voxel size and object category. For example, `lego_voxel0.1_chair` contains all responses from participants who saw a chair at voxel size 0.1.

**Joining the data to `trial.jsonl`.** The two are at different granularities, by necessity. The raw data recorded `(voxel size, class, choice, correct)` and never which stimulus file a participant saw, so responses are pooled over objects — but the flow has to name a specific object per trial, and which object appeared varied per participant. `trial.jsonl` therefore carries 160 trials (`lego_voxel{size}_{class}_ex{n}`, one per object) where the data has 40 keys, and every trial carries `metadata.trial_type` holding the corresponding data key verbatim. Group by that field to analyse: the four exemplar trials of a cell pool onto its one data key.

Analyse at (voxel size × class), which is both the granularity the data has and the one the paper reports. Object identity cannot enter an analysis of these data — it was never recorded, so it is an unobserved nuisance variable that varied within each cell across participants. Note in particular that the trial ids are deliberately *not* reusable as data keys: keying the 56 responses of `lego_voxel0.01_airplane` to `..._ex1` would assert they were all judgements of airplane #1, which is exactly what the design rules out.

### Data Discrepancy

The paper reports 60 participants, but the raw data contains responses from 56 unique participant IDs. The human data files use demographics from the paper (60 participants) with actual response counts from the data (2,240 judgments = 56 participants × 40 trials).

## Key Experimental Parameters

- **Stimulus duration**: 3000ms (delay before response options appear)
- **Intertrial interval**: 500ms
- **Response type**: 10 buttons labeled with object category names
- **Stimuli per participant**: 40 (4 objects per category × 10 categories, one per voxel size)

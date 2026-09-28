# Fu, Kellman, & Lu (2025): Hierarchical Abstraction Enables Human-Like 3D Object Recognition in Deep Learning Models

## Abstract

Both humans and deep learning models can recognize objects from 3D shapes depicted with sparse visual information, such as a set of points randomly sampled from the surfaces of 3D objects (termed a point cloud). Although deep learning models achieve human-like performance in recognizing objects from 3D shapes, it remains unclear whether these models develop 3D shape representations similar to those used by human vision for object recognition. This study conducted two human experiments systematically manipulating point density and object orientation (Experiment 1), and local geometric structure (Experiment 2). Humans consistently performed well across all experimental conditions. The point transformer model provided a better account of human performance than the convolution-based model (DGCNN), with the advantage mainly resulting from the mechanism in the point transformer model that supports hierarchical abstraction of 3D shapes.

## Overview

This dataset contains the converted experimental materials from the cognitive science study examining human 3D object recognition from point cloud displays and comparing performance with deep learning models.

### Experiments

| Experiment | Description | Conditions | Participants | Trials per Participant |
|------------|-------------|------------|--------------|----------------------|
| Exp 1 | Point density and object orientation | Upright vs. Inverted (between-subjects); 7 proportion levels (within-subjects) | 102 total (55 upright, 47 inverted) | 70 |
| Exp 2 | Lego-like voxelized point clouds | 4 voxel sizes (0.01, 0.05, 0.1, 0.2) | 60 | 40 |

### Task Description

Participants viewed rotating 3D point cloud objects displayed for 3 seconds and were asked to identify the object category from 10 options: Airplane, Bottle, Bowl, Chair, Cup, Lamp, Person, Piano, Stool, and Table. The point cloud stimuli were selected from the ModelNet40 dataset, with 7 objects from each of the 10 categories.

## Directory Structure

```
Fu2025Hierarchical/
├── README.md
├── exp1/
│   ├── README.md
│   ├── config.json
│   ├── trial.jsonl
│   ├── instruction.jsonl
│   ├── human_data_ind.json
│   ├── human_data_mean.json
│   └── assets/
│       ├── upright/          # 70 upright point cloud GIFs
│       ├── inverted/         # 70 inverted point cloud GIFs
│       ├── example.gif       # Practice stimulus (plant)
│       └── maximize_window.png
└── exp2/
    ├── README.md
    ├── config.json
    ├── trial.jsonl
    ├── instruction.jsonl
    ├── human_data_ind.json
    ├── human_data_mean.json
    └── assets/               # 280 voxelized point cloud GIFs
```

## Key Findings

1. **Human Robustness**: Humans demonstrated high accuracy (86-95%) across all point density levels, showing remarkable robustness even with sparse 3D information.

2. **Inversion Effect**: Human performance decreased in the inverted condition but remained significantly above chance, demonstrating adaptability to atypical viewpoints.

3. **Voxelization Tolerance**: Humans maintained high accuracy with Lego-like voxelized objects at smaller voxel sizes (0.01-0.05), with gradual decline at larger voxel sizes (0.1-0.2).

4. **Model Comparison**: The Point Transformer model more closely matched human performance patterns than DGCNN, particularly at lower point densities.

5. **Hierarchical Abstraction**: The downsampling mechanism in Point Transformer was identified as the key component supporting global shape bias and human-like recognition.

## Citation

Fu, S., Kellman, P. J., & Lu, H. (2025). Hierarchical Abstraction Enables Human-Like 3D Object Recognition in Deep Learning Models. *Proceedings of the Annual Meeting of the Cognitive Science Society*.

**Paper DOI**: https://arxiv.org/abs/2507.09830

## Data Notes

### Trial-Level Data Limitation

The original experimental code dynamically assigned stimuli to participants based on a randomization scheme. The raw data files record responses with (proportion/voxel, class, choice, correct) but do not include the specific stimulus file identifier. Therefore:

- **Human data is aggregated by trial type** (proportion × class combinations for Exp 1; voxel × class combinations for Exp 2) rather than by specific stimulus file.
- The 70 stimulus files in each condition represent unique objects, but the exact mapping between stimulus files and trial types is not preserved in the original data.

### Participant Counts

| Experiment | Paper | Data | Notes |
|------------|-------|------|-------|
| Exp 1 (upright) | 56 recruited, 55 final | 55 | 1 excluded for reporting lack of seriousness |
| Exp 1 (inverted) | 47 | 47 | - |
| Exp 2 | 60 | 56 | Minor discrepancy; using paper demographics |

## Acknowledgments

This work was supported by the NSF grant BCS-2142269.

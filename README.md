# CogGym

CogGym is a benchmark for comparing human and machine cognition across tasks
grounded in cognitive science.

This repository is the **open 10-study evaluation subset**. It contains 23
experiments spanning all seven CogGym topic groups and all three modalities
(text, image, and video), together with anonymized human responses and the
standalone evaluation code.

## Open subset

| Study | Topic | Modality | Experiments |
| --- | --- | --- | ---: |
| `Yoon2020Polite` | Language and pragmatics | Text | 2 |
| `Tsvilodub2025Nonliteral` | Language and pragmatics | Text | 2 |
| `Radkani2025What` | Moral and responsibility judgments | Text | 4 |
| `Fu2025Hierarchical` | Perception | Video | 2 |
| `Gerstenberg2018What` | Causal and counterfactual reasoning | Video | 2 |
| `Ying2024Grounding` | Theory of mind and social inference | Video | 1 |
| `Bass2022Partial` | Physical reasoning and physical inference | Video | 1 |
| `JaraEttinger2021Quantitative` | Theory of mind and social inference | Image | 3 |
| `Zhou2023Mental` | Physical reasoning and physical inference | Image | 3 |
| `Ong2015Affective` | Emotion attribution | Image | 3 |

The subset was chosen for topic and modality coverage among studies with high
human split-half consistency. It is intended for inspecting the format,
developing evaluation tooling, and reproducing example analyses. Because these
studies are public, they should not be treated as a held-out benchmark.

## Full 50-study dataset

The full 50-study CogGym evaluation dataset is available to qualified
researchers under a signed research-use agreement. Access is limited to
noncommercial evaluation and analysis. The agreement prohibits:

- using any portion of the full dataset to train, fine-tune, align, distill, or
  otherwise optimize a model;
- commercial use; and
- redistribution or public release of the dataset.

To request access, review and sign
[`FULL_DATASET_ACCESS_AGREEMENT.md`](FULL_DATASET_ACCESS_AGREEMENT.md), then
email the signed agreement to [lanceying@mit.edu](mailto:lanceying@mit.edu) with the
subject **CogGym dataset access request**. Access is granted only after the
agreement is countersigned.

## Repository layout

- `EML/`: experiment definitions, stimuli, aggregate human responses, and
  anonymized individual responses.
- `evaluation/`: prompt construction, model execution, response parsing,
  fixed trial selections, scoring, validation, and analysis.

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r evaluation/requirements.txt

# List the 23 experiments.
python -m evaluation.run_models --list

# Inspect one rendered model prompt without making an API call.
python -m evaluation.run_models \
  --experiment JaraEttinger2021Quantitative/exp2 \
  --dry-run

# Validate the complete public subset.
python -m evaluation.validate_package
```

See [`evaluation/README.md`](evaluation/README.md) for the complete runner and
analysis workflow. Documentation is also available at
[coggym-docs-8022f.web.app](https://coggym-docs-8022f.web.app/).

## Citation and attribution

Please cite the CogGym paper and the original studies represented in the
dataset. Original-study citations are recorded in each experiment's
`config.json` and summarized in [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).

## Licensing

Evaluation code is released under the MIT License. CogGym-authored dataset
structure and annotations are released under CC BY 4.0; original study
materials remain subject to their original rights and notices. See
[`LICENSE`](LICENSE), [`DATA_LICENSE.md`](DATA_LICENSE.md), and
[`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).

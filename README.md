# CogGym

CogGym is a benchmark for comparing human and machine cognition across tasks
grounded in cognitive science.

This repository is the **open 10-study evaluation subset**. It contains 23
experiments spanning text, image, and video, together with anonymized human
responses and the standalone evaluation code. Every included study contains at
least one experiment independently replicated in the CogGym paper; all
benchmark-eligible experiments from those studies are included here.

## Open subset

| Study | Topic | Modality | Experiments |
| --- | --- | --- | ---: |
| `Levine2020Logic` | Moral and responsibility judgments | Text | 6 |
| `Yoon2020Polite` | Language and pragmatics | Text | 2 |
| `Tsvilodub2025Nonliteral` | Language and pragmatics | Text | 2 |
| `Hu2023Fine` | Language and pragmatics | Text | 1 |
| `Aboody2025Inferring` | Theory of mind and social inference | Image | 2 |
| `JaraEttinger2021Quantitative` | Theory of mind and social inference | Image | 3 |
| `Chandra2024Cooperative` | Theory of mind and social inference | Image | 1 |
| `Bass2022Partial` | Physical reasoning and physical inference | Video | 1 |
| `Fu2025Hierarchical` | Perception | Video | 2 |
| `sosa2021Moral` | Moral and responsibility judgments | Video | 3 |

The subset was chosen for modality and topic coverage among studies validated
by fresh human replications. It contains 11 text, 6 image, and 6 video
experiments. It is intended for inspecting the format, developing evaluation
tooling, and reproducing example analyses. Because these studies are public,
they should not be treated as a held-out benchmark.

## Full 50-study dataset

The full 50-study CogGym evaluation dataset is available to qualified
researchers under a signed research-use agreement. Access is limited to
noncommercial evaluation and analysis. The agreement prohibits:

- using any portion of the full dataset to train, fine-tune, align, distill, or
  otherwise optimize a model;
- commercial use; and
- redistribution or public release of the dataset.

To request access, review and electronically sign the
[`FULL_DATASET_ACCESS_AGREEMENT.md`](FULL_DATASET_ACCESS_AGREEMENT.md) through
the [CogGym dataset access form](https://coggym.org/dataset-access). After the
signed request is recorded, the form issues a private, short-lived download
link.

For commercial access to the full dataset, contact
[lanceying@mit.edu](mailto:lanceying@mit.edu).

## Repository layout

- `EML/`: experiment definitions, stimuli, aggregate human responses, and
  anonymized individual responses.
- `evaluation/`: prompt construction, model execution, response parsing,
  fixed trial selections, scoring, validation, and analysis.
- `EML_RENDERER.html`: a standalone, local-only browser renderer for inspecting
  experiments, instructions, practice items, response controls, and media.
- `skills/generate-meml/`: an agent skill for reconstructing a paper's
  experiment as source-grounded MEML, compiling it to EML, and preparing the
  result for human review.

## Generate new EML experiments

The repository includes the [`generate-meml`](skills/generate-meml/SKILL.md)
agent skill. It guides an agent through source collection, MEML authoring,
compilation, verification, and a source-evidence report. The skill depends on a
local checkout of the
[`cog-gym-meml`](https://github.com/kasmith/cog-gym-meml) compiler and its
maintained authoring documentation.

For Codex, copy the skill directory into your personal skills folder:

```bash
cp -R skills/generate-meml ~/.codex/skills/
```

Then invoke `$generate-meml` with the target paper and original materials. New
artifacts are created outside `EML/` by default so they can be reviewed before
being added to the public dataset.

## Preview EML in a browser

Open [`EML_RENDERER.html`](EML_RENDERER.html) in Chrome or Edge, then choose the
repository's `EML` directory, a single study directory, or one experiment
directory. The renderer reads the selected files locally; it does not upload
the experiment or record responses. It supports the text, image, video,
single- and multi-slider, choice, multi-select, instruction, quiz, and practice
formats used in this public release.

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

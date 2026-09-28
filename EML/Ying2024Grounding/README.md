# Grounding Language about Belief in a Bayesian Theory-of-Mind (Ying et al., 2024)

This folder contains a CogGym-formatted reconstruction of the human experiment reported in **Ying, L. et al. (2024), “Grounding Language about Belief in a Bayesian Theory-of-Mind.”** Participants watched animations of an agent solving *Doors, Keys, & Gems* puzzles and, at multiple judgment points, rated:

- How likely each of four gems was the player’s goal.
- The probability that two belief statements about hidden keys were true.

The standardized files in `exp1/` were derived from the provided paper (`ying2024grounding.pdf`) and response data (`ying2024grounding.csv`). Where the original statement wording is not available in the supplied files, placeholders indicate that the exact text should be filled in from the paper or source stimuli.

## Contents

- `exp1/` – Experiment files in the HEML/CogGym schema (see that directory’s README for details).
- `build_ying2024grounding.py` – Script used to transform `ying2024grounding.csv` into HEML files.

## Key Notes and Caveats

- **Belief statement text**: Only numeric ratings were included in the CSV. The prompts in `trial.jsonl` therefore reference plan-specific statement slots; populate them with the exact wording from the paper or original stimuli if you have access.
- **Stimulus media**: The original animations are not bundled here. Trials reference text descriptions of the judgment point instead of GIFs/videos.
- **Participants**: 100 Prolific participants (US); mean age 39.57; gender: 50 female, 49 male, 1 agender.

See `exp1/README.md` for schema details, file descriptions, and trial-level metadata.

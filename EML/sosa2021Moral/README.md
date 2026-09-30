# Sosa2021Moral CogGym Dataset

This directory packages the visual moral judgment experiments from **Sosa et al. (2021), "Moral Dynamics: Grounding Moral Judgment in Intuitive Physics and Intuitive Psychology"** into the CogGym / HEML data standard.

Each experiment folder contains:
- `config.json` (study metadata and flow)
- `trial.jsonl` (stimuli definitions and prompts)
- `instruction.jsonl` (pre-task instructions and quizzes)
- `human_data_ind.json` / `human_data_mean.json` (individual and aggregated responses)
- `assets/` (MP4 videos used as stimuli)
- `README.md` (experiment-specific summary)

Source materials were taken from `moral_dynamics/` in this repository (code, data, and videos) plus the accompanying paper `moral_dynamics/Sosa2021Moral.pdf`.

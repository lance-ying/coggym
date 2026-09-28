# Experiment 1 – Doors, Keys, & Gems Belief Ratings

Human participants observed an agent navigating Doors-Keys-Gems gridworlds. At predefined judgment points, they:

1. Selected all goal gems they judged likely (Triangle, Square, Hexagon, Circle).
2. Rated two natural-language belief statements about the locations of hidden keys on a 1–7 scale (1 = definitely false, 7 = definitely true).

## Provenance

- **Paper**: Ying et al. (2024), *Grounding Language about Belief in a Bayesian Theory-of-Mind* (`ying2024grounding.pdf`, arXiv:2402.10416).
- **Data source**: `ying2024grounding.csv` (1954 rows; 100 US participants). The converted human data covers the 1901 rows whose trial cells are present in `trial.jsonl`; raw `4_2_step2` rows are not represented because that converted trial is absent.
- **Stimuli**: GIF trajectory segments from `data/stimuli/segments` are copied into `exp1/assets/segments` and referenced in `trial.jsonl`. The source repository is missing `p4_2_3.gif`, so `4_2_step2` is not included in the current converted trial set.
- **Belief statements**: `trial.jsonl` now embeds the exact statement text from `data/stimuli/stimuli.json` rather than placeholder labels.

## Files

- `trial.jsonl` – 42 trial definitions: 38 main target trials plus 4 demo/practice trials. Each main trial shows the corresponding GIF segment, followed by three queries:
  - `goal_rating` (multi-select across four gems).
  - `belief_statement_1` (single-slider, 1–7).
  - `belief_statement_2` (single-slider, 1–7).
- `assets/segments/` – GIF stimuli copied from `data/stimuli/segments` for the converted trial set.
- `config.json` – Metadata and experiment flow (blocks grouped by plan; no randomization).
- `instruction.jsonl` – Simplified instructions plus a short comprehension check on the rating scales.
- `human_data_ind.json` – Individual-level responses grouped by `stimuli_id` (goal multi-select one-hot arrays + statement ratings).
- `human_data_mean.json` – Mean ratings per query/tag for each trial. Goal means are per-option selection frequencies.

## Trial indexing

Plan identifiers and judgment points reconstructed from the CSV:

```
1_1: steps [1, 2] @ timesteps [4, 6]
1_2: steps [1, 2] @ timesteps [17, 20]
1_3: steps [1, 2, 3] @ timesteps [16, 19, 21]
2_1: steps [1, 2] @ timesteps [5, 10]
2_2: steps [1] @ timesteps [6]
3_1: steps [1, 2] @ timesteps [4, 6]
4_1: steps [1, 2] @ timesteps [6, 9]
4_2: steps [1] @ timesteps [6]
5_1: steps [1, 2] @ timesteps [4, 8]
5_2: steps [1, 2, 3] @ timesteps [3, 10, 14]
6_1: steps [1, 2] @ timesteps [3, 7]
6_2: steps [1, 2, 3] @ timesteps [5, 9, 15]
7_1: steps [1, 2] @ timesteps [4, 7]
7_2: steps [1, 2] @ timesteps [3, 7]
8_1: steps [1, 2, 3] @ timesteps [8, 18, 25]
8_2: steps [1, 2] @ timesteps [5, 8]
9_1: steps [1, 2] @ timesteps [3, 9]
9_2: steps [1, 2] @ timesteps [6, 8]
```

## Data notes

- `goal_rating` responses in the CSV are normalized over selected options. The converted human data stores the recovered multi-select response as one-hot arrays in `human_data_ind.json`; `human_data_mean.json` reports selection frequencies. Keys `goal_rating_1`–`goal_rating_4` correspond to Triangle, Square, Hexagon, Circle.
- `belief_statement_*` ratings preserve the original 1–7 scale.
- `judgment_count` = 5,703 (1901 included rows × 3 query responses per row).
- Participant demographics: `count=100`, mean age 39.57, gender breakdown: 50 female, 49 male, 1 agender (all recruited via Prolific, US).

# Ong, Zaki, & Goodman (2015) Experiment 1: Emotion from outcomes.

## Abstract
One hundred participants viewed 10 randomly sampled wheel-spin outcomes and rated the player's emotions on eight 9-point Likert scales (happy, sad, angry, surprised, fearful, disgusted, content, disappointed). Fifty pre-generated scenarios combined 18 wheels with specific outcomes.

## Overview
- 50 wheel scenarios, each defining payoffs, sector probabilities, and the realized outcome.
- Each trial asks for eight discrete emotion ratings (1-9).
- Human-response data come from `expt1data.csv` (100 participants, 1000 trials).

## Directory Structure
- `trial.jsonl`: Text descriptions of wheel scenarios and the eight emotion queries.
- `config.json`: Metadata and randomized block flow.
- `instruction.jsonl`: Task instructions (consent screens removed).
- `human_data_ind.json` / `human_data_mean.json`: Trial-level responses aggregated by scenario.
- `assets/`: Empty (wheel animations were rendered dynamically in the original code).

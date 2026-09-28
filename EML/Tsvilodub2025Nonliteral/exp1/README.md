# Tsvilodub et al. (2025) Experiment 1: Price Inference (Task 1b only).

## Abstract
Participants read short price-related dialogues and provide the probability that the item has each of 10 specified prices (price inference). Responses are collected on continuous 0–100% sliders.

## Overview
- 30 text-only trials reconstructed from `experiment_1_full.csv`, each with 10 price questions (task_1b) from the original data. The affect question (task_1a) has been removed.
- Each trial presents a short dialogue (context, question, utterance) with 10 queries: 10 price sliders.
- One condition with **10 sequences**, each a balanced random 15-of-30 draw in its own random order. Every trial appears in exactly **5 of the 10** sequences, so each is shown to the same expected share of participants. This matches the design Kao et al. (2014) describe — "Each participant read 15 scenarios" (p.12006), 120 participants — **without** reproducing which particular 15 each of their participants happened to draw. It replaces an earlier encoding as two fixed between-subjects halves of the pool, which no participant ran.
- The authors' 120 real per-participant draws and orders *are* recoverable from `experiment1-raw.csv`, and were shipped as 120 enumerated sequences until 2026-08-14. They were replaced by balanced sampling deliberately: enumerating them reproduced the humans' accidental imbalance (some trials in 39% of sessions, others in 58%) without improving per-trial coverage. **Read the sequences as a sampling device, not as participants' sessions.**
- Human data are mapped from raw slider ratings in `experiment1-raw.csv` (Kao et al., 2014) and converted from 0-1 to 0-100 percentages. Not all participants saw all trials, so response arrays vary in length: **47–70 raters per trial**, summing to 1,800 presentations × 10 sliders = 18,000 = `judgment_count`. Those counts are the authors' own and are unaffected by the flow. Note the balanced flow does **not** predict them trial by trial — the enumerated-sessions encoding did, and that check (30 of 30 exact) is what established the design; see `reports/paper-check/`.

## Directory Structure
- `trial.jsonl`: Dialogue stimuli with price-probability sliders.
- `config.json`: Metadata and trial flow — one condition, 10 balanced sequences of 15 trials.
- `instruction.jsonl`: Prompt-style instructions adapted from `evaluation_0shot_1b_v3.txt` (first sentence verbatim), as in `exp3b/`. The original participant-facing wording from Kao et al. (2014) is not recoverable (`materials/experiment1.html` returns 404 live and in every Wayback capture).
- `human_data_ind.json` / `human_data_mean.json`: Mapped human responses with `state_prob_{price}` keys per trial.
- `assets/`: Empty (text-only stimuli).

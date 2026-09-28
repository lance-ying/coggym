# Tsvilodub et al. (2025) Experiment 3b: Affect prior judgments.

## Abstract
Participants read item price statements and estimate the probability that the buyer thinks the item is expensive. Responses are collected on a continuous 0–1 slider.

## Overview
- 30 text-only trials reconstructed from `experiment_3_full.csv`.
- One condition with **10 sequences**, each a balanced random 15-of-30 draw in its own random order. Every trial appears in exactly **5 of the 10** sequences. This matches the design Kao et al. (2014) describe — "Each participant read 15 scenarios" (p.12007), 30 participants — **without** reproducing which particular 15 each of their participants happened to draw. It replaces an earlier encoding of ten sequences each holding the **whole** 30-trial pool, which is the defect this correction fixes: a participant now sees half the pool, as the original did.
- The authors' 30 real draws and orders *are* recoverable from `experiment3b-raw.csv`, and were shipped as 30 enumerated sequences until 2026-08-14. Balanced sampling replaced them because enumerating them reproduced the humans' accidental imbalance (trials in 30%–70% of sessions) for no gain in coverage. **Read the sequences as a sampling device, not as participants' sessions.**
- The slider's upper anchor is **"absolutely certain"**, per Kao et al. p.12007, the authors' `evaluation_0shot_3b_v3.txt`, Table 1 of the paper, the excluded exp2 (now in `_drafts/`), and this experiment's own `instruction_01`. An earlier encoding carried "extremely likely", which is the anchor of Kao's *price* scales (Experiments 1 and 3a).
- **Stimulus text note.** The stimuli previously ended with an appended sentence, " A friend asked, 'Was it expensive?'", on all 30 screens; it has been removed. This is a maintainer decision, not a source-confirmed restoration: no surviving source either confirms or refutes that the original Experiment 3b screens carried it, because the linked materials page (`stanford.edu/~justinek/hyperbole-paper/materials/experiment3b.html`) returns 404 and all five Wayback Machine captures of that URL recorded a 404. The sentence borrows the Experiment 1/2 dialogue template from grid columns that this experiment's own prompt file leaves unused, and it is not verbatim from that template ("him" was dropped); the corrected stimuli match the shape Table 1 of the paper prints for Experiment 3b. If the materials page ever resurfaces, this is the edit to re-open.
- Human data are mapped from `experiment3b-raw.csv` (Kao et al., 2014) and converted from 0-1 to 0-100 percentages. Sharp-price rows are represented with the corresponding rounded state plus one (for example, rounded 500 with `sharp` is represented as 501), so all 30 converted trials have human data. **Raters per trial run 9–21**, summing to `judgment_count` 450. Those counts are the authors' own and are unaffected by the flow; the balanced flow does not predict them trial by trial, though the enumerated-sessions encoding did (30 of 30 exact) — see `reports/paper-check/`.

## Directory Structure
- `trial.jsonl`: Text stimuli and affect-prior sliders.
- `config.json`: Metadata and trial flow — one condition, 10 balanced sequences of 15 trials.
- `instruction.jsonl`: Prompt-style instructions derived from `evaluation_0shot_3b_v3.txt`.
- `human_data_ind.json` / `human_data_mean.json`: Mapped human responses for the converted trials.
- `assets/`: Empty (text-only stimuli).

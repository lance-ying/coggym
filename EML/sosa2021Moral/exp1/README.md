# Experiment 1 - Pairwise Moral Comparison

- **Stimuli:** 11 unique pairs of alien interactions (Blue agent, Green victim, and a Fireball hazard) rendered as short MP4 clips.
- **Task:** Participants watched both clips in a pair and judged where the Blue agent's action toward the Green was morally worse on a 6-point slider.
- **Participants:** 46 MTurk workers (mean age ≈ 34.5 years) rated every pair, yielding 506 judgments after quality control.
- **Data files:** `trial.jsonl` lists each canonical pair and the 6-point slider query. `human_data_ind.json` stores the flipped-corrected slider responses, while `human_data_mean.json` records the mean slider response for each trial.

All videos referenced in `trial.jsonl` are available locally under `assets/` as MP4 files copied from `moral_dynamics/videos/experiment1`.

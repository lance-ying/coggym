# Experiment 3 - Responsibility, Effort, and Causality Ratings

- **Stimuli:** 20 MP4 clips depicting a Blue agent, a Green victim, and an unseen Red hazard. Greens always collide with the Red, but the Blue's behavior varies.
- **Task:** Each participant rated a single query per clip using a 0-100 slider: responsibility, effort, a counterfactual question about whether the collision would have happened without Blue, or badness. Assignment to the four queries was between-subjects.
- **Participants:** 209 MTurk workers after bot-check exclusion (mean age ≈ 37.9 years); 55 answered responsibility, 51 rated effort, 51 answered the counterfactual question, and 52 rated badness, producing 4,180 total judgments.
- **Data files:** `trial.jsonl` lists the shared video stimuli and the four slider prompts. `human_data_ind.json` contains a slider array per prompt, populated only for participants who answered that question. `human_data_mean.json` reports the mean slider value for each metric.

All videos referenced in `trial.jsonl` are available under `assets/` as MP4 files copied from `moral_dynamics/videos/experiment3`.

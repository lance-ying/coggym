# Experiment 2 - Single Video Ratings

- **Stimuli:** 17 distinct MP4 clips showing a Blue agent, a Green agent, and Fireballs under different kinematic configurations.
- **Task:** Each participant watched one video at a time and used a 0-100 slider to rate either (a) how much effort the Blue exerted or (b) how bad the Blue's action was. Assignment to effort vs. badness was between-subjects but every clip appeared in both conditions.
- **Participants:** 83 MTurk workers (mean age ≈ 35.7 years); 42 rated effort and 41 rated moral badness, providing 1,411 total judgments.
- **Data files:** `trial.jsonl` defines the shared video stimuli and includes both slider prompts. `human_data_ind.json` stores two arrays per trial (`effort_rating` and `badness_rating`), with values populated only for the participants who saw that question. `human_data_mean.json` provides the mean slider value for each metric.

All videos referenced in `trial.jsonl` are available under `assets/` as MP4 files copied from `moral_dynamics/videos/experiment2`.

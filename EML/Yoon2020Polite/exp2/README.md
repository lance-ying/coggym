# Yoon et al. (2020) Experiment 2: Speaker Production Task.

## Abstract
Participants read scenarios describing a speaker's true evaluation of a product/performance (0-3 hearts) and a communicative goal (informative, kind, or both). They then predict what the speaker would say by selecting an utterance built from a negation choice ("was/wasn't") and an adjective (terrible/bad/good/amazing).

## Overview
- 51 trial definitions total: 3 practice trials plus 48 main condition-specific definitions covering 12 goal x state cells across four option-order conditions. Each experiment flow presents 12 main trials.
- Each session is three goal blocks of four trials, the blocks in a per-participant random order and the four states shuffled within each block, as in the original script (`goal_list = shuffle([goals1, goals2, goals3])`, `states1 = shuffle([...])`). Ten sequences per condition encode that randomization.
- Context items and speaker names were randomized per participant; this conversion instantiates representative contexts and names, held fixed across sequences (the trial *ordering* is not fixed — see above).
- The original response interface used two side-by-side categorical dropdowns: `was`/`wasn't` and `terrible`/`bad`/`good`/`amazing`. Four counterbalanced option-order conditions existed (`cond = random(4)+1`, drawn once per session), and are encoded here as the four between-participant conditions `ui_cond_1`-`ui_cond_4`; responses and human means are keyed to the visible option order for each condition-specific trial. A participant sees one layout for the whole session.
- The heart-state sentence reads "on a scale of 0 to 3:" where the original script wrote "on a scale of 0 to 3 hearts:"; the unit is carried instead by the appended "(N out of 3 hearts)" gloss, which the original did not display. A documented conversion adaptation, kept deliberately.
- Human data are derived from raw MTurk JSON files in `original_experiments/01_experiments/02_speaker_production/production-results/`, filtered to participants who passed the three practice checks (matching the preprocessing script). Practice judgments and option-order-invariant base aggregates are omitted from the human comparison data.

## Directory Structure
- `trial.jsonl`: 3 practice trials plus 48 condition-specific main trials with goal prompts and two categorical utterance-selection queries. The practice trials carry `role: "attention_check"` and the authors' own answer key (Yes/No/Yes): the original study kept only the 203 of 264 submissions that answered all three correctly, so they gated sample membership rather than being warm-ups. Substantive practice questions are stored in their response-query prompts, and each production question is a display-only query preceding the two categorical response queries.
- `config.json`: Metadata and experiment flow (instructions -> practice -> main trials), with four between-participant conditions of ten sequences each.
- `instruction.jsonl`: One instruction screen plus three practice test trials.
- `human_data_ind.json` / `human_data_mean.json`: Trial-level utterance-selection data for the condition-specific main trials; practice/test trials are omitted from the human comparison data.
- `assets/`: Empty (all stimuli are text-based in the original experiment).

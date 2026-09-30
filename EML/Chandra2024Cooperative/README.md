# Chandra et al. (2024) Cooperative Explanation as Rational Communication

## Abstract

Chandra et al. study how people select explanations for surprising actions in a route-planning domain. Participants reason about Alice and Bob moving through a neighborhood under different circumstances, identify Alice's quickest route, observe Bob question part of that route, and choose the statement or combination of statements that Alice should give in reply.

## Overview

- The paper reports one behavioral experiment containing 15 scenarios.
- Each participant completed nine rounds: scenarios 1–3 in fixed order, followed by six scenarios sampled without replacement from scenarios 4–15.
- Each converted round contains one self-contained explanation-selection trial. It states the circumstances, shows Alice's correct planned route, presents the comic sequence, and asks for Alice's explanation.
- The source's route-selection gate is omitted from the converted benchmark because it was a comprehension check rather than a target judgment, every participant had to pass it, and the released logs do not preserve usable route-choice responses.
- The 99 completed task records contain 95 unique scenario orders. Those 95 unique orders are encoded once each as `experimental_condition` flows without retaining Prolific IDs.
- All 96 rendered scenario images and the instruction map were copied byte-for-byte from the released experiment.

## Human-data provenance

The paper reports 100 recruited participants and five exclusions. The two final log files used by the released `fit.py` contain 99 completed records (30 in `log-reword-eve.jsonl` and 69 in `log.jsonl`). The released analysis criterion excludes any record with more than two incorrect route attempts in any round; this excludes eight records and leaves 91 participants. The converted human-data files use this reproducible 91-person subset. Age and gender were not collected in the released task; the consent screen establishes only that participants were at least 18 years old.

Across the 91 included participants, there are 819 explanation selections (91 participants × 9 rounds). Route selection is omitted from both the converted trial flow and the human benchmark data. The source required every participant to reach the correct route and did not retain the realized terminal option label, so it provides no meaningful model-versus-human response target. Each human-data file therefore contains 819 scored human judgments.

## Directory Structure

- `exp1/`: The cooperative-explanation benchmark, including all 15 scenarios, 95 unique observed flows, 75 self-contained explanation trials, human explanation responses, and all original visual assets.

Conversion-wide provenance, discrepancies, and renderer-level limitations are recorded in `../conversion_log.md` and `../conversion_report.md`.

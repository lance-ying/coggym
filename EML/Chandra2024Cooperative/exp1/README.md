# Chandra et al. (2024) Experiment 1: Route explanations

## Abstract

Participants planned the quickest route for Alice to take Bob to a convenience store under scenario-specific circumstances. After confirming the route, they viewed a short sequence in which Bob questioned Alice's movement and selected one or more statements for Alice to use as an explanation.

## Overview

- Fifteen scenario definitions were recovered directly from `tom.py`.
- Every participant saw scenarios 1–3 first and then six of the remaining twelve scenarios, sampled without replacement and shown in sampled order.
- Each round is represented by one self-contained `explanation_*` trial. It includes the round heading, circumstances, Alice's correct planned-route image, comic sequence, and explanation query.
- Scenario-by-round variants preserve the source's displayed `Round X of 9` heading. The 75 observed scenario/round combinations produce 75 response-bearing explanation trials.
- The original route-selection gate is intentionally excluded. It checked route understanding, forced every participant to reach the same correct outcome, and has no recoverable response target suitable for the human-versus-model benchmark.
- `config.json` contains the 95 unique anonymized observed-sequence conditions reconstructed from the 99 completed released-log records.

## Human data

The converted individual and mean files use the 91 records retained by the released `fit.py` filter (`num_wrong > 2` in any round causes exclusion). Participant identifiers, exit-survey answers, durations, and other non-experimental fields were not copied.

| Scenario | Included participants | Explanation judgments |
| ---: | ---: | ---: |
| 1 | 91 | 91 |
| 2 | 91 | 91 |
| 3 | 91 | 91 |
| 4 | 46 | 46 |
| 5 | 48 | 48 |
| 6 | 42 | 42 |
| 7 | 41 | 41 |
| 8 | 49 | 49 |
| 9 | 42 | 42 |
| 10 | 47 | 47 |
| 11 | 51 | 51 |
| 12 | 46 | 46 |
| 13 | 45 | 45 |
| 14 | 42 | 42 |
| 15 | 47 | 47 |
| **Total** | — | **819** |

`judgment_count` is 819: one explanation selection for each included round. Route selection is omitted from the converted flow and both human-data files. The original retry loop guaranteed that participants ultimately selected the correct route, while the released logs do not retain the realized terminal option label or the identities/order of earlier wrong choices. Two released explanation responses contain no checked statement and are preserved as all-zero multi-select vectors.

The paper reports 100 recruited participants and five exclusions, whereas the final logs contain 99 completed records and the released code excludes eight. The code-reproducible counts are used here. Age and gender are unavailable, so `age` is `null`, `gender` is an empty dictionary, and the known 18+ eligibility requirement is retained separately.

## Fidelity notes

- Each explanation trial shows the canonical correct `##-path.png` as Alice's planned route before the comic frames. This supplies the route context that all source participants had after passing the route check.
- The original route alternatives are static map images with no baked-in response widgets. They remain in `assets/` byte-for-byte for provenance, but the distractors are not referenced by the benchmark flow.
- The original explanation screen randomized the first four statement checkboxes while always leaving the “odd question” option last and mutually exclusive. The converted query retains whole-list randomization and adds an explicit instruction to the odd-question option not to select any other option with it. The raw data contain no response that combines that option with another statement.
- The source combined instructions and a four-checkbox quiz on one page and repeated the page until correct. HEML's comprehension-quiz schema supports `multi-choice`, not `multi-select`, so the four statements are rendered as four native true/false questions after the instruction page. The map remains on the preceding instruction screen, and both screens tell participants that they can return there to review it. Correct answers are retained; only the source-specific failure/re-display sequence is not reproduced literally.
- Consent, compensation/completion pages, the exit survey, and other non-experimental screens are omitted.
- No `supplementary.pdf` was present. No visual stimulus is missing.

## Directory Structure

- `trial.jsonl`: 75 self-contained explanation trials, preserving every observed scenario/round pairing.
- `config.json`: Metadata and 95 unique observed-sequence `experimental_condition` flows.
- `instruction.jsonl`: One general instruction module and one comprehension quiz. There are no instruction modules interleaved between regular trials.
- `human_data_ind.json`: Anonymized response vectors for the 91 code-included participants.
- `human_data_mean.json`: Explanation-option selection proportions.
- `assets/`: The instruction map and 96 original scenario images.

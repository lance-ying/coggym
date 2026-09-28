# Study 4: Belief Polarization Over Time

## Overview

Study 4 examines how shared observations of punishment affect belief polarization in experimental societies. Participants observe a sequence of punitive actions and report their evolving beliefs about the target and authority.

## Design

- **Type:** Between-subject with repeated measures
- **N:** 165 participants
- **Conditions:** Legitimate (52), Wrong (57), Not-wrong (56)

### Experimental Conditions

| Condition | Description |
|-----------|-------------|
| Legitimate | Target's behavior described as legitimate |
| Wrong | Target's behavior described as wrong |
| Not-wrong | Target's behavior described as not wrong |

### Observations

Each participant provided responses at 6 time points, in a fixed temporal order (observation 0 first, then 1 through 5 - nothing about this series is randomized):
- **Observation 0:** Prior beliefs (before any punitive action)
- **Observations 1-5:** After each of 5 consecutive daily observations. The authority punishes harshly on the first four; on the fifth it does nothing.

## Dependent Variables

| Variable | Scale | Measured At | Description |
|----------|-------|-------------|-------------|
| wrongness | 0-6 | All observations | Perceived wrongness of target's behavior |
| alpha_justice | 0-6 | All observations | Belief authority wants wrongdoing punished |
| alpha_target | 0-6 | Observation 5 only | Belief authority is biased against target |
| alpha_self | 0-6 | Observation 5 only | Belief authority seeks personal benefit |

## Key Findings

- Shared observations of punishment can curtail, sustain, or spread belief polarization
- In "Wrong + Just" societies, beliefs converge over time
- In "Wrong + Not-wrong" societies, beliefs diverge (polarization increases)
- The model predicts asymmetric belief updating based on prior beliefs

## Files

- `config.json` - Experiment configuration with 3 conditions × 6 observations
- `instruction.jsonl` - The condition instruction and the two comprehension-check items for each of the 3 conditions (9 modules)
- `trial.jsonl` - 42 trial definitions (3 conditions × 14 queries across observations)
- `human_data_ind.json` - Individual response metadata
- `human_data_mean.json` - Aggregated response metadata

## Original Data

Full data available at: `original_experiments/s5ydj/Version2/Data/formatted_data.csv`. Node `s5ydj` holds two complete runs of Study 4; the data, stimuli and instrument text shipped here are **Version 2**.

## Preregistration

[https://osf.io/kngu9](https://osf.io/kngu9)


## Author review (2026-08-25)

Setayesh Radkani, the paper's first author, reviewed the CogGym rendering and
supplied the original Qualtrics surveys for Study 1 and Study 4. The following
corrections were applied against those surveys as ground truth.

- **Scenario fragment page removed.** The flow opened with a bare page carrying
  one sentence of the scenario ("You hear that Paji has a strong sense of
  justice...") and then asked two comprehension questions with no scenario
  visible. That sentence is already part of every trial's scenario text, so the
  fragment screen and the two standalone quiz screens were removed.
- **Comprehension checks moved onto the prior-belief page**, alongside the
  wrongness and justice-motive questions, as in the original. They are excluded
  from scoring via `scoring_rules.json`.
- **Daily observations accumulate.** The original keeps every previous day in the
  scenario, so the Wednesday page shows Monday, Tuesday and Wednesday. CogGym
  replaced the observation each day. Verified against the survey: Monday appears
  on 5 pages, Tuesday on 4, Wednesday on 3, Thursday on 2, Friday on 1.
- **Prior prompt reworded** to the authors' *"What do you know so far?"*.
- **Instructions replaced with the authors' Study 4 text.**
- **Responses forced**, and the separate "I don't know" questions removed.

### Response scales, as surveyed

| Tag | Range | Labels |
|---|---|---|
| `wrongness` | 0–6 | Not at all wrong (0) · Extremely wrong (6) |
| `alpha_justice` | 0–6 | Not at all (0) · Extremely (6) |
| `alpha_self` | 0–6 | Not at all (0) · Extremely (6) |
| `alpha_target` | −3–3 | Strongly biased against (−3) · Neutral/treating equally (0) · Strongly biased in favor (3) |
| `harshness` | −3–3 | Too lenient (−3) · Proportional/fair (0) · Too harsh (3) |
| `U_target` | 0–6 | Not at all (0) · Very much (6) |
| `U_self` | −3–3 | Huge costs (−3) · No consequences (0) · Huge benefits (3) |

CogGym previously showed invented midpoints ("Moderately", "Moderate",
"Moderately wrong"), "Very much" in place of "Extremely" for `alpha_justice`,
"Not at all selfish"/"Extremely selfish" for `alpha_self`, and "Impartial" in
place of "Neutral/treating equally" for `alpha_target`.

### Analysis status

- Study 4's six waves form one cumulative observation sequence per condition.
  The EML is retained as a faithful study representation, but Study 4 is
  excluded from CogGym's standard independent-trial scatter/r² analysis.
- **Slider start position** (`default_value`) is left as-is. The original sets no
  start position on most sliders, so the knob is unplaced and a forced response
  is a real choice; whether CogGym should drop the default is a rendering
  question raised with the authors, not a verified defect.

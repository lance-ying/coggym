# Study 1: Prior Belief Manipulation

## Overview

Study 1 examines how prior beliefs about a target's wrongdoing influence observers' inferences from punishment. Using a strategy method design, participants provided judgments for all possible punitive actions under different prior belief conditions.

## Design

- **Type:** Within-subject, over 6 between-participant Latin-square arms (`latin_row_1` ... `latin_row_6`): every participant reads all 6 scenarios, one in each prior condition
- **N:** 358 participants
- **Age:** M = 39.88 years
- **Gender:** 194 male, 160 female, 4 other

### Experimental Conditions

| Condition | Description |
|-----------|-------------|
| No-info | No prior information about target's behavior |
| Wrong | Target's behavior was described as wrong |
| Not-wrong | Target's behavior was described as not wrong |
| Somewhat-wrong | Target's behavior was described as somewhat wrong |
| Legitimate | Target's behavior was described as legitimate |
| Illegitimate | Target's behavior was described as illegitimate |

### Actions

Each scenario is a four-page unit. The prior page comes first; the three punitive-response pages follow in a per-participant randomized order. Each participant responded to 4 action stages per scenario:
1. **Prior** - Before learning authority's action
2. **None** - Authority takes no action
3. **Mild** - Authority issues mild punishment
4. **Harsh** - Authority issues harsh punishment

## Dependent Variables

| Variable | Scale | Description |
|----------|-------|-------------|
| wrongness | 0-6 | Perceived wrongness of target's behavior |
| alpha_justice | 0-6 | Belief authority wants wrongdoing punished |
| alpha_target | 0-6 | Belief authority is biased against target |
| alpha_self | 0-6 | Belief authority seeks personal benefit |
| harshness | -3 to +3 | Perceived harshness of punishment |
| U_target | -6 to 0 | Utility to target from punishment |
| U_self | -6 to +6 | Utility to authority from punishment |

## Key Findings

- Prior beliefs systematically influence inferences about the authority's motivations
- When targets are believed to have done wrong, punishment is attributed more to justice
- When targets are believed innocent, punishment is attributed more to bias or self-interest
- The Bayesian inverse planning model accurately predicts these asymmetric inferences

## Files

- `config.json` - Experiment configuration: 6 Latin-square conditions × 4 actions, 10 enumerated orderings per condition
- `instruction.jsonl` - Task instructions for each condition and DV
- `trial.jsonl` - 24 trial definitions for Scenario 1 (6 conditions × 4 actions)
- `human_data_ind.json` - Individual response metadata
- `human_data_mean.json` - Aggregated response metadata

## Original Data

Human JSON is regenerated from the authors' analysis-ready
`formatted_data_2.csv`: https://osf.io/download/r5a3p/ (SHA-256
`93973f1d8663d842ee6d317a83bc976e9e7639075ab09dba14c0d7e330e85bde`).

## Preregistration

[https://osf.io/hjcrz](https://osf.io/hjcrz)


## Author review (2026-08-25)

Setayesh Radkani, the paper's first author, reviewed the CogGym rendering and
supplied the original Qualtrics surveys for Study 1 and Study 4. The following
corrections were applied against those surveys as ground truth.

- **Scenario framing restored per scenario.** The sentence *"Imagine you are
  traveling very far away, and meet a new group of people you know nothing
  about..."* opens every scenario in the original (it is a separate `*-scenario`
  block repeated for each one), which keeps the six societies independent. CogGym
  had hoisted it into the instructions and added *"In each scenario, you will read
  about two people in this society"*, implying one shared society with six
  comparable authorities — an inference the study does not intend.
- **Instructions replaced with the authors' text.** The original instruction
  covers slider mechanics, the "I don't know" option, scenario independence and
  the repeated-question warning. It does **not** name the dependent variables;
  CogGym's version listed all four in advance.
- **Action space restored on posterior trials.** Every scenario states the
  authority's full set of options ("could either do nothing, take away half...,
  or take away all..."). CogGym showed it only on the prior-belief trial and
  dropped it once the decision was revealed. Restored on all posterior trials.
- **Invented prior prompt removed.** *"Before you learn what X decided to do,
  please answer the following questions about your current beliefs:"* appears
  nowhere in the survey.
- **Scenario 4 text corrected.** The action is *"using a voca"*, not *"using a
  voca during the day"*, and the line *"People in this society have items called
  a 'voca'"* was not in the original.
- **Response scales corrected to the surveyed labels** (see table below).
- **Responses forced.** The original sets `ForceResponse: ON` on every rating;
  all queries were `required: false`.
- **Separate "I don't know" questions removed.** In the original this is an `NA`
  label on the slider itself, not an extra question per DV. The option is
  described in the instructions. These queries carried no human data.

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

### Human-data correction (2026-08-27)

- The human JSON was regenerated from the authors' public, analysis-ready
  `formatted_data_2.csv`, which is also the input to their
  `fit_joint_model_change.R` analysis. All four belief measures are now present
  for every prior row. The earlier `formatted_data_0.csv` conversion had
  partially masked prior columns and caused unequal point counts.
- The paper's primary comparison is **belief update** (posterior − matched
  scenario/condition prior), not posterior level. Model outputs produced before
  the corrected four-query prior pages must be rerun before reporting updated
  model–human r².
- **Slider start position** (`default_value`) is left as-is. The original sets no
  start position on most sliders, so the knob is unplaced and a forced response
  is a real choice; whether CogGym should drop the default is a rendering
  question raised with the authors, not a verified defect.

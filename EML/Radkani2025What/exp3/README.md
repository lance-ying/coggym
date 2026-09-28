# Study 3: Self-Consequences for Authority

## Overview

Study 3 examines how information about consequences to the authority from punishment influences observers' inferences. This study tests whether the authority's personal stake in the outcome affects attributions of selfishness.

## Design

- **Type:** 2×3, **within**-subject: each participant reads all 6 scenarios, one in each of the 6 conditions, over 6 Latin-square arms (`latin_row_1` ... `latin_row_6`)
- **N:** 361 participants
- **Age:** M = 38.2 years
- **Gender:** 175 male, 180 female, 6 other

### Experimental Factors

**Factor 1: Wrongness**
| Level | Description |
|-------|-------------|
| Wrong | Target's behavior described as wrong |
| Not-wrong | Target's behavior described as not wrong |

**Factor 2: Self-Consequences**
| Level | Description |
|-------|-------------|
| Cost | Punishment costs the authority |
| No-consequence | Punishment has no consequence for authority |
| Benefit | Punishment benefits the authority |

### Actions

Each scenario is a four-page unit. The prior page comes first; the three punitive-response pages follow in a per-participant randomized order. Each participant responded to 4 action stages:
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

- Self-consequences specifically affect attributions of selfishness (alpha_self)
- When punishment benefits the authority, selfishness attributions increase
- When punishment costs the authority, selfishness attributions decrease
- Prior beliefs about wrongness continue to influence justice attributions

## Files

- `config.json` - Experiment configuration: 6 Latin-square conditions (2×3), 10 enumerated orderings per condition
- `instruction.jsonl` - Task instructions for each condition
- `trial.jsonl` - 24 trial definitions for Scenario 1 (6 conditions × 4 actions)
- `human_data_ind.json` - Individual response metadata
- `human_data_mean.json` - Aggregated response metadata

## Original Data

Human JSON is regenerated from the authors' analysis-ready
`formatted_data_2.csv`: https://osf.io/download/79amz/ (SHA-256
`c54387509fea9d5c469ee2968f792f44e25a9e141586bee5583da1d4504997a4`).

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

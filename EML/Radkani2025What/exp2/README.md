# Study 2: Authority-Target Relationship

## Overview

Study 2 examines how information about the relationship between the authority and target influences observers' inferences from punishment. This study tests whether ally relationships reduce attributions of bias.

## Design

- **Type:** 3×3, with both factors varying **within** participant. Each participant sees all three relationship levels (twice each) and two of the three prior-information levels; the between-participant assignment is which six of the nine cells a participant receives, over 9 Latin-square arms (`latin_row_1` ... `latin_row_9`)
- **N:** 535 participants
- **Age:** M = 38.5 years
- **Gender:** 265 male, 262 female, 8 other

### Experimental Factors

**Factor 1: Prior Information**
| Level | Description |
|-------|-------------|
| Legitimate | Target's behavior described as legitimate |
| Wrong | Target's behavior described as wrong |
| No-info | No prior information provided |

**Factor 2: Authority-Target Relationship**
| Level | Description |
|-------|-------------|
| Ally | Authority and target are allies/friends |
| Neutral | No special relationship (baseline) |
| Competitor | Authority and target are competitors |

### Actions

Each participant responded to 3 action stages:
1. **Prior** - Before learning authority's action
2. **Mild** - Authority issues mild punishment
3. **Harsh** - Authority issues harsh punishment

## Dependent Variables

| Variable | Scale | Description |
|----------|-------|-------------|
| wrongness | 0-6 | Perceived wrongness of target's behavior |
| alpha_justice | 0-6 | Belief authority wants wrongdoing punished |
| alpha_target | 0-6 | Belief authority is biased against target |
| alpha_self | 0-6 | Belief authority seeks personal benefit |
| harshness | -3 to +3 | Perceived harshness of punishment |
| U_target | -6 to 0 | Utility to target from punishment |

## Key Findings

- Ally relationships reduce attributions of bias against the target
- Competitor relationships increase bias attributions
- Prior beliefs about wrongness continue to influence justice attributions
- The relationship manipulation specifically affects the alpha_target (bias) variable

## Files

- `config.json` - Experiment configuration: 9 Latin-square conditions (3×3), 10 enumerated orderings per condition
- `instruction.jsonl` - Task instructions for each condition
- `trial.jsonl` - 12 trial definitions for Scenario 1 (4 conditions × 3 actions)
- `human_data_ind.json` - Individual response metadata
- `human_data_mean.json` - Aggregated response metadata

## Original Data

Human JSON is regenerated from the authors' analysis-ready
`formatted_data_2.csv`: https://osf.io/download/5swdn/ (SHA-256
`f590b0bd66a85e7fa9640766041d0921e057586c4a777512044e5582edf4a51e`).

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

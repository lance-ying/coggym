# Radkani2025What

## What people learn from punishment: A cognitive model

**Authors:** Amir Radkani, Joshua B. Tenenbaum, Rebecca Saxe

**Journal:** Proceedings of the National Academy of Sciences (PNAS), 2025

**DOI:** [10.1073/pnas.2500730122](https://doi.org/10.1073/pnas.2500730122)

**Preregistration:** [https://osf.io/hjcrz](https://osf.io/hjcrz) (Studies 1-3), [https://osf.io/kngu9](https://osf.io/kngu9) (Study 4)

---

## Overview

This dataset contains four preregistered behavioral experiments (N=1,410 total participants) investigating how observers make inferences about agents' moral character and motivations from observations of punishment. The studies test a computational model based on Bayesian inverse planning that captures how people learn about:

1. **The target's wrongness** - Whether the punished person deserved punishment
2. **The authority's motivations** - Whether the authority was motivated by justice, bias against the target, or self-interest

The key finding is that the same punitive action can lead observers to draw different inferences depending on their prior beliefs about the target's wrongness.

---

## Experimental Structure

### Study 1 (exp1): Prior Belief Manipulation
- **N = 358 participants**
- **Design:** Within-subject, 6 prior conditions (No-info, Wrong, Not-wrong, Somewhat-wrong, Legitimate, Illegitimate) × 4 action stages (Prior, None, Mild, Harsh)
- **Original folder:** nxswy
- **Key finding:** Prior beliefs about the target's wrongness systematically influence inferences about the authority's motivations

### Study 2 (exp2): Authority-Target Relationship
- **N = 535 participants**
- **Design:** 3×3 crossing of prior information (Legitimate, Wrong, No-info) × authority-target relationship (Ally, Neutral, Competitor). Both factors vary **within** participant — each participant sees all three relationship levels (twice each) and two of the three prior-information levels; the between-participant assignment is *which* six of the nine cells a participant receives, over nine Latin-square arms
- **Original folder:** p3t42
- **Key finding:** Relationship information affects bias attributions, with punishment of allies seen as more justice-motivated

### Study 3 (exp3): Self-Consequences for Authority
- **N = 361 participants**
- **Design:** 2×3 crossing of wrongness (Wrong, Not-wrong) × self-consequences (Cost, No-consequence, Benefit). **Within**-subject: each participant reads all six scenarios, one in each of the six conditions, over six Latin-square arms
- **Original folder:** tj7zp
- **Key finding:** Information about consequences to the authority affects attributions of self-interest

### Study 4 (exp4): Belief Polarization Over Time
- **N = 165 participants** (Legitimate 52, Wrong 57, Not-wrong 56)
- **Design:** Between-subject, 3 prior conditions (Legitimate, Wrong, Not-wrong) × 6 observations, presented in a fixed temporal order (observation 0 = prior beliefs, then observations 1-5)
- **Original folder:** s5ydj, **Version 2** (the run whose data and stimuli this dataset ships; node s5ydj holds two complete runs)
- **Key finding:** Shared observations of punishment can curtail, sustain, or spread belief polarization depending on initial beliefs

---

## Dependent Variables

All studies measure some subset of the following variables:

| Variable | Scale | Description |
|----------|-------|-------------|
| `wrongness` | 0-6 | Perceived wrongness of target's behavior |
| `alpha_justice` | 0-6 | Authority's desire for wrongdoing to be punished |
| `alpha_target` | 0-6 | Authority's desire for target to suffer (bias) |
| `alpha_self` | 0-6 | Authority's desire for personal benefit (selfishness) |
| `harshness` | -3 to +3 | Perceived harshness of punishment |
| `U_target` | -6 to 0 | Utility to target from punishment |
| `U_self` | -6 to +6 | Utility to authority from punishment |

**Note:** "I don't know" responses were scored at each scale's midpoint.

---

## File Structure

```
Radkani2025What/
├── README.md                  # This file
├── exp1/                      # Study 1
│   ├── config.json           # Experiment configuration
│   ├── instruction.jsonl     # Task instructions
│   ├── trial.jsonl           # Trial definitions
│   ├── human_data_ind.json   # Individual responses metadata
│   ├── human_data_mean.json  # Aggregated responses metadata
│   └── README.md             # Study-specific details
├── exp2/                      # Study 2
│   └── [same structure]
├── exp3/                      # Study 3
│   └── [same structure]
└── exp4/                      # Study 4
    └── [same structure]
```

---

## Scenarios

All studies used 6 workplace scenarios involving authority figures and targets:
1. Manager and employee (expense reports)
2. Supervisor and worker (project deadlines)
3. Director and staff (resource allocation)
4. Executive and subordinate (policy violations)
5. Administrator and team member (compliance)
6. Coordinator and colleague (procedural adherence)

Each scenario followed the same structure: a target commits a potentially ambiguous act, the observer receives prior information about the act's wrongness, and an authority figure takes one of three possible actions (none, mild punishment, harsh punishment).

---

## CogGym Format

This dataset has been converted to the CogGym HEML (Human Experiment Markup Language) format for LLM evaluation benchmarking. Each experiment folder contains:

- **config.json**: Experiment metadata, conditions, and flow structure
- **instruction.jsonl**: Task instructions and condition descriptions
- **trial.jsonl**: Individual trial definitions with query types and response scales
- **human_data_ind.json**: Metadata about individual participant responses
- **human_data_mean.json**: Metadata about aggregated mean responses

---

## Known departures from the deployed studies

Named here rather than left silent, because the EML flows cannot encode them:

- **The attention-check screen is not encoded (exp1, exp2, exp3).** The deployed surveys placed a slider attention check ("...Please put the slider knob below on 'I am a real person!'") randomly among the six scenario units. Its prompt and its placement rule are recoverable from the authors' exports, but its response scale is not - the export records only the selected value - so restoring it would mean inventing a scale. Omitted deliberately, not accidentally.
- **The comprehension gate's exclusion rule is not encoded (exp4).** The two comprehension items are present with correct answer keys and their preregistered option randomization, but the preregistration's "exclude the data from participants who respond otherwise" (enforced in the authors' `preprocess_data_0.R`) has no EML expression: nothing in the format gates progression on a quiz answer.
- **Exp. 1--3 human responses were regenerated from the authors' analysis-ready
  `formatted_data_2.csv` files (2026-08-27).** The earlier conversion used
  `formatted_data_0.csv`, where prior responses are partially masked. The
  replacement files are the inputs used by the paper's own belief-update
  analysis and retain all four prior-belief judgments for every prior row.
  The public source URLs and verified SHA-256 digests are recorded in the
  experiment READMEs.
- **Exp. 4 is represented but excluded from CogGym's independent-trial
  benchmark analysis.** Its observations form a cumulative sequence, so its
  waves are not exchangeable independent trials.

---

## Citation

```bibtex
@article{radkani2025what,
  title={What people learn from punishment: A cognitive model},
  author={Radkani, Amir and Tenenbaum, Joshua B and Saxe, Rebecca},
  journal={Proceedings of the National Academy of Sciences},
  volume={122},
  number={32},
  pages={e2500730122},
  year={2025},
  publisher={National Acad Sciences},
  doi={10.1073/pnas.2500730122}
}
```

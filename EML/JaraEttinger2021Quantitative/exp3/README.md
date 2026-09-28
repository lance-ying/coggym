# Jara-Ettinger & Rubio-Fernandez (2021) Experiment 3: Joint inferences with real-world objects.

## Abstract
Two hundred Mechanical Turk participants (mean age 37.63 years, 50 per list) played a coordination game with a virtual partner. Participants saw a 2×2 grid of real-world object photographs, with one object enclosed in a black square (the partner may or may not be able to see it). The partner gave an instruction like "Select the [object]" and participants selected the intended referent and rated (0–10) their certainty that the partner knew about the boxed object. Three types of linguistic modification were tested: color (e.g., "the red watch"), category (e.g., "the dalmatian"), and size (e.g., "the small suitcase"), each in four variants: Direct (A), Indirect (B), Contrastive (C), and Ambiguous (D).

## Overview
- Forty-eight unique trial types: 16 color, 16 category, 16 size (4 variants each).
- Four lists of 12 trials each (Latin-square counterbalancing), with each list containing one variant of each item.
- Two responses per trial: referent selection (multi-choice: TL/TR/BL/BR) and knowledge inference (0–10 slider).
- Each trial includes a photograph of the 2×2 object display.

## Directory Structure
- `trial.jsonl`: 48 trial definitions, each with an image stimulus and text description, plus two queries.
- `config.json`: Metadata and experiment flow with four experimental conditions (List_1 through List_4).
- `instruction.jsonl`: 3 instruction pages and one comprehension quiz with 3 questions.
- `human_data_ind.json` / `human_data_mean.json`: Individual and mean responses (50 participants per trial, pooled across lists for shared trials).
- `assets/`: 48 stimulus photographs (JPG) of 2×2 object displays.

## Conversion Notes
- Stimulus images were copied from the original experiment's stimuli directory. Some filenames use `.JPG` and others `.jpg` (case preserved).
- Referent responses are encoded as `multi-choice` with options ["Top-left", "Top-right", "Bottom-left", "Bottom-right"].
- Knowledge inference uses a `single-slider` with min=0, max=10, labels at 0 ("Definitely not"), 5 ("Maybe"), and 10 ("Definitely").
- Two raw data rows had empty Inference values; their referent selections were excluded while their available knowledge ratings were retained, resulting in 4,798 total judgments (vs. 4,800 expected).
- The computed mean age (37.79) differs slightly from the paper-reported value (37.63), likely due to one missing age entry in the demographics file.

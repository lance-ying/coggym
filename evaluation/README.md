# CogGym evaluation

This folder contains the standalone code needed to turn the public EML
experiments into model prompts, call a model, parse its structured responses,
and compare its judgments with the released human means.

## Install

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r evaluation/requirements.txt
```

The included provider uses the Google GenAI SDK. Put credentials in the
environment, never in the repository:

```bash
export GOOGLE_API_KEY='...'
```

For Vertex AI, set `GOOGLE_CLOUD_PROJECT` and adapt provider construction in
`evaluation/cli.py` to pass `vertexai=True`.

## Inspect the release

```bash
# List all packaged experiments.
python -m evaluation.run_models --list

# Render the prompts for one experiment without making API calls.
python -m evaluation.run_models \
  --experiment JaraEttinger2021Quantitative/exp2 \
  --dry-run
```

`public_manifest.json` is the experiment allowlist. `trial_selection_map.json`
fixes the trial subset used for comparable runs. The runner applies that map by
default and stops if an experiment or selected trial is missing. Use
`--all-trials` only for a deliberately different analysis.

## Run a model

```bash
python -m evaluation.run_models \
  --experiment JaraEttinger2021Quantitative/exp2 \
  --model gemini-2.5-flash \
  --temperature 1.0 \
  --repetitions 5 \
  --output-dir results/gemini-2.5-flash
```

Omit `--experiment` to run the complete public set, or pass `--study` to run
one study. A full run can be expensive: always inspect prompts with `--dry-run`
and start with one experiment.

The provider-specific surface is intentionally small. To add another provider,
implement `complete_with_metadata()` with this return shape and pass it through
the same prompt/parser/scorer pipeline:

```python
{
    "text": response_text,
    "reasoning": None,
    "token_usage": {
        "input_tokens": None,
        "output_tokens": None,
        "thinking_tokens": None,
        "total_tokens": None,
    },
}
```

Preserve the text and media parts produced by `build_messages()`. Do not replace
video with a still image or omit other stimulus modalities.

The prompt builder follows each exact `experimentFlow` sequence and includes
only instruction modules that occur before the current trial. Presentation-only
pages can remain visible to human participants while being excluded from model
prompts by setting `"include_in_model_prompt": false` on that instruction in
`instruction.jsonl`. The field defaults to `true` when omitted.

## Analyze runs

```bash
python -m evaluation.analyze results/gemini-2.5-flash \
  --output-dir analysis/gemini-2.5-flash
```

The analyzer:

1. averages repeated model responses for each item;
2. keeps response regimes and scales separate during normalization;
3. computes Pearson R² for each experiment; and
4. reports the arithmetic mean of experiment-level R² values by modality.

It writes `experiment_r2.csv` and `summary.json`. Experiments with fewer than
five scorable item-level pairs are excluded by default; change this with
`--min-items`.

## Validate the package

Before publishing or modifying the release, run:

```bash
python -m evaluation.validate_package
python -m unittest discover -s evaluation/tests -v
```

The validator checks that the EML tree exactly matches the public manifest,
every selected trial and referenced media file exists, and no individual human
responses, paper PDFs, macOS sidecar files, or embedded credentials are present.

## Files

- `run_models.py` / `cli.py`: command-line model runner.
- `experiment.py`: EML loading and experiment-flow resolution.
- `prompt_builder.py`: prompt and media construction.
- `providers.py`: Gemini adapter and retry handling.
- `response_parser.py`: structured response parsing.
- `scorer.py`: item-level comparison with human means.
- `reporter.py`: immediate per-run diagnostics.
- `analyze.py`: repeated-run aggregation and public-set R² analysis.
- `public_manifest.json`: exact public experiment allowlist.
- `trial_selection_map.json`: fixed trial selection used for comparable runs.

## Reproducibility and privacy

The public package includes aggregate human means but not individual participant
responses. Raw model outputs may contain sensitive provider metadata or model
text; review them before sharing. API keys must remain in environment variables
or ignored local files.

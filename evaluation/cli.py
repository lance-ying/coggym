"""CLI for running single experiments interactively."""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any

from .experiment import Experiment, discover_experiments, load_experiment
from .prompt_builder import build_messages
from .response_parser import parse_response
from .scorer import score_trial
from .reporter import aggregate_experiment


def _list_experiments(processed_dir: Path) -> None:
    experiments = discover_experiments(processed_dir)
    print(f"\nFound {len(experiments)} experiments:\n")

    by_study: dict[str, list[Experiment]] = {}
    for exp in experiments:
        by_study.setdefault(exp.study, []).append(exp)

    for study in sorted(by_study):
        for exp in by_study[study]:
            types = ", ".join(exp.response_types)
            print(f"  {exp.full_name:<50} [{types}]  ({exp.stimuli_count} stimuli)")

    print(f"\n  Total: {len(experiments)} experiments across {len(by_study)} studies")


def _dry_run(experiment: Experiment, trials: list[Any]) -> None:
    print(f"\n=== DRY RUN: {experiment.full_name} ===")
    print(f"  Trials: {len(trials)}, Types: {', '.join(experiment.response_types)}")
    print()

    for i, trial in enumerate(trials[:3]):
        system, messages = build_messages(trial, experiment)
        if i == 0:
            print("--- SYSTEM PROMPT ---")
            print(system)
            print()

        print(f"--- TRIAL {trial.id} ---")
        content = messages[0]["content"]
        if isinstance(content, str):
            print(content[:500])
        elif isinstance(content, list):
            for part in content:
                if part.get("type") == "text":
                    print(part["text"][:500])
                elif part.get("type") == "video":
                    print(f"  [VIDEO: {part.get('path', '?')}]")
                else:
                    print(f"  [IMAGE]")
        print()

    if len(trials) > 3:
        print(f"  ... and {len(trials) - 3} more trials")


def _run_experiment(
    experiment: Experiment,
    trials: list[Any],
    provider: Any,
    model: str,
    temperature: float,
    max_tokens: int,
) -> list[dict[str, Any]]:
    from .providers import call_with_retry

    results: list[dict[str, Any]] = []

    for i, trial in enumerate(trials):
        system, messages = build_messages(trial, experiment)

        try:
            result = call_with_retry(
                provider, system, messages, model,
                temperature=temperature, max_tokens=max_tokens,
                with_metadata=True,
            )
            resp_text = result["text"]
            parsed = parse_response(resp_text, trial.queries)
            scores = score_trial(parsed, trial, experiment)

            entry = {
                "trial_id": trial.id,
                "condition": trial.condition,
                "response": resp_text,
                "reasoning": result["reasoning"],
                "token_usage": result["token_usage"],
                "parsed": parsed,
                "scores": scores,
                "model": model,
            }
            results.append(entry)

            # Progress
            r_info = ""
            for tag, s in scores.items():
                if s.get("scorable"):
                    if "normalized_error" in s:
                        r_info += f" nerr={s['normalized_error']:.3f}"
                    elif "cosine_similarity" in s and s["cosine_similarity"] is not None:
                        r_info += f" cos={s['cosine_similarity']:.3f}"
            print(f"  [{i+1}/{len(trials)}] {trial.id}{r_info}")

        except Exception as e:
            print(f"  [{i+1}/{len(trials)}] {trial.id}  ERROR: {e}")
            results.append({"trial_id": trial.id, "error": str(e)[:300], "model": model})

        time.sleep(0.3)

    return results


def _load_selection_map(path: Path | None) -> dict[str, Any]:
    if path is None:
        return {}
    with path.open() as handle:
        return json.load(handle)


def _selected_trials(
    experiment: Experiment,
    selection_map: dict[str, Any],
    use_all_trials: bool,
) -> list[Any]:
    trials = experiment.experiment_trials()
    if use_all_trials:
        return trials

    selection = selection_map.get(experiment.full_name)
    if selection is None:
        raise ValueError(
            f"{experiment.full_name} is missing from the selection map; "
            "use --all-trials only if this is intentional"
        )

    selected_ids = selection.get("selected_ids", [])
    by_id = {trial.id: trial for trial in trials}
    missing = [trial_id for trial_id in selected_ids if trial_id not in by_id]
    if missing:
        preview = ", ".join(missing[:5])
        raise ValueError(
            f"{experiment.full_name}: {len(missing)} selected trial IDs are missing "
            f"from the EML ({preview})"
        )
    return [by_id[trial_id] for trial_id in selected_ids]


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="CogGym Harness — Run Gemini on cognitive science experiments",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  python -m evaluation.run_models --list
  python -m evaluation.run_models --experiment JaraEttinger2021Quantitative/exp2 --dry-run
  python -m evaluation.run_models --experiment JaraEttinger2021Quantitative/exp2 --model gemini-2.5-flash
  python -m evaluation.run_models --study JaraEttinger2021Quantitative --model gemini-2.5-flash
""",
    )

    parser.add_argument("--list", action="store_true", help="List all experiments and exit")
    parser.add_argument("--experiment", type=str, help="Single experiment path (e.g. study/exp1)")
    parser.add_argument("--study", type=str, help="Filter to a single study")
    parser.add_argument("--response-type", type=str, help="Filter by response type")
    parser.add_argument("--task-type", type=str, help="Filter by task type")
    parser.add_argument("--model", type=str, default="gemini-3-flash-preview", help="Gemini model name")
    parser.add_argument("--temperature", type=float, default=1.0, help="Sampling temperature (default: 1.0)")
    parser.add_argument("--max-tokens", type=int, default=512, help="Max response tokens (default: 512)")
    parser.add_argument("--dry-run", action="store_true", help="Preview prompts without calling API")
    parser.add_argument("--max-experiments", type=int, help="Limit number of experiments")
    parser.add_argument("--repetitions", type=int, default=1, help="Independent runs per trial (default: 1)")
    parser.add_argument("-o", "--output-dir", type=str, default="results", help="Output directory")
    parser.add_argument("--eml-dir", type=str, default="EML", help="EML experiments root")
    parser.add_argument(
        "--selection-map",
        type=str,
        default=str(Path(__file__).with_name("trial_selection_map.json")),
        help="Canonical trial selection map",
    )
    parser.add_argument(
        "--all-trials",
        action="store_true",
        help="Ignore the canonical selection map and evaluate every experimental trial",
    )

    args = parser.parse_args(argv)
    processed_dir = Path(args.eml_dir)
    output_dir = Path(args.output_dir)
    selection_map = _load_selection_map(None if args.all_trials else Path(args.selection_map))

    if args.repetitions < 1:
        parser.error("--repetitions must be at least 1")

    if args.list:
        _list_experiments(processed_dir)
        return

    if args.experiment:
        parts = args.experiment.strip("/").split("/")
        if len(parts) != 2:
            print(f"Error: --experiment must be 'study/expN', got {args.experiment!r}")
            sys.exit(1)
        exp_dir = processed_dir / parts[0] / parts[1]
        experiments = [load_experiment(exp_dir)]
    else:
        experiments = discover_experiments(
            processed_dir, filter_study=args.study,
            filter_response_type=args.response_type, filter_task_type=args.task_type,
        )

    if not experiments:
        print("No experiments found.")
        sys.exit(1)
    if args.max_experiments:
        experiments = experiments[: args.max_experiments]

    if args.dry_run:
        for exp in experiments:
            _dry_run(exp, _selected_trials(exp, selection_map, args.all_trials))
        return

    from .providers import GeminiProvider

    provider = GeminiProvider()
    model = args.model
    print(f"Model: {model}, Experiments: {len(experiments)}")

    for exp_i, experiment in enumerate(experiments):
        trials = _selected_trials(experiment, selection_map, args.all_trials)
        print(f"\n[{exp_i+1}/{len(experiments)}] {experiment.full_name} ({len(trials)} trials)")

        for repetition in range(1, args.repetitions + 1):
            if args.repetitions > 1:
                print(f"  Repetition {repetition}/{args.repetitions}")
            trial_results = _run_experiment(
                experiment, trials, provider, model, args.temperature, args.max_tokens
            )
            summary = aggregate_experiment(trial_results)

            safe_name = experiment.full_name.replace("/", "_")
            safe_model = model.replace("/", "_")
            output_dir.mkdir(parents=True, exist_ok=True)
            output_path = output_dir / (
                f"{safe_name}_{safe_model}_run-{repetition:03d}.json"
            )
            with output_path.open("w") as handle:
                json.dump(
                    {
                        "model": model,
                        "experiment": experiment.full_name,
                        "repetition": repetition,
                        "temperature": args.temperature,
                        "max_tokens": args.max_tokens,
                        "selection_map": None if args.all_trials else str(args.selection_map),
                        "summary": summary,
                        "trials": trial_results,
                    },
                    handle,
                    indent=2,
                )

            r = summary.get("cross_trial_pearson_r")
            print(
                f"  Summary: {summary.get('n_scorable_queries', 0)} scored"
                + (f", r={r:+.3f}" if r is not None else "")
                + f" -> {output_path}"
            )


if __name__ == "__main__":
    main()

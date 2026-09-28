"""Aggregate CogGym model runs and compute per-experiment Pearson R².

The runner writes one JSON artifact per experiment and repetition. This script
averages repeated model responses at the item level, normalizes incompatible
response scales within an experiment, computes one R² per experiment, and then
reports the arithmetic mean of experiment-level R² values by modality.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import statistics
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable


def _pearson_r2(xs: list[float], ys: list[float]) -> float | None:
    if len(xs) < 3:
        return None
    mx, my = statistics.mean(xs), statistics.mean(ys)
    sx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    sy = math.sqrt(sum((y - my) ** 2 for y in ys))
    if sx == 0 or sy == 0:
        return None
    r = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / (sx * sy)
    return r * r


def _artifact_paths(inputs: Iterable[Path]) -> list[Path]:
    paths: set[Path] = set()
    for item in inputs:
        if item.is_file():
            paths.add(item)
        elif item.is_dir():
            paths.update(item.rglob("*.json"))
        else:
            raise FileNotFoundError(item)
    return sorted(paths)


def _load_query_metadata(eml_root: Path, experiment: str) -> dict[tuple[str, str], dict[str, Any]]:
    trial_path = eml_root / experiment / "trial.jsonl"
    metadata: dict[tuple[str, str], dict[str, Any]] = {}
    with trial_path.open() as handle:
        for line in handle:
            if not line.strip():
                continue
            trial = json.loads(line)
            for query in trial.get("queries", []):
                tag = query.get("tag", "")
                slider = query.get("slider_config") or {}
                metadata[(trial["id"], tag)] = {
                    "type": query.get("type"),
                    "scale_min": slider.get("min"),
                    "scale_max": slider.get("max"),
                    "n_options": len(query.get("option", [])),
                }
    return metadata


def _append_pair(
    store: dict[str, dict[str, list[float]]],
    item_key: str,
    model_value: Any,
    human_value: Any,
) -> None:
    try:
        model_float = float(model_value)
        human_float = float(human_value)
    except (TypeError, ValueError):
        return
    store[item_key]["model"].append(model_float)
    store[item_key]["human"].append(human_float)


def _collect_score(
    groups: dict[str, dict[str, Any]],
    trial_id: str,
    tag: str,
    score: dict[str, Any],
    query_meta: dict[str, Any],
) -> None:
    query_type = query_meta.get("type") or "unknown"
    scale_min = query_meta.get("scale_min")
    scale_max = query_meta.get("scale_max")
    n_options = query_meta.get("n_options") or 0

    if score.get("model_value") is not None and score.get("human_mean") is not None:
        group_key = f"{query_type}:{tag}:{scale_min}:{scale_max}"
        group = groups[group_key]
        group["bounds"] = [scale_min, scale_max]
        _append_pair(group["items"], f"{trial_id}___{tag}", score["model_value"], score["human_mean"])
        return

    if score.get("model_values") and score.get("human_means"):
        group_key = f"multi-slider:{tag}:{scale_min}:{scale_max}"
        group = groups[group_key]
        group["bounds"] = [scale_min, scale_max]
        for option, model_value in score["model_values"].items():
            if option in score["human_means"]:
                _append_pair(
                    group["items"],
                    f"{trial_id}___{tag}___{option}",
                    model_value,
                    score["human_means"][option],
                )
        return

    if score.get("model_binary") is not None and score.get("human_proportions") is not None:
        group_key = f"multi-select:{tag}"
        group = groups[group_key]
        group["bounds"] = [0.0, 1.0]
        for index, (model_value, human_value) in enumerate(
            zip(score["model_binary"], score["human_proportions"])
        ):
            _append_pair(
                group["items"], f"{trial_id}___{tag}___{index}", model_value, human_value
            )
        return

    if score.get("model_choice_index") is not None and score.get("human_distribution") is not None:
        group_key = f"choice:{tag}"
        group = groups[group_key]
        group["bounds"] = [0.0, 1.0]
        choice = int(score["model_choice_index"])
        for index, human_value in enumerate(score["human_distribution"]):
            _append_pair(
                group["items"],
                f"{trial_id}___{tag}___{index}",
                1.0 if index == choice else 0.0,
                human_value,
            )
        return

    if score.get("model_ranks") and score.get("human_mean_ranks"):
        group_key = f"ranking:{tag}"
        group = groups[group_key]
        group["bounds"] = [1.0, float(max(n_options, 2))]
        for option, model_value in score["model_ranks"].items():
            if option in score["human_mean_ranks"]:
                _append_pair(
                    group["items"],
                    f"{trial_id}___{tag}___{option}",
                    model_value,
                    score["human_mean_ranks"][option],
                )


def _normalize_group(group: dict[str, Any]) -> tuple[list[float], list[float]]:
    pairs = []
    for values in group["items"].values():
        if values["model"] and values["human"]:
            pairs.append((statistics.mean(values["model"]), statistics.mean(values["human"])))
    if not pairs:
        return [], []

    lower, upper = group.get("bounds", [None, None])
    if lower is None or upper is None or upper == lower:
        human_values = [human for _, human in pairs]
        lower, upper = min(human_values), max(human_values)
        if upper == lower:
            return [], []

    width = float(upper) - float(lower)
    model = [(value - float(lower)) / width for value, _ in pairs]
    human = [(value - float(lower)) / width for _, value in pairs]
    return model, human


def analyze(
    artifacts: list[Path],
    eml_root: Path,
    manifest_path: Path,
    min_items: int,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[str]]:
    manifest = json.loads(manifest_path.read_text())
    release = {entry["path"]: entry for entry in manifest["experiments"]}
    metadata_cache: dict[str, dict[tuple[str, str], dict[str, Any]]] = {}
    data: dict[str, dict[str, dict[str, dict[str, Any]]]] = defaultdict(
        lambda: defaultdict(lambda: defaultdict(lambda: {"bounds": [None, None], "items": defaultdict(lambda: {"model": [], "human": []})}))
    )
    artifact_counts: dict[tuple[str, str], int] = defaultdict(int)
    skipped: list[str] = []

    for path in artifacts:
        try:
            artifact = json.loads(path.read_text())
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            skipped.append(f"{path}: invalid JSON ({exc})")
            continue
        model = artifact.get("model")
        experiment = artifact.get("experiment")
        trials = artifact.get("trials")
        if not model or experiment not in release or not isinstance(trials, list):
            continue

        if experiment not in metadata_cache:
            metadata_cache[experiment] = _load_query_metadata(eml_root, experiment)
        query_metadata = metadata_cache[experiment]
        artifact_counts[(model, experiment)] += 1

        for trial in trials:
            trial_id = trial.get("trial_id", "")
            for tag, score in trial.get("scores", {}).items():
                if not score.get("scorable"):
                    continue
                meta = query_metadata.get((trial_id, tag), {})
                _collect_score(data[model][experiment], trial_id, tag, score, meta)

    rows: list[dict[str, Any]] = []
    for model in sorted(data):
        for experiment in sorted(data[model]):
            model_values: list[float] = []
            human_values: list[float] = []
            used_groups = 0
            for group in data[model][experiment].values():
                group_model, group_human = _normalize_group(group)
                if group_model:
                    used_groups += 1
                    model_values.extend(group_model)
                    human_values.extend(group_human)
            value = _pearson_r2(model_values, human_values) if len(model_values) >= min_items else None
            rows.append(
                {
                    "model": model,
                    "experiment": experiment,
                    "modality": release[experiment].get("modality"),
                    "r2": value,
                    "n_items": len(model_values),
                    "n_response_groups": used_groups,
                    "n_artifacts": artifact_counts[(model, experiment)],
                }
            )

    by_modality: dict[tuple[str, str], list[float]] = defaultdict(list)
    for row in rows:
        if row["r2"] is not None:
            by_modality[(row["model"], row["modality"])].append(row["r2"])
    summary = [
        {
            "model": model,
            "modality": modality,
            "mean_r2": statistics.mean(values),
            "n_experiments": len(values),
        }
        for (model, modality), values in sorted(by_modality.items())
    ]
    return rows, summary, skipped


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Analyze CogGym model-run artifacts")
    parser.add_argument("inputs", nargs="+", type=Path, help="Run JSON file(s) or directories")
    parser.add_argument("--eml-dir", type=Path, default=Path("EML"))
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path(__file__).with_name("public_manifest.json"),
    )
    parser.add_argument("--min-items", type=int, default=5)
    parser.add_argument("--output-dir", type=Path, default=Path("analysis"))
    args = parser.parse_args(argv)

    artifacts = _artifact_paths(args.inputs)
    rows, summary, skipped = analyze(artifacts, args.eml_dir, args.manifest, args.min_items)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    csv_path = args.output_dir / "experiment_r2.csv"
    fields = ["model", "experiment", "modality", "r2", "n_items", "n_response_groups", "n_artifacts"]
    with csv_path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    json_path = args.output_dir / "summary.json"
    json_path.write_text(
        json.dumps(
            {
                "method": "Mean repeated model responses by item; normalize response groups; compute Pearson R² per experiment; average experiment R² by modality.",
                "min_items": args.min_items,
                "artifacts_scanned": len(artifacts),
                "experiments": rows,
                "modality_summary": summary,
                "skipped": skipped,
            },
            indent=2,
        )
        + "\n"
    )

    print(f"Wrote {csv_path} and {json_path}")
    for row in summary:
        print(
            f"{row['model']}: {row['modality']} mean R²={row['mean_r2']:.3f} "
            f"(n={row['n_experiments']})"
        )


if __name__ == "__main__":
    main()

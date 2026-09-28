"""Aggregate trial-level scores into experiment and cross-experiment reports."""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


def _pearson(xs: list[float], ys: list[float]) -> float | None:
    n = len(xs)
    if n < 2:
        return None
    mx = sum(xs) / n
    my = sum(ys) / n
    cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    sy = math.sqrt(sum((y - my) ** 2 for y in ys))
    if sx == 0 or sy == 0:
        return None
    return cov / (sx * sy)


def _spearman(xs: list[float], ys: list[float]) -> float | None:
    if len(xs) < 2:
        return None

    def rank(vs):
        sv = sorted(enumerate(vs), key=lambda t: t[1])
        r = [0.0] * len(vs)
        i = 0
        while i < len(sv):
            j = i
            while j < len(sv) and sv[j][1] == sv[i][1]:
                j += 1
            avg = (i + j + 1) / 2
            for k in range(i, j):
                r[sv[k][0]] = avg
            i = j
        return r

    return _pearson(rank(xs), rank(ys))


def aggregate_experiment(
    trial_scores: list[dict[str, Any]],
) -> dict[str, Any]:
    """Aggregate per-trial scores into experiment-level summary."""
    metrics_by_type: dict[str, dict[str, list[float]]] = {}

    # Collect (model, human) pairs per tag for cross-trial correlation
    pairs_by_tag: dict[str, list[tuple[float, float]]] = {}

    n_trials = len(trial_scores)
    n_scorable = 0

    for entry in trial_scores:
        scores = entry.get("scores", {})
        for tag, tag_scores in scores.items():
            if not tag_scores.get("scorable", False):
                continue

            n_scorable += 1

            # Per-trial metrics (existing behavior)
            for metric, value in tag_scores.items():
                if metric in ("scorable", "parse_error", "missing_response",
                              "type", "text", "partial_ranking",
                              "human_distribution", "model_choice",
                              "model_choice_index", "model_binary",
                              "human_proportions", "model_values",
                              "human_means", "model_ranks", "human_mean_ranks",
                              "model_value", "human_mean"):
                    continue
                if value is None:
                    continue
                metrics_by_type.setdefault(metric, {"values": []})
                if isinstance(value, (int, float)):
                    metrics_by_type[metric]["values"].append(float(value))

            # Collect (model, human) pairs for slider-type queries
            mv = tag_scores.get("model_value")
            hv = tag_scores.get("human_mean")
            if mv is not None and hv is not None:
                pairs_by_tag.setdefault(tag, []).append((float(mv), float(hv)))

    summary: dict[str, Any] = {
        "n_trials": n_trials,
        "n_scorable_queries": n_scorable,
    }
    for metric, data in metrics_by_type.items():
        vals = data["values"]
        if vals:
            summary[f"mean_{metric}"] = sum(vals) / len(vals)
            if len(vals) > 1:
                mean = sum(vals) / len(vals)
                var = sum((v - mean) ** 2 for v in vals) / (len(vals) - 1)
                summary[f"std_{metric}"] = math.sqrt(var)

    # Cross-trial correlations per tag (and combined)
    if pairs_by_tag:
        per_tag_corr = {}
        all_m, all_h = [], []
        for tag, pairs in pairs_by_tag.items():
            ms = [p[0] for p in pairs]
            hs = [p[1] for p in pairs]
            all_m.extend(ms)
            all_h.extend(hs)
            per_tag_corr[tag] = {
                "n": len(ms),
                "pearson_r": _pearson(ms, hs),
                "spearman_rho": _spearman(ms, hs),
            }
        summary["cross_trial_correlation"] = per_tag_corr
        if all_m:
            summary["cross_trial_pearson_r"] = _pearson(all_m, all_h)
            summary["cross_trial_spearman_rho"] = _spearman(all_m, all_h)
            summary["cross_trial_n"] = len(all_m)

    return summary


def aggregate_cross_experiment(
    experiment_summaries: list[dict[str, Any]],
) -> dict[str, Any]:
    """Aggregate experiment-level summaries into a cross-experiment report."""
    all_metrics: dict[str, list[float]] = {}

    for exp_summary in experiment_summaries:
        for key, value in exp_summary.items():
            if key.startswith("mean_") and isinstance(value, (int, float)):
                all_metrics.setdefault(key, []).append(value)

    grand_summary: dict[str, Any] = {
        "n_experiments": len(experiment_summaries),
        "total_trials": sum(s.get("n_trials", 0) for s in experiment_summaries),
        "total_scorable_queries": sum(
            s.get("n_scorable_queries", 0) for s in experiment_summaries
        ),
    }

    for metric, vals in all_metrics.items():
        if vals:
            grand_name = f"grand_{metric}"
            grand_summary[grand_name] = sum(vals) / len(vals)
            if len(vals) > 1:
                mean = sum(vals) / len(vals)
                var = sum((v - mean) ** 2 for v in vals) / (len(vals) - 1)
                grand_summary[f"grand_std_{metric.removeprefix('mean_')}"] = math.sqrt(var)

    return grand_summary


def format_report(
    model: str,
    experiment_results: list[dict[str, Any]],
    grand_summary: dict[str, Any],
) -> str:
    """Format a human-readable text report."""
    lines: list[str] = []
    lines.append("=" * 72)
    lines.append(f"  CogGym Harness Report — Model: {model}")
    lines.append("=" * 72)
    lines.append("")

    # Grand summary
    lines.append("OVERALL SUMMARY")
    lines.append("-" * 40)
    lines.append(f"  Experiments tested:   {grand_summary.get('n_experiments', 0)}")
    lines.append(f"  Total trials:         {grand_summary.get('total_trials', 0)}")
    lines.append(f"  Scorable queries:     {grand_summary.get('total_scorable_queries', 0)}")
    lines.append("")

    for key, val in sorted(grand_summary.items()):
        if key.startswith("grand_mean_"):
            metric = key.removeprefix("grand_")
            std_key = f"grand_std_{metric.removeprefix('mean_')}"
            std_val = grand_summary.get(std_key)
            if std_val is not None:
                lines.append(f"  {metric}: {val:.4f} (±{std_val:.4f})")
            else:
                lines.append(f"  {metric}: {val:.4f}")
    lines.append("")

    # Per-experiment summaries
    lines.append("PER-EXPERIMENT RESULTS")
    lines.append("-" * 40)
    for exp_result in experiment_results:
        exp_name = exp_result.get("experiment", "")
        summary = exp_result.get("summary", {})
        lines.append(f"\n  {exp_name}")
        lines.append(f"    Trials: {summary.get('n_trials', 0)}, "
                      f"Scorable: {summary.get('n_scorable_queries', 0)}")

        for key, val in sorted(summary.items()):
            if key.startswith("mean_") and isinstance(val, (int, float)):
                lines.append(f"    {key}: {val:.4f}")
    lines.append("")

    return "\n".join(lines)


def save_results(
    results: list[dict[str, Any]],
    output_path: Path,
) -> None:
    """Save per-trial results to a JSONL file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        for entry in results:
            f.write(json.dumps(entry) + "\n")


def save_report(report: str, output_path: Path) -> None:
    """Save a text report to a file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        f.write(report)

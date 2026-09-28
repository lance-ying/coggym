"""Score model responses against human data.

Computes per-trial and aggregate metrics appropriate to each query type.
All metrics are implemented from scratch (no numpy/scipy dependency).
"""

from __future__ import annotations

import math
from typing import Any, Optional

from .experiment import Experiment, Query, Trial


# ── Metric helpers ──────────────────────────────────────────────────────────


def _pearson_r(xs: list[float], ys: list[float]) -> Optional[float]:
    """Pearson correlation coefficient. Returns None if degenerate."""
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


def _spearman_rho(xs: list[float], ys: list[float]) -> Optional[float]:
    """Spearman rank correlation."""
    if len(xs) < 2:
        return None
    rx = _rank(xs)
    ry = _rank(ys)
    return _pearson_r(rx, ry)


def _rank(values: list[float]) -> list[float]:
    """Assign ranks (1-based, averaged for ties)."""
    indexed = sorted(enumerate(values), key=lambda x: x[1])
    ranks = [0.0] * len(values)
    i = 0
    while i < len(indexed):
        j = i
        while j < len(indexed) and indexed[j][1] == indexed[i][1]:
            j += 1
        avg_rank = (i + j + 1) / 2  # average of 1-based ranks
        for k in range(i, j):
            ranks[indexed[k][0]] = avg_rank
        i = j
    return ranks


def _cosine_similarity(a: list[float], b: list[float]) -> Optional[float]:
    """Cosine similarity between two vectors."""
    dot = sum(x * y for x, y in zip(a, b))
    mag_a = math.sqrt(sum(x * x for x in a))
    mag_b = math.sqrt(sum(x * x for x in b))
    if mag_a == 0 or mag_b == 0:
        return None
    return dot / (mag_a * mag_b)


def _mse(xs: list[float], ys: list[float]) -> float:
    """Mean squared error."""
    return sum((x - y) ** 2 for x, y in zip(xs, ys)) / len(xs)


def _mae(xs: list[float], ys: list[float]) -> float:
    """Mean absolute error."""
    return sum(abs(x - y) for x, y in zip(xs, ys)) / len(xs)


# ── Per-query scoring ───────────────────────────────────────────────────────


def _get_human_values(
    trial_id: str, tag: str, n_options: int, human_data: dict,
    option_names: list[str] | None = None,
) -> Optional[list[float]]:
    """Extract human mean values for a given trial and query tag.

    Tries several key formats:
      1. human_data[trial_id][tag] = {tag_1: v1, tag_2: v2, ...}
      2. human_data[trial_id][tag] = {option_name: v1, ...}  (using query option names)
      3. human_data[trial_id][tag] = {arbitrary_key: v1, ...} (positional, if count matches)
    """
    trial_data = human_data.get(trial_id)
    if not trial_data or not isinstance(trial_data, dict):
        return None
    tag_data = trial_data.get(tag)
    if not tag_data or not isinstance(tag_data, dict):
        return None

    # Try format 1: tag_1, tag_2, ...
    values = []
    for i in range(1, n_options + 1):
        key = f"{tag}_{i}"
        if key in tag_data and tag_data[key] is not None:
            values.append(float(tag_data[key]))
        else:
            break
    if len(values) == n_options:
        return values

    # Try format 2: option names as keys (missing keys treated as 0)
    if option_names and len(option_names) == n_options:
        values = []
        found_any = False
        for opt in option_names:
            if opt in tag_data and tag_data[opt] is not None:
                values.append(float(tag_data[opt]))
                found_any = True
            else:
                values.append(0.0)
        if found_any:
            return values

    # Try format 3: positional (if dict has exactly n_options entries)
    numeric_vals = {k: v for k, v in tag_data.items() if v is not None}
    if len(numeric_vals) == n_options:
        try:
            return [float(v) for v in numeric_vals.values()]
        except (TypeError, ValueError):
            pass

    return None


def score_multi_choice(
    parsed: dict[str, Any],
    trial: Trial,
    query: Query,
    human_data: dict,
) -> dict[str, Any]:
    """Score a multi-choice response against human data."""
    n = len(query.option)
    human_vals = _get_human_values(trial.id, query.tag, n, human_data, option_names=query.option)
    if human_vals is None:
        return {"scorable": False}

    idx = parsed.get("selected_index", -1)
    if idx < 0 or idx >= n:
        return {"scorable": False, "parse_error": True}

    # Human probability assigned to the model's choice
    human_prob = human_vals[idx]

    # Mode match: did the model pick the most popular human choice?
    mode_idx = max(range(n), key=lambda i: human_vals[i])
    mode_match = int(idx == mode_idx)

    # Model as one-hot distribution
    model_dist = [0.0] * n
    model_dist[idx] = 1.0

    return {
        "scorable": True,
        "mode_match": mode_match,
        "human_prob_of_choice": human_prob,
        "human_distribution": human_vals,
        "model_choice_index": idx,
        "model_choice": parsed.get("selected", ""),
        "cosine_similarity": _cosine_similarity(model_dist, human_vals),
    }


def score_multi_select(
    parsed: dict[str, Any],
    trial: Trial,
    query: Query,
    human_data: dict,
) -> dict[str, Any]:
    """Score a multi-select response against human data."""
    n = len(query.option)
    human_vals = _get_human_values(trial.id, query.tag, n, human_data, option_names=query.option)
    if human_vals is None:
        return {"scorable": False}

    binary = parsed.get("binary", [0] * n)
    if len(binary) != n:
        return {"scorable": False, "parse_error": True}

    model_floats = [float(b) for b in binary]

    # Cosine similarity between model binary and human proportions
    cos_sim = _cosine_similarity(model_floats, human_vals)

    # Pearson correlation
    r = _pearson_r(model_floats, human_vals)

    # F1 against human threshold (options with proportion > 0.5 are "positive")
    human_binary = [1 if v > 0.5 else 0 for v in human_vals]
    tp = sum(1 for a, b in zip(binary, human_binary) if a == 1 and b == 1)
    fp = sum(1 for a, b in zip(binary, human_binary) if a == 1 and b == 0)
    fn = sum(1 for a, b in zip(binary, human_binary) if a == 0 and b == 1)
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0

    return {
        "scorable": True,
        "cosine_similarity": cos_sim,
        "pearson_r": r,
        "f1_vs_human_majority": f1,
        "model_binary": binary,
        "human_proportions": human_vals,
    }


def score_single_slider(
    parsed: dict[str, Any],
    trial: Trial,
    query: Query,
    human_data: dict,
) -> dict[str, Any]:
    """Score a single-slider response against human data."""
    trial_data = human_data.get(trial.id)
    if not trial_data or not isinstance(trial_data, dict):
        return {"scorable": False}
    tag_data = trial_data.get(query.tag)
    if tag_data is None:
        return {"scorable": False}

    # Single slider may have format:
    #   {tag: <number>}  (flat)
    #   {tag: {tag_response: <number>}}
    #   {tag: {tag_1: <number>}}
    human_val = None
    if isinstance(tag_data, (int, float)):
        human_val = float(tag_data)
    elif isinstance(tag_data, dict):
        response_key = f"{query.tag}_response"
        if response_key in tag_data:
            human_val = float(tag_data[response_key])
        else:
            key1 = f"{query.tag}_1"
            if key1 in tag_data:
                human_val = float(tag_data[key1])

    if human_val is None:
        return {"scorable": False}

    model_val = parsed.get("value")
    if model_val is None:
        return {"scorable": False, "parse_error": True}

    sc = query.slider_config or {}
    lo, hi = sc.get("min", 0), sc.get("max", 100)
    scale_range = hi - lo if hi != lo else 1

    abs_err = abs(model_val - human_val)
    norm_err = abs_err / scale_range

    return {
        "scorable": True,
        "absolute_error": abs_err,
        "normalized_error": norm_err,
        "model_value": model_val,
        "human_mean": human_val,
    }


def score_multi_slider(
    parsed: dict[str, Any],
    trial: Trial,
    query: Query,
    human_data: dict,
) -> dict[str, Any]:
    """Score a multi-slider response against human data."""
    n = len(query.option)
    human_vals = _get_human_values(trial.id, query.tag, n, human_data, option_names=query.option)
    if human_vals is None:
        return {"scorable": False}

    model_values = parsed.get("values", {})
    model_list: list[float] = []
    for opt in query.option:
        v = model_values.get(opt)
        if v is None:
            return {"scorable": False, "parse_error": True}
        model_list.append(v)

    r = _pearson_r(model_list, human_vals)
    mse = _mse(model_list, human_vals)
    mae = _mae(model_list, human_vals)

    return {
        "scorable": True,
        "pearson_r": r,
        "mse": mse,
        "mae": mae,
        "model_values": dict(zip(query.option, model_list)),
        "human_means": dict(zip(query.option, human_vals)),
    }


def score_ranking(
    parsed: dict[str, Any],
    trial: Trial,
    query: Query,
    human_data: dict,
) -> dict[str, Any]:
    """Score a ranking response against human data."""
    n = len(query.option)
    human_vals = _get_human_values(trial.id, query.tag, n, human_data, option_names=query.option)
    if human_vals is None:
        return {"scorable": False}

    ranking = parsed.get("ranking", [])
    if len(ranking) < n:
        return {"scorable": False, "parse_error": True, "partial_ranking": ranking}

    # Convert model ranking to rank values per option (1-based)
    model_ranks: list[float] = []
    for opt in query.option:
        if opt in ranking:
            model_ranks.append(float(ranking.index(opt) + 1))
        else:
            model_ranks.append(float(n))  # unranked items get last rank

    rho = _spearman_rho(model_ranks, human_vals)

    # Kendall's tau (simplified: count concordant/discordant pairs)
    concordant = 0
    discordant = 0
    for i in range(n):
        for j in range(i + 1, n):
            model_diff = model_ranks[i] - model_ranks[j]
            human_diff = human_vals[i] - human_vals[j]
            if model_diff * human_diff > 0:
                concordant += 1
            elif model_diff * human_diff < 0:
                discordant += 1
    n_pairs = n * (n - 1) / 2
    tau = (concordant - discordant) / n_pairs if n_pairs > 0 else None

    return {
        "scorable": True,
        "spearman_rho": rho,
        "kendall_tau": tau,
        "model_ranks": dict(zip(query.option, model_ranks)),
        "human_mean_ranks": dict(zip(query.option, human_vals)),
    }


def _score_textbox(
    parsed: dict[str, Any],
    trial: Trial,
    query: Query,
    human_data: dict,
) -> dict[str, Any]:
    """Score a textbox response. If both model and human are numeric, score like a slider."""
    import re
    text = parsed.get("text", "")

    # Strip currency symbols, commas, whitespace before extracting number
    cleaned = re.sub(r"[$€£¥,]", "", text).strip()
    numbers = re.findall(r"-?\d+(?:\.\d+)?", cleaned)
    if not numbers:
        return {"scorable": False, "type": "textbox", "text": text}

    model_val = float(numbers[0])

    # Check if human data has a numeric value for this tag
    trial_data = human_data.get(trial.id)
    if not trial_data or not isinstance(trial_data, dict):
        return {"scorable": False, "type": "textbox", "text": text}

    human_val = trial_data.get(query.tag)
    if human_val is None or not isinstance(human_val, (int, float)):
        return {"scorable": False, "type": "textbox", "text": text}

    human_val = float(human_val)
    abs_err = abs(model_val - human_val)

    return {
        "scorable": True,
        "absolute_error": abs_err,
        "model_value": model_val,
        "human_mean": human_val,
    }


# ── Main scoring entry point ───────────────────────────────────────────────


def score_trial(
    parsed_response: dict[str, Any],
    trial: Trial,
    experiment: Experiment,
) -> dict[str, Any]:
    """Score all queries in a trial against human data.

    Returns a dict keyed by query tag with scoring results.
    """
    human_data = experiment.human_data_mean
    results: dict[str, Any] = {}

    for query in trial.queries:
        if query.type == "text-instruction":
            continue
        tag = query.tag
        if tag not in parsed_response:
            results[tag] = {"scorable": False, "missing_response": True}
            continue

        parsed = parsed_response[tag]

        if query.type == "multi-choice":
            results[tag] = score_multi_choice(parsed, trial, query, human_data)
        elif query.type == "multi-select":
            results[tag] = score_multi_select(parsed, trial, query, human_data)
        elif query.type == "single-slider":
            results[tag] = score_single_slider(parsed, trial, query, human_data)
        elif query.type == "multi-slider":
            results[tag] = score_multi_slider(parsed, trial, query, human_data)
        elif query.type == "ranking":
            results[tag] = score_ranking(parsed, trial, query, human_data)
        elif query.type == "textbox":
            results[tag] = _score_textbox(parsed, trial, query, human_data)

    return results

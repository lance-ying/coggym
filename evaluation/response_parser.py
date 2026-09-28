"""Parse raw LLM text responses into structured data by query type."""

from __future__ import annotations

import json as _json
import re
from typing import Any

from .experiment import Query


def _extract_json(text: str) -> dict | None:
    """Try to extract a JSON object from text."""
    # Try parsing the whole text
    text = text.strip()
    # Strip markdown code fences
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```\s*$", "", text)
    try:
        return _json.loads(text)
    except _json.JSONDecodeError:
        pass
    # Try finding JSON object in text
    match = re.search(r"\{[^{}]*\}", text)
    if match:
        try:
            return _json.loads(match.group())
        except _json.JSONDecodeError:
            pass
    # Try finding JSON with nested braces
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return _json.loads(match.group())
        except _json.JSONDecodeError:
            pass
    return None


def _split_json_objects(raw: str) -> list[str]:
    """Extract top-level ``{...}`` JSON object strings in order, brace-matched.

    Handles models that return one JSON object per query concatenated together
    (e.g. ``{"answer": 6, ...}\\n{"answer": 2, ...}``), which the marker/blank-line
    splitters miss -- causing the first object to be broadcast to every query.
    """
    objs: list[str] = []
    depth = 0
    start = None
    in_str = False
    esc = False
    for i, ch in enumerate(raw):
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
            continue
        if ch == '"':
            in_str = True
        elif ch == "{":
            if depth == 0:
                start = i
            depth += 1
        elif ch == "}":
            if depth > 0:
                depth -= 1
                if depth == 0 and start is not None:
                    objs.append(raw[start : i + 1])
                    start = None
    return objs


def _load_json_whole(text: str):
    """Parse the ENTIRE text as one JSON value (strips code fences). None on failure."""
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```\s*$", "", text)
    try:
        return _json.loads(text)
    except _json.JSONDecodeError:
        return None


def _segments_from_json(raw: str, queries: list[Query]) -> dict[str, str] | None:
    """Map a structured JSON response to per-query segments, or None if not applicable.

    Handles the common multi-query formats that the line/marker splitter mangles:
      * one dict with one entry per query, keyed by query tag, by "Question N", or
        positionally (insertion order);
      * N concatenated top-level JSON objects, one per query (positional).
    Returns segments keyed by query tag (each a JSON string for the downstream parser).
    """
    n = len(queries)
    whole = _load_json_whole(raw)
    if isinstance(whole, dict) and len(whole) == n:
        keys = [str(k).strip() for k in whole.keys()]
        vals = list(whole.values())
        tagset = {q.tag for q in queries}
        # (a) keyed by query tag
        if tagset and tagset.issubset(set(keys)):
            by_key = {str(k).strip(): v for k, v in whole.items()}
            return {q.tag: _json.dumps(by_key[q.tag]) for q in queries}
        # (b) keyed by "Question N" / a bare number
        qn = [re.match(r"(?:question\s*)?(\d+)\s*$", k, re.I) for k in keys]
        if all(qn):
            order = sorted(range(n), key=lambda i: int(qn[i].group(1)))
            return {queries[i].tag: _json.dumps(vals[order[i]]) for i in range(n)}
        # (c) positional by insertion order
        return {queries[i].tag: _json.dumps(vals[i]) for i in range(n)}
    # (e) single wrapper dict with one list key ({"answers": [...]}) — N per-query objects
    if isinstance(whole, dict) and len(whole) == 1:
        v = next(iter(whole.values()))
        if isinstance(v, list) and len(v) == n:
            return {queries[i].tag: _json.dumps(v[i]) for i in range(n)}
    # (d) N concatenated top-level JSON objects, one per query
    objs = _split_json_objects(raw)
    if len(objs) == n:
        return {queries[i].tag: objs[i] for i in range(n)}
    return None


def parse_response(raw: str, queries: list[Query]) -> dict[str, Any]:
    """Parse a raw model response into structured per-query results.

    Returns a dict keyed by query tag, with values appropriate to the query type:
      multi-choice   -> {"selected": str, "selected_index": int}
      multi-select   -> {"selected": [str, ...], "binary": [0/1, ...]}
      single-slider  -> {"value": float}
      multi-slider   -> {"values": {option: float, ...}}
      ranking        -> {"ranking": [str, ...]}   (ordered best-to-worst)
      textbox        -> {"text": str}
    """
    # If there's only one non-instruction query, give it the full response
    scorable = [q for q in queries if q.type != "text-instruction"]
    if not scorable:
        return {}

    if len(scorable) == 1:
        segments = {scorable[0].tag: raw.strip()}
    else:
        segments = _segments_from_json(raw, scorable) or _split_response(raw, scorable)

    result: dict[str, Any] = {}
    for query in scorable:
        text = segments.get(query.tag, "").strip()
        if query.type == "multi-choice":
            result[query.tag] = _parse_multi_choice(text, query)
        elif query.type == "multi-select":
            result[query.tag] = _parse_multi_select(text, query)
        elif query.type == "single-slider":
            result[query.tag] = _parse_single_slider(text, query)
        elif query.type == "multi-slider":
            result[query.tag] = _parse_multi_slider(text, query)
        elif query.type == "ranking":
            result[query.tag] = _parse_ranking(text, query)
        elif query.type == "textbox":
            result[query.tag] = {"text": text}

    return result


def _split_response(raw: str, queries: list[Query]) -> dict[str, str]:
    """Split a multi-query response into segments for each query.

    Tries to find "Question N:" markers or query tag references.
    Falls back to splitting on blank lines.
    """
    segments: dict[str, str] = {}
    lines = raw.strip().split("\n")

    # Try splitting on "Question N:" markers
    question_pattern = re.compile(r"^(?:Question\s+)?(\d+)[.:)\s]", re.I)
    current_q = None
    current_lines: list[str] = []

    for line in lines:
        m = question_pattern.match(line.strip())
        if m:
            q_num = int(m.group(1))
            if current_q is not None and 0 <= current_q < len(queries):
                segments[queries[current_q].tag] = "\n".join(current_lines).strip()
            current_q = q_num - 1
            # Remove the "Question N:" prefix from the line
            remainder = line.strip()[m.end():].strip()
            current_lines = [remainder] if remainder else []
        else:
            current_lines.append(line)

    if current_q is not None and 0 <= current_q < len(queries):
        segments[queries[current_q].tag] = "\n".join(current_lines).strip()

    # If we found segments for all queries, return
    if len(segments) == len(queries):
        return segments

    # Fallback: try splitting on blank lines or newlines
    segments = {}
    chunks = re.split(r"\n\s*\n", raw.strip())
    if len(chunks) >= len(queries):
        for i, q in enumerate(queries):
            segments[q.tag] = chunks[i].strip()
    else:
        # Last resort: only broadcast when there is exactly one query.
        # For multi-query trials, broadcasting silently corrupts data with a
        # single value applied to every query — return empty segments so each
        # per-query parse cleanly returns scorable=False / parse_error=True.
        if len(queries) == 1:
            segments[queries[0].tag] = raw.strip()
        else:
            for q in queries:
                segments[q.tag] = ""

    return segments


def _parse_multi_choice(text: str, query: Query) -> dict[str, Any]:
    """Parse a multi-choice response. Returns selected option and index."""
    # Try JSON first
    j = _extract_json(text)
    if isinstance(j, dict) and "answer" in j:
        ans = str(j["answer"]).strip()
        # Letter answer (A, B, C...)
        if len(ans) == 1 and ans.upper() in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            idx = ord(ans.upper()) - ord("A")
            if 0 <= idx < len(query.option):
                return {"selected": query.option[idx], "selected_index": idx}
        # Match against option text
        ans_lower = ans.lower()
        for i, opt in enumerate(query.option):
            if ans_lower == opt.lower():
                return {"selected": opt, "selected_index": i}
        # Substring match (longest first)
        sorted_opts = sorted(enumerate(query.option), key=lambda x: len(x[1]), reverse=True)
        for i, opt in sorted_opts:
            if opt.lower() in ans_lower or ans_lower in opt.lower():
                return {"selected": opt, "selected_index": i}

    # Fallback: text-based parsing for non-JSON responses
    text_clean = text.strip().rstrip(".")
    text_lower = text_clean.lower()
    first_line = text_clean.split("\n")[0].strip().rstrip(".")
    first_line_lower = first_line.lower()

    # Try exact match first (full text or first line)
    for i, opt in enumerate(query.option):
        opt_lower = opt.lower()
        if text_lower == opt_lower or first_line_lower == opt_lower:
            return {"selected": opt, "selected_index": i}

    # Try letter prefix match (A, B, C...)
    letter_match = re.match(r"^([A-Z])[).:\s]", text_clean, re.I)
    if letter_match:
        idx = ord(letter_match.group(1).upper()) - ord("A")
        if 0 <= idx < len(query.option):
            return {"selected": query.option[idx], "selected_index": idx}

    # Try numeric prefix match (1, 2, 3...)
    num_match = re.match(r"^(\d+)[).:\s]", first_line)
    if num_match:
        idx = int(num_match.group(1)) - 1
        if 0 <= idx < len(query.option):
            return {"selected": query.option[idx], "selected_index": idx}

    # Try standalone number on first line
    num_only = re.match(r"^(\d+)\s*$", first_line)
    if num_only:
        idx = int(num_only.group(1)) - 1
        if 0 <= idx < len(query.option):
            return {"selected": query.option[idx], "selected_index": idx}

    # Try substring match — longest match first
    sorted_opts = sorted(enumerate(query.option), key=lambda x: len(x[1]), reverse=True)
    for i, opt in sorted_opts:
        if opt.lower() in text_lower:
            return {"selected": opt, "selected_index": i}

    # Try the reverse
    for i, opt in sorted_opts:
        if first_line_lower in opt.lower():
            return {"selected": opt, "selected_index": i}

    # No match found
    return {"selected": text_clean, "selected_index": -1}


def _parse_multi_select(text: str, query: Query) -> dict[str, Any]:
    """Parse a multi-select response. Returns list of selected options and binary vector."""
    binary = [0] * len(query.option)
    selected: list[str] = []

    # Try JSON first
    j = _extract_json(text)
    if isinstance(j, dict) and "answer" in j:
        ans = j["answer"]
        if isinstance(ans, list):
            for a in ans:
                a = str(a).strip()
                if len(a) == 1 and a.upper() in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                    idx = ord(a.upper()) - ord("A")
                    if 0 <= idx < len(query.option):
                        binary[idx] = 1
                        selected.append(query.option[idx])
                else:
                    a_low = a.lower()
                    # exact match first; else word-boundary longest match
                    # (prevents "Brick 1" swallowing "Brick 11")
                    hit = next((i for i, opt in enumerate(query.option)
                                if a_low == opt.lower()), None)
                    if hit is None:
                        cands = [(i, opt) for i, opt in enumerate(query.option)
                                 if re.search(r"(?<!\w)" + re.escape(opt.lower()) + r"(?!\w)", a_low)]
                        if cands:
                            hit = max(cands, key=lambda x: len(x[1]))[0]
                    if hit is not None:
                        binary[hit] = 1
                        if query.option[hit] not in selected:
                            selected.append(query.option[hit])
            if any(binary):
                return {"selected": selected, "binary": binary}

    # Fallback: text-based parsing
    text_clean = text.strip()
    parts = re.split(r"[,;\n]|\band\b", text_clean)
    parts = [p.strip().rstrip(".") for p in parts if p.strip()]

    for part in parts:
        letter_match = re.match(r"^([A-Z])[).:\s]", part, re.I)
        if letter_match:
            idx = ord(letter_match.group(1).upper()) - ord("A")
            if 0 <= idx < len(query.option):
                binary[idx] = 1
                selected.append(query.option[idx])
                continue

        matched = False
        sorted_opts = sorted(enumerate(query.option), key=lambda x: len(x[1]), reverse=True)
        for i, opt in sorted_opts:
            if opt.lower() in part.lower() or part.lower() in opt.lower():
                binary[i] = 1
                if opt not in selected:
                    selected.append(opt)
                matched = True
                break

        if not matched:
            for i, opt in enumerate(query.option):
                if opt.lower() in text_clean.lower():
                    binary[i] = 1
                    if opt not in selected:
                        selected.append(opt)

    return {"selected": selected, "binary": binary}


def _parse_single_slider(text: str, query: Query) -> dict[str, Any]:
    """Parse a single slider response. Returns a numeric value."""
    sc = query.slider_config or {}
    lo = sc.get("min", float("-inf"))
    hi = sc.get("max", float("inf"))

    # Try JSON first
    j = _extract_json(text)
    if isinstance(j, dict) and "answer" in j:
        try:
            value = float(j["answer"])
            value = max(lo, min(hi, value))
            return {"value": value}
        except (TypeError, ValueError):
            pass

    # Fallback: extract first number
    numbers = re.findall(r"-?\d+(?:\.\d+)?", text)
    if numbers:
        value = float(numbers[0])
        value = max(lo, min(hi, value))
        return {"value": value}
    return {"value": None}


def _parse_multi_slider(text: str, query: Query) -> dict[str, Any]:
    """Parse a multi-slider response. Returns values for each option."""
    sc = query.slider_config or {}
    lo = sc.get("min", float("-inf"))
    hi = sc.get("max", float("inf"))
    values: dict[str, float | None] = {}

    # Try JSON first
    j = _extract_json(text)
    if isinstance(j, dict):
        # JSON might be {"opt1": val, "opt2": val} or {"answer": {"opt1": val, ...}}
        data = j.get("answer", j) if "answer" in j else j
        if isinstance(data, dict):
            all_found = True
            for opt in query.option:
                if opt in data:
                    try:
                        values[opt] = max(lo, min(hi, float(data[opt])))
                    except (TypeError, ValueError):
                        values[opt] = None
                        all_found = False
                else:
                    all_found = False
            if all_found or any(v is not None for v in values.values()):
                for opt in query.option:
                    if opt not in values:
                        values[opt] = None
                return {"values": values}
        values = {}

    # Fallback: text-based parsing
    for opt in query.option:
        pattern = re.compile(
            re.escape(opt) + r"[:\-–—=]\s*(-?\d+(?:\.\d+)?)",
            re.I,
        )
        m = pattern.search(text)
        if m:
            val = float(m.group(1))
            values[opt] = max(lo, min(hi, val))
        else:
            values[opt] = None

    # Fallback: extract numbers in order
    if all(v is None for v in values.values()):
        numbers = re.findall(r"-?\d+(?:\.\d+)?", text)
        for i, opt in enumerate(query.option):
            if i < len(numbers):
                values[opt] = float(numbers[i])

    return {"values": values}


def _parse_ranking(text: str, query: Query) -> dict[str, Any]:
    """Parse a ranking response. Returns ordered list of items."""
    ranking: list[str] = []

    # Try JSON first
    j = _extract_json(text)
    if j:
        ans = j.get("answer", j.get("ranking", []))
        if isinstance(ans, list):
            for item in ans:
                item = str(item).strip()
                best = _best_option_match(item, query.option)
                if best and best not in ranking:
                    ranking.append(best)
            if ranking:
                return {"ranking": ranking}
        ranking = []

    # Fallback: numbered list
    numbered = re.findall(r"\d+[.):\s]+(.+)", text)
    if numbered:
        for item_text in numbered:
            item_text = item_text.strip().rstrip(".")
            best_match = _best_option_match(item_text, query.option)
            if best_match and best_match not in ranking:
                ranking.append(best_match)

    if len(ranking) < len(query.option):
        for line in text.strip().split("\n"):
            line = line.strip().rstrip(".")
            line = re.sub(r"^\d+[.):\s]+", "", line).strip()
            line = re.sub(r"^[-•]\s*", "", line).strip()
            if line:
                best = _best_option_match(line, query.option)
                if best and best not in ranking:
                    ranking.append(best)

    return {"ranking": ranking}


def _best_option_match(text: str, options: list[str]) -> str | None:
    """Find the best matching option for a text fragment."""
    text_lower = text.lower()
    # Exact match
    for opt in options:
        if text_lower == opt.lower():
            return opt
    # Containment
    for opt in options:
        if opt.lower() in text_lower or text_lower in opt.lower():
            return opt
    return None

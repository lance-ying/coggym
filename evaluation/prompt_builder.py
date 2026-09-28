"""Build Gemini prompts from EML experiment data.

Message structure:
  [system]  Generic participant instruction
  [user]    Experiment instructions + trial stimuli + queries (merged)
"""

from __future__ import annotations

import base64
import io
import mimetypes
import re
from pathlib import Path
from typing import Any

from .experiment import Experiment, Query, Stimulus, Trial

# ── Media helpers ───────────────────────────────────────────────────────────

SUPPORTED_IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".webp"}
SUPPORTED_AUDIO_EXTS = {".mp3", ".wav", ".aac", ".ogg", ".flac"}
SUPPORTED_MEDIA_EXTS = SUPPORTED_IMAGE_EXTS | {".mp4"} | SUPPORTED_AUDIO_EXTS
UNSUPPORTED_MEDIA_EXTS = set()


def _resolve_media(media_url: str, experiment_path: Path) -> Path:
    return experiment_path / media_url


def _encode_image_base64(path: Path) -> tuple[str, str]:
    suffix = path.suffix.lower()
    media_type = mimetypes.types_map.get(suffix, "image/png")
    if suffix == ".jpg":
        media_type = "image/jpeg"
    with open(path, "rb") as f:
        data = base64.standard_b64encode(f.read()).decode("ascii")
    return data, media_type


def _extract_gif_frames(path: Path) -> list[dict[str, Any]]:
    """Extract all frames from an animated GIF as individual PNGs."""
    from PIL import Image

    frames: list[dict[str, Any]] = []
    with Image.open(path) as img:
        n_frames = getattr(img, "n_frames", 1)
        for i in range(n_frames):
            img.seek(i)
            frame = img.convert("RGBA")
            buf = io.BytesIO()
            frame.save(buf, format="PNG")
            b64 = base64.standard_b64encode(buf.getvalue()).decode("ascii")
            frames.append({"base64": b64, "media_type": "image/png"})
    return frames


def _is_animated_gif(path: Path) -> bool:
    if path.suffix.lower() != ".gif":
        return False
    from PIL import Image
    with Image.open(path) as img:
        return getattr(img, "n_frames", 1) > 1


def _strip_html(text: str) -> str:
    # Insert newlines when block-level tags close so paragraphs/list items don't merge
    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.I)
    text = re.sub(r"</(p|div|li|h[1-6]|blockquote)\s*>", "\n", text, flags=re.I)
    text = re.sub(r"<li[^>]*>", "- ", text, flags=re.I)
    # Strip remaining tags (block-level closers already handled above)
    text = re.sub(r"</?(p|ul|ol|li|strong|b|i|em|div|span|q|blockquote|h[1-6])[^>]*>", "", text, flags=re.I)
    text = text.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    text = text.replace("&nbsp;", " ").replace("&quot;", '"')
    # Collapse 3+ consecutive newlines to 2
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _encode_media(path: Path, refs_only: bool = False) -> list[dict[str, Any]]:
    """Encode media into content parts.

    If refs_only=True, returns lightweight references (no base64, no GIF extraction).
    Used when media will be resolved to GCS URIs later.
    """
    suffix = path.suffix.lower()

    if refs_only:
        # Lightweight: just return a reference with the source path
        mime = mimetypes.types_map.get(suffix, "image/png")
        if suffix == ".jpg":
            mime = "image/jpeg"
        if suffix in (".mp4",):
            return [{"type": "video", "path": str(path), "mime_type": "video/mp4"}]
        if suffix == ".gif":
            mp4 = path.with_suffix(".mp4")
            if mp4.exists():
                return [{"type": "video", "path": str(mp4), "mime_type": "video/mp4"}]
        if suffix in SUPPORTED_AUDIO_EXTS:
            mime = mimetypes.types_map.get(suffix, "audio/mpeg")
            return [{"type": "audio", "path": str(path), "mime_type": mime}]
        else:
            return [{"type": "image_ref", "path": str(path), "mime_type": mime}]

    if suffix == ".gif":
        mp4 = path.with_suffix(".mp4")
        if mp4.exists():
            return [{"type": "video", "path": str(mp4), "mime_type": "video/mp4"}]
    if _is_animated_gif(path):
        frames = _extract_gif_frames(path)
        for f in frames:
            f["_source_path"] = str(path)
        return frames
    elif suffix == ".mp4":
        return [{"type": "video", "path": str(path), "mime_type": "video/mp4"}]
    elif suffix in SUPPORTED_AUDIO_EXTS:
        mime = mimetypes.types_map.get(suffix, "audio/mpeg")
        return [{"type": "audio", "path": str(path), "mime_type": mime}]
    else:
        b64, mtype = _encode_image_base64(path)
        return [{"base64": b64, "media_type": mtype, "_source_path": str(path)}]


# ── Query formatting ────────────────────────────────────────────────────────


def _format_query(query: Query, index: int = 1) -> str:
    parts: list[str] = []

    if query.type == "text-instruction":
        parts.append(_strip_html(query.prompt))
        return "\n".join(parts)

    parts.append(f"Question {index}: {_strip_html(query.prompt)}")

    if query.type == "multi-choice":
        parts.append("Select exactly ONE of the following options:")
        for i, opt in enumerate(query.option):
            parts.append(f"  {chr(65 + i)}) {opt}")
        parts.append('Respond in JSON: {"answer": "<selected option letter A/B/C/...>"}')

    elif query.type == "multi-select":
        parts.append("Select one or more of the following options:")
        for i, opt in enumerate(query.option):
            parts.append(f"  {chr(65 + i)}) {opt}")
        parts.append('Respond in JSON: {"answer": ["<letter>", "<letter>", ...]}')

    elif query.type == "single-slider":
        sc = query.slider_config or {}
        lo, hi = sc.get("min", 0), sc.get("max", 100)
        labels = sc.get("labels", [])
        label_str = ", ".join(f'{l.get("value", "")}={l.get("label", "")}' for l in labels if isinstance(l, dict))
        if label_str:
            parts.append(f"  Scale: {label_str}")
        parts.append(f'Respond in JSON: {{"answer": <number between {lo} and {hi}>}}')

    elif query.type == "multi-slider":
        sc = query.slider_config or {}
        lo, hi = sc.get("min", 0), sc.get("max", 100)
        labels = sc.get("labels", [])
        label_str = ", ".join(f'{l.get("value", "")}={l.get("label", "")}' for l in labels if isinstance(l, dict))
        parts.append(f"Rate each item below on a scale from {lo} to {hi}.")
        if label_str:
            parts.append(f"  Scale: {label_str}")
        example = ", ".join(f'"{opt}": <number>' for opt in query.option)
        parts.append(f"Respond in JSON: {{{example}}}")

    elif query.type == "ranking":
        parts.append("Rank the following items from most to least preferred:")
        for opt in query.option:
            parts.append(f"  - {opt}")
        parts.append('Respond in JSON: {"answer": ["<most preferred>", "<2nd>", ..., "<least preferred>"]}')

    elif query.type == "textbox":
        parts.append(f'Respond in JSON: {{"answer": "<your response>"}}')

    return "\n".join(parts)


# ── Stimulus formatting ─────────────────────────────────────────────────────


def _format_stimulus_text(stimulus: Stimulus) -> str:
    parts: list[str] = []
    if stimulus.title:
        parts.append(f"[{stimulus.title}]")
    if stimulus.input_type == "text" and stimulus.text:
        parts.append(_strip_html(stimulus.text))
    elif stimulus.input_type in ("img", "video", "audio"):
        pass  # media handled separately by _encode_media
    return "\n".join(parts)


# ── Main prompt builders ────────────────────────────────────────────────────


def build_system_prompt(experiment: Experiment) -> str:
    return (
        "You are a participant in a cognitive science experiment. "
        "Follow the instructions carefully and respond to each question. "
        "Give only your answer — do not add explanations, reasoning, or caveats. "
        "IMPORTANT: You MUST respond in valid JSON format. "
        "Use the exact format specified in each question."
    )




# -- Tutorial/practice filtering (prompts must not include tutorial trials) --
_TUT_ID_RE = re.compile(r"(practice|tutorial|demo|quiz|comprehension|test_trial)", re.I)
_TUT_TEXT_RE = re.compile(
    r"(finished the (tutorial|practice)|you'?ve? (now )?finished"
    r"|comprehension (question|quiz|check)|practice (scenario|run|trial)"
    r"|congratulations.{0,50}(finished|complete)|you will now (observe|see|start)"
    r"|ready to (start|begin)\?|retake the quiz"
    r"|for the last part of the tutorial|quick questions to check your understanding)",
    re.I)
_PRACTICE_NARR_RE = re.compile(
    r"practice (run|trial|scenario)|practice scenario|watch the players? move a step"
    r"|the true goal was|was trying to reach|correct answer was|the answer (was|is)",
    re.I)
_TUT_SENT_RE = re.compile(
    r"[^.!?]*(practice (run|trial|scenario)s?|comprehension (question|quiz|check)s?"
    r"|finished the (tutorial|practice)|check questions|retake the quiz"
    r"|the true goal was|was trying to reach [^.!?]*therefore"
    r"|you will see a practice)[^.!?]*[.!?]",
    re.I)

def _is_tutorial_module(instr) -> bool:
    # ID-based: catches things like "tutorial_01", "practice_intro", "comprehension_quiz_01"
    if _TUT_ID_RE.search(str(getattr(instr, "id", "") or "")):
        return True
    text = str(getattr(instr, "text", "") or "")
    if not text:
        return False
    plain = re.sub(r"<[^>]+>", " ", text).strip()
    # Only drop modules dominated by end-of-tutorial framing. Passing mentions of
    # "practice trial" in substantive task instructions must be kept — sentence-level
    # scrubbing (_scrub_tutorial_sentences below) handles those in-place.
    STRONG = re.compile(
        r"(you'?ve? (now )?finished the (tutorial|practice)"
        r"|you have finished the (tutorial|practice)"
        r"|congratulations[^.!?]{0,60}(finished|complete))",
        re.I)
    # Only drop if strong signal appears near the START of the module (first 120 chars)
    # AND the module is short overall (dominated by that framing).
    if STRONG.search(plain[:120]) and len(plain) < 350:
        return True
    return False

def _is_practice_narration(text: str) -> bool:
    return bool(text and _PRACTICE_NARR_RE.search(text))

def _scrub_tutorial_sentences(text: str) -> str:
    if not text:
        return text
    return _TUT_SENT_RE.sub("", text)


def _get_condition_instructions(experiment: Experiment, trial_id: str) -> list:
    """Get prompt-visible instructions that precede this trial in its flow.

    EML instruction placement is temporal.  A later instruction must not leak
    into an earlier trial prompt, even when both belong to the same condition.
    """
    block_groups = experiment.flow_block_groups()

    # Liu2025Children uses interleaved familiarization/test blocks (one fam video per
    # concept). A trial should only receive the global intro (first block) + its OWN
    # concept's familiarization (the nearest preceding instruction block), NOT every
    # concept's fam. Scoped to Liu2025Children to avoid changing other experiments.
    if "Liu2025Children" in str(getattr(experiment, "path", "")):
        instr_ids_all = {
            i.id
            for i in experiment.instructions
            if i.type == "instruction" and i.include_in_model_prompt
        }
        def _is_instr_block(b):
            return len(b) > 0 and all(x in instr_ids_all for x in b)
        for blocks in block_groups:
            ti = next((bi for bi, b in enumerate(blocks) if trial_id in b), None)
            if ti is None:
                continue
            keep: list = []
            if blocks and _is_instr_block(blocks[0]):
                keep += [x for x in blocks[0] if x in instr_ids_all]
            for bi in range(ti - 1, -1, -1):
                if _is_instr_block(blocks[bi]):
                    for x in blocks[bi]:
                        if x in instr_ids_all and x not in keep:
                            keep.append(x)
                    break
            if keep:
                order = {i.id: k for k, i in enumerate(experiment.instruction_modules())}
                keep_sorted = sorted(set(keep), key=lambda x: order.get(x, 10**9))
                return [
                    i
                    for i in experiment.instruction_modules()
                    if i.id in keep_sorted and i.include_in_model_prompt
                ]

    # Default behavior (all other experiments): accumulate only instructions
    # encountered before the target trial in the matching exact sequence.
    instruction_by_id = {
        instruction.id: instruction
        for instruction in experiment.instruction_modules()
        if instruction.include_in_model_prompt
    }
    for blocks in block_groups:
        preceding: list = []
        for block in blocks:
            for item_id in block:
                if item_id == trial_id:
                    return preceding
                instruction = instruction_by_id.get(item_id)
                if instruction is not None and instruction not in preceding:
                    preceding.append(instruction)

    # Fallback for malformed/legacy flows: preserve the previous broad behavior,
    # while still respecting the explicit prompt-visibility flag.
    return [
        instruction
        for instruction in experiment.instruction_modules()
        if instruction.include_in_model_prompt
    ]

def build_instruction_content(experiment: Experiment, refs_only: bool = False,
                              trial_id: str | None = None) -> list[dict[str, Any]]:
    """Build content parts for experiment instructions.

    If trial_id is provided, only includes instructions from the matching condition.
    """
    text_parts: list[str] = ["=== EXPERIMENT INSTRUCTIONS ===\n"]
    media_parts: list[dict[str, Any]] = []

    if trial_id:
        instructions = _get_condition_instructions(experiment, trial_id)
    else:
        instructions = experiment.instruction_modules()

    # Build interleaved: text then media for each instruction, preserving order
    result: list[dict[str, Any]] = [{"type": "text", "text": "=== EXPERIMENT INSTRUCTIONS ===\n"}]

    for instr in instructions:
        if not instr.include_in_model_prompt:
            continue
        if _is_tutorial_module(instr):
            continue
        instr_text = _strip_html(instr.text) if instr.text else ""
        drop_media = _is_practice_narration(instr_text)
        instr_text = _scrub_tutorial_sentences(instr_text)
        if instr_text.strip():
            result.append({"type": "text", "text": instr_text + "\n"})
        if drop_media:
            continue

        for url in instr.media_url:
            if re.search(r"(^|/)(tutorials?|practice|demos?)(/|_)", str(url), re.I):
                continue
            abs_path = _resolve_media(url, experiment.path)
            if abs_path.exists() and abs_path.suffix.lower() in SUPPORTED_MEDIA_EXTS:
                parts = _encode_media(abs_path, refs_only=refs_only)
                for part in parts:
                    if part.get("type") in ("video", "image_ref", "audio"):
                        result.append(part)
                    else:
                        result.append({"type": "image", **part})

    return result


def build_trial_content(trial: Trial, experiment: Experiment, refs_only: bool = False) -> list[dict[str, Any]]:
    """Build content parts for a single trial, interleaving text and media."""
    result: list[dict[str, Any]] = [{"type": "text", "text": "\n=== SCENARIO ===\n"}]

    # Stimuli: interleave text and media per stimulus
    for stim in trial.stimuli:
        stim_text = _format_stimulus_text(stim)
        if stim_text:
            result.append({"type": "text", "text": stim_text})

        if stim.input_type in ("img", "video", "audio"):
            for url in stim.media_url:
                abs_path = _resolve_media(url, experiment.path)
                if abs_path.exists() and abs_path.suffix.lower() in SUPPORTED_MEDIA_EXTS:
                    parts = _encode_media(abs_path, refs_only=refs_only)
                    for part in parts:
                        if part.get("type") in ("video", "image_ref", "audio"):
                            result.append(part)
                        else:
                            result.append({"type": "image", **part})

    # Queries
    q_lines = []
    q_index = 1
    for query in trial.queries:
        if query.type == "text-instruction":
            q_lines.append(_format_query(query))
        else:
            q_lines.append(_format_query(query, q_index))
            q_index += 1
        q_lines.append("")

    result.append({"type": "text", "text": "\n".join(q_lines)})
    return result


def build_messages(
    trial: Trial, experiment: Experiment, refs_only: bool = False,
) -> tuple[str, list[dict[str, Any]]]:
    """Build the full message sequence for one trial.

    Returns (system_prompt, messages).
    """
    system = build_system_prompt(experiment)
    instr_content = build_instruction_content(experiment, refs_only=refs_only, trial_id=trial.id)
    trial_content = build_trial_content(trial, experiment, refs_only=refs_only)

    # Format for Gemini (base64 images + video file paths)
    instr_parts = _format_content(instr_content)
    trial_parts = _format_content(trial_content)

    # Merge into single user message
    if isinstance(instr_parts, str) and isinstance(trial_parts, str):
        combined = instr_parts + "\n\n" + trial_parts
    elif isinstance(instr_parts, str):
        combined = [{"type": "text", "text": instr_parts}] + trial_parts
    elif isinstance(trial_parts, str):
        combined = instr_parts + [{"type": "text", "text": trial_parts}]
    else:
        combined = instr_parts + trial_parts

    return system, [{"role": "user", "content": combined}]


def _format_content(parts: list[dict[str, Any]]) -> list[dict[str, Any]] | str:
    """Format content parts for Gemini."""
    has_media = any(p["type"] in ("image", "video", "image_ref", "audio") for p in parts)

    if not has_media:
        return "\n".join(p["text"] for p in parts if p["type"] == "text")

    formatted = []
    for p in parts:
        if p["type"] == "text":
            formatted.append({"type": "text", "text": p["text"]})
        elif p["type"] in ("video", "image_ref", "audio"):
            formatted.append(p)
        elif p["type"] == "image":
            img_part = {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": p["media_type"],
                    "data": p["base64"],
                },
            }
            if "_source_path" in p:
                img_part["_source_path"] = p["_source_path"]
            formatted.append(img_part)
    return formatted

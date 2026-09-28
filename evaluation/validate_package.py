"""Validate the public CogGym package before publishing it."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

from .experiment import load_experiment


REQUIRED_FILES = {
    "config.json",
    "instruction.jsonl",
    "trial.jsonl",
    "human_data_mean.json",
}
FORBIDDEN_NAMES = {"paper.pdf", ".DS_Store", ".env"}
SECRET_PATTERN = re.compile(
    r"(?i)(?:api[_-]?key|secret|token)\s*=\s*['\"][A-Za-z0-9_\-]{16,}['\"]"
)


def _urls(value) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [item for item in value if isinstance(item, str)]
    return []


def _referenced_media(exp_path: Path) -> set[str]:
    references: set[str] = set()
    for filename in ("instruction.jsonl", "trial.jsonl"):
        with (exp_path / filename).open() as handle:
            for line in handle:
                if not line.strip():
                    continue
                record = json.loads(line)
                references.update(_urls(record.get("media_url")))
                for stimulus in record.get("stimuli", []):
                    references.update(_urls(stimulus.get("media_url")))
    return references


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    manifest_path = root / "evaluation" / "public_manifest.json"
    selection_path = root / "evaluation" / "trial_selection_map.json"
    manifest = json.loads(manifest_path.read_text())
    selection = json.loads(selection_path.read_text())
    expected = {entry["path"] for entry in manifest["experiments"]}
    actual = {
        path.parent.relative_to(root / "EML").as_posix()
        for path in (root / "EML").glob("*/*/config.json")
    }

    if manifest.get("experimentCount") != len(expected):
        errors.append("manifest experimentCount does not match its experiment list")
    if expected != actual:
        errors.append(
            f"EML allowlist mismatch: missing={sorted(expected - actual)}, "
            f"extra={sorted(actual - expected)}"
        )
    if set(selection) != expected:
        errors.append("trial selection keys do not exactly match the public manifest")

    declared_individual_count = manifest.get("individualResponseExperimentCount")
    actual_individual_count = 0

    for relative in sorted(expected):
        exp_path = root / "EML" / relative
        missing_files = sorted(name for name in REQUIRED_FILES if not (exp_path / name).is_file())
        if missing_files:
            errors.append(f"{relative}: missing required files {missing_files}")
            continue

        experiment = load_experiment(exp_path)
        individual_path = exp_path / "human_data_ind.json"
        has_individual = individual_path.is_file()
        manifest_entry = next(entry for entry in manifest["experiments"] if entry["path"] == relative)
        if manifest_entry.get("hasIndividualResponses") != has_individual:
            errors.append(f"{relative}: individual-response availability differs from manifest")
        if has_individual:
            actual_individual_count += 1
            try:
                individual_data = json.loads(individual_path.read_text())
            except (OSError, json.JSONDecodeError) as error:
                errors.append(f"{relative}: invalid human_data_ind.json ({error})")
            else:
                if not isinstance(individual_data, dict):
                    errors.append(f"{relative}: human_data_ind.json must contain a JSON object")

        trial_ids = {trial.id for trial in experiment.experiment_trials()}
        selected_ids = selection[relative].get("selected_ids", [])
        missing_trials = sorted(set(selected_ids) - trial_ids)
        if missing_trials:
            errors.append(f"{relative}: selected IDs absent from experiment flow: {missing_trials[:5]}")

        for reference in sorted(_referenced_media(exp_path)):
            parsed = urlparse(reference)
            if parsed.scheme in {"http", "https", "data", "gs"}:
                continue
            if not (exp_path / reference).is_file():
                errors.append(f"{relative}: missing referenced media {reference}")

    if declared_individual_count != actual_individual_count:
        errors.append(
            "manifest individualResponseExperimentCount does not match packaged files: "
            f"declared={declared_individual_count}, actual={actual_individual_count}"
        )

    for path in root.rglob("*"):
        if path.is_file() and (
            path.name in FORBIDDEN_NAMES
            or path.name.startswith("._")
            or path.suffix.lower() == ".pdf"
        ):
            errors.append(f"forbidden release artifact: {path.relative_to(root)}")
        if path.is_file() and path.suffix in {".py", ".json", ".md"}:
            try:
                text = path.read_text()
            except UnicodeDecodeError:
                continue
            if SECRET_PATTERN.search(text):
                errors.append(f"possible embedded credential: {path.relative_to(root)}")

    return errors


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    errors = validate(root)
    if errors:
        print("Public package validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        raise SystemExit(1)

    manifest = json.loads((root / "evaluation" / "public_manifest.json").read_text())
    print(
        f"Validated {manifest['experimentCount']} experiments across "
        f"{manifest['studyCount']} studies; no forbidden artifacts or missing references."
    )


if __name__ == "__main__":
    main()

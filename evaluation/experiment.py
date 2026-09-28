"""Experiment discovery and EML file loading."""

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional


@dataclass
class Query:
    prompt: str
    type: str
    tag: str = ""
    option: list[str] = field(default_factory=list)
    slider_config: Optional[dict] = None
    answer: Optional[int] = None
    required: bool = False
    randomize_order: bool = False
    sampling_size: Optional[int] = None

    @classmethod
    def from_dict(cls, d: dict) -> "Query":
        return cls(
            prompt=d.get("prompt", ""),
            type=d["type"],
            tag=d.get("tag", ""),
            option=d.get("option", []),
            slider_config=d.get("slider_config"),
            answer=d.get("answer"),
            required=d.get("required", False),
            randomize_order=d.get("randomize_order", False),
            sampling_size=d.get("sampling_size"),
        )


@dataclass
class Stimulus:
    input_type: str  # img, video, text
    media_url: list[str] = field(default_factory=list)
    text: str = ""
    title: str = ""
    width: Optional[int] = None
    height: Optional[int] = None

    @classmethod
    def from_dict(cls, d: dict) -> "Stimulus":
        return cls(
            input_type=d["input_type"],
            media_url=d.get("media_url", []),
            text=d.get("text", ""),
            title=d.get("title", ""),
            width=d.get("width"),
            height=d.get("height"),
        )


@dataclass
class Trial:
    id: str
    stimuli: list[Stimulus]
    queries: list[Query]
    condition: str = ""
    metadata: Optional[dict] = None

    @classmethod
    def from_dict(cls, d: dict) -> "Trial":
        return cls(
            id=d["id"],
            stimuli=[Stimulus.from_dict(s) for s in d.get("stimuli", [])],
            queries=[Query.from_dict(q) for q in d.get("queries", [])],
            condition=d.get("condition", ""),
            metadata=d.get("metadata"),
        )


@dataclass
class Instruction:
    id: str
    type: str  # instruction, test_trial, comprehension_quiz
    text: str = ""
    media_url: list[str] = field(default_factory=list)
    stimuli_id: str = ""
    include_in_model_prompt: bool = True

    @classmethod
    def from_dict(cls, d: dict) -> "Instruction":
        return cls(
            id=d["id"],
            type=d["type"],
            text=d.get("text", ""),
            media_url=d.get("media_url", []),
            stimuli_id=d.get("stimuli_id", ""),
            include_in_model_prompt=d.get("include_in_model_prompt", True),
        )


@dataclass
class Experiment:
    path: Path
    study: str
    exp_name: str
    config: dict
    instructions: list[Instruction]
    trials: list[Trial]
    human_data_mean: dict

    @property
    def full_name(self) -> str:
        return f"{self.study}/{self.exp_name}"

    @property
    def experiment_name(self) -> str:
        return self.config.get("experimentName", self.full_name)

    @property
    def description(self) -> str:
        return self.config.get("description", "")

    @property
    def task_types(self) -> list[str]:
        return self.config.get("taskType", [])

    @property
    def response_types(self) -> list[str]:
        return self.config.get("responseType", [])

    @property
    def stimuli_count(self) -> int:
        return self.config.get("stimuli_count", len(self.trials))

    def instruction_modules(self) -> list[Instruction]:
        """Return only instruction-type modules (skip test_trial, comprehension_quiz)."""
        return [i for i in self.instructions if i.type == "instruction"]

    def experiment_trials(self) -> list[Trial]:
        """Return trials that appear in experimentFlow (excluding practice/tutorial)."""
        flow_ids = set()
        for blocks in self.flow_block_groups():
            for block in blocks:
                flow_ids.update(block)

        # Separate practice/tutorial trials from experiment trials
        instruction_ids = {i.id for i in self.instructions}
        # Also collect stimuli_ids referenced by test_trial instructions
        test_trial_stimuli = {
            i.stimuli_id for i in self.instructions if i.type == "test_trial" and i.stimuli_id
        }

        return [
            t
            for t in self.trials
            if t.id in flow_ids
            and t.id not in instruction_ids
            and t.id not in test_trial_stimuli
        ]

    def flow_block_groups(self) -> list[list[list[str]]]:
        """Return the block lists for every condition/sequence in the EML flow.

        Older EML files put ``blocks`` directly under a condition. Current EML
        files put one or more ``sequences`` under each condition. Supporting
        both layouts keeps the public runner compatible with the full release.
        """
        groups: list[list[list[str]]] = []
        for condition in self.config.get("experimentFlow", []):
            direct_blocks = condition.get("blocks")
            if isinstance(direct_blocks, list):
                groups.append(direct_blocks)

            for sequence in condition.get("sequences", []):
                blocks = sequence.get("blocks")
                if isinstance(blocks, list):
                    groups.append(blocks)
        return groups


def load_experiment(exp_dir: Path) -> Experiment:
    """Load a single experiment from its directory."""
    study = exp_dir.parent.name
    exp_name = exp_dir.name

    with open(exp_dir / "config.json") as f:
        config = json.load(f)

    instructions = []
    instr_path = exp_dir / "instruction.jsonl"
    if instr_path.exists():
        with open(instr_path) as f:
            for line in f:
                line = line.strip()
                if line:
                    instructions.append(Instruction.from_dict(json.loads(line)))

    trials = []
    trial_path = exp_dir / "trial.jsonl"
    if trial_path.exists():
        with open(trial_path) as f:
            for line in f:
                line = line.strip()
                if line:
                    trials.append(Trial.from_dict(json.loads(line)))

    human_data_mean: dict[str, Any] = {}
    mean_path = exp_dir / "human_data_mean.json"
    if mean_path.exists():
        with open(mean_path) as f:
            human_data_mean = json.load(f)

    return Experiment(
        path=exp_dir,
        study=study,
        exp_name=exp_name,
        config=config,
        instructions=instructions,
        trials=trials,
        human_data_mean=human_data_mean,
    )


def discover_experiments(
    processed_dir: Path,
    filter_study: Optional[str] = None,
    filter_response_type: Optional[str] = None,
    filter_task_type: Optional[str] = None,
) -> list[Experiment]:
    """Discover and load all experiments under processed_dir.

    Args:
        processed_dir: Root processed/ directory.
        filter_study: If set, only load experiments from this study (e.g. "alanqary2021Modeling").
        filter_response_type: If set, only load experiments containing this response type.
        filter_task_type: If set, only load experiments containing this task type.
    """
    experiments = []
    if not processed_dir.exists():
        return experiments

    for study_dir in sorted(processed_dir.iterdir()):
        if not study_dir.is_dir():
            continue
        if filter_study and study_dir.name != filter_study:
            continue

        for exp_dir in sorted(study_dir.iterdir()):
            if not exp_dir.is_dir():
                continue
            config_path = exp_dir / "config.json"
            if not config_path.exists():
                continue

            try:
                exp = load_experiment(exp_dir)
            except Exception as e:
                print(f"  Warning: failed to load {study_dir.name}/{exp_dir.name}: {e}")
                continue

            if filter_response_type and filter_response_type not in exp.response_types:
                continue
            if filter_task_type and filter_task_type not in exp.task_types:
                continue

            experiments.append(exp)

    return experiments

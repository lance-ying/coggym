from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from evaluation.analyze import analyze
from evaluation.experiment import load_experiment
from evaluation.prompt_builder import build_messages
from evaluation.validate_package import validate


ROOT = Path(__file__).resolve().parents[2]


class PublicEvaluationTests(unittest.TestCase):
    def test_nested_sequence_flow_is_loaded(self) -> None:
        experiment = load_experiment(ROOT / "EML" / "Radkani2025What" / "exp4")
        trials = experiment.experiment_trials()
        self.assertEqual(len(trials), 18)
        system, messages = build_messages(trials[0], experiment, refs_only=True)
        self.assertIn("cognitive science experiment", system)
        self.assertEqual(messages[0]["role"], "user")

    def test_perfect_synthetic_run_has_unit_r2(self) -> None:
        trial_ids = [f"Legitimate_obs{index}" for index in range(5)]
        artifact = {
            "model": "test-model",
            "experiment": "Radkani2025What/exp4",
            "trials": [
                {
                    "trial_id": trial_id,
                    "scores": {
                        "wrongness": {
                            "scorable": True,
                            "model_value": index,
                            "human_mean": index,
                        }
                    },
                }
                for index, trial_id in enumerate(trial_ids)
            ],
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "run.json"
            path.write_text(json.dumps(artifact))
            rows, summary, skipped = analyze(
                [path],
                ROOT / "EML",
                ROOT / "evaluation" / "public_manifest.json",
                min_items=5,
            )
        self.assertFalse(skipped)
        self.assertEqual(len(rows), 1)
        self.assertAlmostEqual(rows[0]["r2"], 1.0)
        self.assertAlmostEqual(summary[0]["mean_r2"], 1.0)

    def test_release_integrity(self) -> None:
        self.assertEqual(validate(ROOT), [])

    def test_prompts_include_only_preceding_visible_instructions(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            exp_dir = Path(directory) / "SyntheticStudy" / "exp1"
            exp_dir.mkdir(parents=True)
            (exp_dir / "config.json").write_text(json.dumps({
                "experimentName": "Instruction scope test",
                "description": "",
                "taskType": ["test"],
                "responseType": ["single-slider"],
                "stimuli_count": 2,
                "experimentFlow": [{
                    "condition": "default",
                    "sequences": [{
                        "seq_id": "seq_1",
                        "blocks": [["instruction_1"], ["trial_1"], ["instruction_2", "break"], ["trial_2"]],
                    }],
                }],
            }))
            instructions = [
                {"id": "instruction_1", "type": "instruction", "text": "FIRST INSTRUCTION"},
                {"id": "instruction_2", "type": "instruction", "text": "SECOND INSTRUCTION"},
                {
                    "id": "break",
                    "type": "instruction",
                    "text": "PRESENTATION ONLY",
                    "include_in_model_prompt": False,
                },
            ]
            (exp_dir / "instruction.jsonl").write_text(
                "\n".join(json.dumps(item) for item in instructions) + "\n"
            )
            trials = [
                {
                    "id": trial_id,
                    "stimuli": [{"input_type": "text", "text": trial_id}],
                    "queries": [{
                        "prompt": "Rate it.",
                        "type": "single-slider",
                        "tag": "rating",
                        "slider_config": {"min": 0, "max": 100},
                    }],
                }
                for trial_id in ("trial_1", "trial_2")
            ]
            (exp_dir / "trial.jsonl").write_text(
                "\n".join(json.dumps(item) for item in trials) + "\n"
            )
            (exp_dir / "human_data_mean.json").write_text("{}")

            experiment = load_experiment(exp_dir)
            trial_1, trial_2 = experiment.experiment_trials()
            _, first_messages = build_messages(trial_1, experiment, refs_only=True)
            _, second_messages = build_messages(trial_2, experiment, refs_only=True)
            first_prompt = first_messages[0]["content"]
            second_prompt = second_messages[0]["content"]

            self.assertIn("FIRST INSTRUCTION", first_prompt)
            self.assertNotIn("SECOND INSTRUCTION", first_prompt)
            self.assertIn("FIRST INSTRUCTION", second_prompt)
            self.assertIn("SECOND INSTRUCTION", second_prompt)
            self.assertNotIn("PRESENTATION ONLY", second_prompt)


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("evaluate_agent_runs", ROOT / "scripts/evaluate_agent_runs.py")
if spec is None or spec.loader is None:
    raise RuntimeError("evaluation module unavailable")
evaluation = importlib.util.module_from_spec(spec)
spec.loader.exec_module(evaluation)

CASES = [
    {"id": "small", "must_use": [], "must_not_use": ["big-skill"]},
    {"id": "debug", "must_use": ["debug-skill"], "must_not_use": []},
]


def record(variant="baseline", case="debug", **changes):
    r = {
        "case_id": case, "runtime": "codex", "model": "model-a", "environment": "linux",
        "trial": 1, "variant": variant, "outcome": "unknown",
        "loaded_skills": [], "trace_checked": True,
    }
    r.update(changes)
    return r


class EvaluationTests(unittest.TestCase):
    def test_paired_usage_and_routing(self):
        a = record(input_tokens=100, output_tokens=20)
        b = record("skills", input_tokens=70, output_tokens=20, loaded_skills=["debug-skill"])
        pair = evaluation.evaluate([a, b], CASES)["pairs"][0]
        self.assertEqual(pair["token_delta"], -30)
        self.assertEqual(pair["routing"], "pass")

    def test_never_invents_missing_tokens_or_route(self):
        pair = evaluation.evaluate(
            [record(), record("skills", trace_checked=False, loaded_skills=["debug-skill"])],
            CASES,
        )["pairs"][0]
        self.assertIsNone(pair["token_delta"])
        self.assertEqual(pair["routing"], "unknown")

    def test_reports_false_activation(self):
        pair = evaluation.evaluate(
            [record(case="small"), record("skills", case="small", loaded_skills=["big-skill"])],
            CASES,
        )["pairs"][0]
        self.assertEqual(pair["routing"], "fail")

    def test_baseline_with_skills_is_contaminated(self):
        pair = evaluation.evaluate(
            [record(loaded_skills=["debug-skill"]), record("skills", loaded_skills=["debug-skill"])],
            CASES,
        )["pairs"][0]
        self.assertEqual(pair["routing"], "contaminated-baseline")

    def test_does_not_pair_different_models(self):
        report = evaluation.evaluate([record(), record("skills", model="other")], CASES)
        self.assertEqual({x["status"] for x in report["pairs"]}, {"unpaired"})

    def test_requires_evidence_for_reported_pass(self):
        with self.assertRaisesRegex(ValueError, "evidence"):
            evaluation.evaluate([record(outcome="pass")], CASES)

    def test_rejects_duplicate_variant(self):
        with self.assertRaisesRegex(ValueError, "duplicate variant"):
            evaluation.evaluate([record(), record()], CASES)

    def test_rejects_bool_for_token_counter(self):
        with self.assertRaisesRegex(ValueError, "input_tokens"):
            evaluation.evaluate([record(input_tokens=True)], CASES)

    def test_markdown_keeps_unknown_usage_explicit(self):
        report = evaluation.evaluate([record(), record("skills")], CASES)
        self.assertIn("unknown", evaluation.markdown(report))


if __name__ == "__main__":
    unittest.main()

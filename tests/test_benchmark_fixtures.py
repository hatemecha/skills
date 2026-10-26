from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("prepare_eval_case", ROOT / "scripts/prepare_eval_case.py")
if spec is None or spec.loader is None:
    raise RuntimeError("preparation module unavailable")
preparation = importlib.util.module_from_spec(spec)
spec.loader.exec_module(preparation)


class FixtureTests(unittest.TestCase):
    def test_baseline_states_are_intentional(self):
        cases = json.loads((ROOT / "evals" / "benchmark-cases.json").read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as root:
            for case in cases:
                with self.subTest(case=case["id"]):
                    target = preparation.prepare(case["id"], "baseline", Path(root))
                    result = subprocess.run(
                        [sys.executable, "-m", "unittest", "discover", "-s", ".", "-p", "test_*.py"],
                        cwd=target, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                        text=True, timeout=15,
                    )
                    expected = case["baseline_tests"]
                    self.assertEqual(result.returncode == 0, expected == "pass", result.stderr)

    def test_prepare_never_overwrites_existing_workspace(self):
        with tempfile.TemporaryDirectory() as root:
            output = Path(root)
            preparation.prepare("regression", "skills", output)
            with self.assertRaises(FileExistsError):
                preparation.prepare("regression", "skills", output)


if __name__ == "__main__":
    unittest.main()

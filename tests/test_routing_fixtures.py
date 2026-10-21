from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class RoutingFixtureTests(unittest.TestCase):
    def test_fixtures_have_consistent_skill_ids(self):
        catalog = {p.name for p in (ROOT / "skills").iterdir() if (p / "SKILL.md").is_file()}
        cases = json.loads((ROOT / "evals" / "routing-cases.json").read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(cases), 8)
        ids = [c["id"] for c in cases]
        self.assertEqual(len(ids), len(set(ids)))
        for case in cases:
            with self.subTest(case=case["id"]):
                self.assertTrue(case["prompt"].strip())
                self.assertTrue(case["success"].strip())
                lists = [case[key] for key in ("must_use", "may_use", "must_not_use")]
                for values in lists:
                    self.assertTrue(set(values) <= catalog)
                    self.assertEqual(len(values), len(set(values)))
                self.assertEqual(sum(map(len, lists)), len(set().union(*map(set, lists))))
        self.assertTrue(set.union(*(set(c["must_use"]) for c in cases)) <= catalog)

"""Catalog regression checks; runtime behavior is evaluated separately."""

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("catalog_validator", ROOT / "scripts" / "validate_skills.py")
assert spec and spec.loader
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class CatalogTests(unittest.TestCase):
    def test_current_catalog(self):
        self.assertEqual(validator.validate(ROOT), [])

    def test_missing_license_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "skills" / "sample").mkdir(parents=True)
            (root / "LICENSE").write_text("MIT test license\n", encoding="utf-8")
            (root / "skills" / "sample" / "SKILL.md").write_text(
                "---\nname: sample\ndescription: Example\nlicense: MIT\n---\n",
                encoding="utf-8",
            )
            (root / "skills.sh.json").write_text(
                json.dumps({"groupings": [{"skills": ["sample"]}]}),
                encoding="utf-8",
            )
            self.assertTrue(any("LICENSE.txt" in error for error in validator.validate(root)))


if __name__ == "__main__":
    unittest.main()

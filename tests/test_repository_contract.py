from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
EXPECTED_SKILLS = {
    "open-source-engineering",
    "open-source-project",
    "orchestrating-engineering-agents",
}
IGNORED_DIRS = {".git", ".venv", "venv", "node_modules", "__pycache__"}


class PackagingContractTests(unittest.TestCase):
    def test_only_catalog_skills_are_discoverable(self) -> None:
        discovered = {
            path.parent.name
            for path in ROOT.rglob("SKILL.md")
            if not any(part in IGNORED_DIRS for part in path.relative_to(ROOT).parts)
        }
        self.assertEqual(discovered, EXPECTED_SKILLS)

    def test_each_skill_bundles_the_mit_license(self) -> None:
        root_license = (ROOT / "LICENSE").read_text(encoding="utf-8")
        for skill_name in EXPECTED_SKILLS:
            with self.subTest(skill=skill_name):
                skill_dir = SKILLS / skill_name
                skill_text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
                self.assertRegex(skill_text, r"(?m)^license:\s*MIT\s*$")
                self.assertEqual(
                    (skill_dir / "LICENSE.txt").read_text(encoding="utf-8"),
                    root_license,
                )

    def test_portable_markdown_has_no_dollar_prefixed_skill_invocation(self) -> None:
        violations: list[str] = []
        for path in SKILLS.rglob("*.md"):
            if "agents" in path.parts:
                continue
            if re.search(r"\$[a-z][a-z0-9-]+", path.read_text(encoding="utf-8")):
                violations.append(str(path.relative_to(ROOT)))
        self.assertEqual(violations, [])

    def test_template_bundles_license_notice(self) -> None:
        template_license = ROOT / "template" / "LICENSE.txt"
        self.assertTrue(template_license.is_file())
        self.assertEqual(
            template_license.read_text(encoding="utf-8"),
            (ROOT / "LICENSE").read_text(encoding="utf-8"),
        )


class SafetyContractTests(unittest.TestCase):
    def test_repository_execution_skills_define_trust_gate(self) -> None:
        for skill_name in ("open-source-engineering", "open-source-project"):
            with self.subTest(skill=skill_name):
                text = (SKILLS / skill_name / "SKILL.md").read_text(encoding="utf-8")
                self.assertIn("## Trust and execution safety", text)
                self.assertIn("untrusted data", text)
                self.assertIn("credentials", text)
                self.assertIn("isolated", text)

    def test_open_source_project_modes_define_write_permissions(self) -> None:
        text = (SKILLS / "open-source-project" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Audit is read-only by default.", text)
        self.assertIn("Publish does not authorize commits, pushes, releases", text)
        self.assertIn("revoke or rotate", text)

    def test_engineering_review_and_design_are_read_only_by_default(self) -> None:
        text = (SKILLS / "open-source-engineering" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("Review and Design are read-only by default.", text)

    def test_orchestrator_defines_capability_and_trust_gate(self) -> None:
        text = (SKILLS / "orchestrating-engineering-agents" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("## Capability and trust gate", text)
        self.assertIn("untrusted data", text)
        self.assertIn("NEEDS_HUMAN", text)
        self.assertIn("BLOCKED", text)


if __name__ == "__main__":
    unittest.main()

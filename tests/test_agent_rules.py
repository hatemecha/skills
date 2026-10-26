from __future__ import annotations

import importlib.util
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("install_agent_rules", ROOT / "scripts" / "install_agent_rules.py")
if spec is None or spec.loader is None:
    raise RuntimeError("installer module unavailable")
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)
POLICY = "# Engineering baseline\n\nUse relevant installed skills.\n"


class ManagedPolicyTests(unittest.TestCase):
    def test_preview_never_writes_and_apply_is_idempotent(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "nested" / "AGENTS.md"
            self.assertEqual(installer.install(target, POLICY), "create")
            self.assertFalse(target.exists())
            self.assertEqual(installer.install(target, POLICY, apply=True), "create")
            content = target.read_text(encoding="utf-8")
            self.assertEqual(content.count(installer.START), 1)
            self.assertEqual(installer.install(target, POLICY, apply=True), "unchanged")
            self.assertEqual(target.read_text(encoding="utf-8"), content)

    def test_preserves_unmanaged_content_on_update(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "AGENTS.md"
            target.write_text("# Existing project preference\n", encoding="utf-8")
            installer.install(target, POLICY, apply=True)
            installer.install(target, "# Updated baseline", apply=True)
            content = target.read_text(encoding="utf-8")
            self.assertTrue(content.startswith("# Existing project preference\n"))
            self.assertEqual(content.count(installer.START), 1)
            self.assertIn("# Updated baseline", content)
            self.assertNotIn("Use relevant installed skills.", content)

    def test_refuses_partial_markers_without_modifying(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "AGENTS.md"
            original = "Existing\n" + installer.START
            target.write_text(original, encoding="utf-8")
            with self.assertRaises(ValueError):
                installer.install(target, POLICY, apply=True)
            self.assertEqual(target.read_text(encoding="utf-8"), original)

    def test_codex_home_is_respected(self):
        with tempfile.TemporaryDirectory() as temp:
            with patch.dict("os.environ", {"CODEX_HOME": temp}):
                self.assertEqual(installer.target_paths()["codex"], Path(temp) / "AGENTS.md")

    def test_codex_override_detection(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "AGENTS.md"
            override = Path(temp) / "AGENTS.override.md"
            self.assertIsNone(installer.shadowing_codex_override(path))
            override.write_text("   \n", encoding="utf-8")
            self.assertIsNone(installer.shadowing_codex_override(path))
            override.write_text("# Active custom rules\n", encoding="utf-8")
            self.assertEqual(installer.shadowing_codex_override(path), override)

    def test_refuses_symlink(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            real = root / "real.md"
            real.write_text("preserve", encoding="utf-8")
            target = root / "link.md"
            try:
                target.symlink_to(real)
            except (OSError, NotImplementedError):
                self.skipTest("symlinks not available")
            with self.assertRaises(ValueError):
                installer.install(target, POLICY, apply=True)
            self.assertEqual(real.read_text(encoding="utf-8"), "preserve")

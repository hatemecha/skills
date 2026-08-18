from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_discovery.py"
EXPECTED = {
    "open-source-engineering",
    "open-source-project",
    "orchestrating-engineering-agents",
}

spec = importlib.util.spec_from_file_location("check_discovery", SCRIPT)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Could not load {SCRIPT}")
check_discovery = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check_discovery)


def create_installed_catalog(root: Path, names: set[str]) -> Path:
    catalog = root / ".agents" / "skills"
    for name in names:
        skill_dir = catalog / name
        (skill_dir / "agents").mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text("# Installed\n", encoding="utf-8")
        (skill_dir / "LICENSE.txt").write_text("MIT License\n", encoding="utf-8")
        (skill_dir / "agents" / "openai.yaml").write_text(
            "interface: {}\n", encoding="utf-8"
        )
    return catalog


class InstalledCatalogTests(unittest.TestCase):
    def test_catalog_validator_exists(self) -> None:
        self.assertTrue(hasattr(check_discovery, "validate_installed_catalog"))

    def test_accepts_exact_installed_catalog(self) -> None:
        self.assertTrue(hasattr(check_discovery, "validate_installed_catalog"))
        with tempfile.TemporaryDirectory() as tempdir:
            catalog = create_installed_catalog(Path(tempdir), EXPECTED)
            check_discovery.validate_installed_catalog(catalog, EXPECTED)

    def test_rejects_extra_template_skill(self) -> None:
        self.assertTrue(hasattr(check_discovery, "validate_installed_catalog"))
        with tempfile.TemporaryDirectory() as tempdir:
            catalog = create_installed_catalog(
                Path(tempdir), EXPECTED | {"example-skill"}
            )
            with self.assertRaisesRegex(ValueError, "unexpected installed skills"):
                check_discovery.validate_installed_catalog(catalog, EXPECTED)

    def test_rejects_missing_expected_skill(self) -> None:
        self.assertTrue(hasattr(check_discovery, "validate_installed_catalog"))
        with tempfile.TemporaryDirectory() as tempdir:
            catalog = create_installed_catalog(
                Path(tempdir), EXPECTED - {"open-source-engineering"}
            )
            with self.assertRaisesRegex(ValueError, "missing installed skills"):
                check_discovery.validate_installed_catalog(catalog, EXPECTED)

    def test_rejects_missing_installed_license(self) -> None:
        self.assertTrue(hasattr(check_discovery, "validate_installed_catalog"))
        with tempfile.TemporaryDirectory() as tempdir:
            catalog = create_installed_catalog(Path(tempdir), EXPECTED)
            (catalog / "open-source-project" / "LICENSE.txt").unlink()
            with self.assertRaisesRegex(ValueError, "missing installed file"):
                check_discovery.validate_installed_catalog(catalog, EXPECTED)

    def test_allows_optional_adapter_to_be_absent(self) -> None:
        self.assertTrue(hasattr(check_discovery, "validate_installed_catalog"))
        with tempfile.TemporaryDirectory() as tempdir:
            catalog = create_installed_catalog(Path(tempdir), EXPECTED)
            for skill_name in EXPECTED:
                adapter = catalog / skill_name / "agents" / "openai.yaml"
                adapter.unlink()
            try:
                check_discovery.validate_installed_catalog(catalog, EXPECTED)
            except ValueError as exc:
                self.fail(f"optional adapters must not be required: {exc}")

    def test_rejects_tampered_installed_content(self) -> None:
        self.assertTrue(hasattr(check_discovery, "validate_installed_catalog"))
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            source = create_installed_catalog(root / "source", EXPECTED)
            installed = create_installed_catalog(root / "installed", EXPECTED)
            (installed / "open-source-project" / "SKILL.md").write_text(
                "# Tampered\n", encoding="utf-8"
            )
            with self.assertRaisesRegex(ValueError, "content mismatch"):
                check_discovery.validate_installed_catalog(installed, EXPECTED, source)

    def test_rejects_unexpected_installed_file(self) -> None:
        self.assertTrue(hasattr(check_discovery, "validate_installed_catalog"))
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            source = create_installed_catalog(root / "source", EXPECTED)
            installed = create_installed_catalog(root / "installed", EXPECTED)
            (installed / "open-source-project" / "unexpected.txt").write_text(
                "unexpected\n", encoding="utf-8"
            )
            with self.assertRaisesRegex(
                ValueError, "unexpected installed source files"
            ):
                check_discovery.validate_installed_catalog(installed, EXPECTED, source)


if __name__ == "__main__":
    unittest.main()

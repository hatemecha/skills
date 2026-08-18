from __future__ import annotations

import contextlib
import importlib.util
import io
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = REPO_ROOT / "scripts" / "validate_skills.py"

spec = importlib.util.spec_from_file_location("validate_skills", VALIDATOR_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Could not load validator from {VALIDATOR_PATH}")
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class ValidatorRoot:
    def __init__(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        self.old_root = getattr(validator, "ROOT")
        self.old_skills_dir = getattr(validator, "SKILLS_DIR")

    def __enter__(self) -> Path:
        setattr(validator, "ROOT", self.root)
        setattr(validator, "SKILLS_DIR", self.root / "skills")
        getattr(validator, "SKILLS_DIR").mkdir()
        return self.root

    def __exit__(self, *args: object) -> None:
        setattr(validator, "ROOT", self.old_root)
        setattr(validator, "SKILLS_DIR", self.old_skills_dir)
        self.tempdir.cleanup()


def create_skill(
    root: Path,
    name: str,
    frontmatter: str,
    body: str = "# Test\n",
    *,
    include_license: bool = True,
) -> Path:
    skill_dir = root / "skills" / name
    skill_dir.mkdir(parents=True)
    if include_license:
        frontmatter += "\nlicense: MIT"
        (skill_dir / "LICENSE.txt").write_text("MIT License\n", encoding="utf-8")
    (skill_dir / "SKILL.md").write_text(
        f"---\n{frontmatter}\n---\n\n{body}", encoding="utf-8"
    )
    return skill_dir


class FrontmatterValidationTests(unittest.TestCase):
    def test_accepts_folded_yaml_description(self) -> None:
        with ValidatorRoot() as root:
            skill_dir = create_skill(
                root,
                "folded-description",
                "name: folded-description\ndescription: >\n  Valid YAML can span\n  multiple lines.",
            )
            self.assertEqual(validator.validate_skill(skill_dir), [])

    def test_rejects_malformed_yaml(self) -> None:
        with ValidatorRoot() as root:
            skill_dir = create_skill(
                root,
                "malformed-yaml",
                'name: malformed-yaml\ndescription: "unterminated',
            )
            self.assertTrue(validator.validate_skill(skill_dir))

    def test_rejects_duplicate_frontmatter_keys(self) -> None:
        with ValidatorRoot() as root:
            skill_dir = create_skill(
                root,
                "duplicate-key",
                "name: duplicate-key\nname: duplicate-key\ndescription: Duplicate keys are invalid.",
            )
            self.assertTrue(validator.validate_skill(skill_dir))

    def test_rejects_name_over_64_characters(self) -> None:
        with ValidatorRoot() as root:
            name = "a" * 65
            skill_dir = create_skill(
                root, name, f"name: {name}\ndescription: Too long."
            )
            self.assertTrue(validator.validate_skill(skill_dir))

    def test_rejects_description_over_1024_characters(self) -> None:
        with ValidatorRoot() as root:
            skill_dir = create_skill(
                root,
                "long-description",
                "name: long-description\ndescription: " + ("x" * 1025),
            )
            self.assertTrue(validator.validate_skill(skill_dir))

    def test_rejects_unknown_root_field(self) -> None:
        with ValidatorRoot() as root:
            skill_dir = create_skill(
                root,
                "unknown-field",
                "name: unknown-field\ndescription: Unknown field.\nvendor-magic: enabled",
            )
            self.assertTrue(validator.validate_skill(skill_dir))

    def test_rejects_non_scalar_mapping_key_without_crashing(self) -> None:
        with ValidatorRoot() as root:
            skill_dir = create_skill(
                root,
                "complex-key",
                "? [unsupported, key]\n: value\n"
                "name: complex-key\ndescription: Invalid mapping key.",
            )
            self.assertTrue(validator.validate_skill(skill_dir))

    def test_allows_evals_directory(self) -> None:
        with ValidatorRoot() as root:
            skill_dir = create_skill(
                root,
                "with-evals",
                "name: with-evals\ndescription: Includes evaluations.",
            )
            (skill_dir / "evals").mkdir()
            (skill_dir / "evals" / "evals.json").write_text("{}\n", encoding="utf-8")
            self.assertEqual(validator.validate_skill(skill_dir), [])

    def test_requires_license_field(self) -> None:
        with ValidatorRoot() as root:
            skill_dir = create_skill(
                root,
                "missing-license",
                "name: missing-license\ndescription: Missing license.",
                include_license=False,
            )
            self.assertTrue(validator.validate_skill(skill_dir))

    def test_requires_bundled_license_notice(self) -> None:
        with ValidatorRoot() as root:
            skill_dir = create_skill(
                root,
                "missing-notice",
                "name: missing-notice\ndescription: Missing notice.",
            )
            (skill_dir / "LICENSE.txt").unlink()
            self.assertTrue(validator.validate_skill(skill_dir))


class AdapterValidationTests(unittest.TestCase):
    def test_rejects_invalid_openai_adapter(self) -> None:
        with ValidatorRoot() as root:
            skill_dir = create_skill(
                root,
                "bad-adapter",
                "name: bad-adapter\ndescription: Has an invalid adapter.",
            )
            adapter_dir = skill_dir / "agents"
            adapter_dir.mkdir()
            (adapter_dir / "openai.yaml").write_text(
                "interface:\n  display_name: Bad Adapter\n  short_description: short\n"
                "  default_prompt: Does not name the skill.\n",
                encoding="utf-8",
            )
            self.assertTrue(validator.validate_skill(skill_dir))

    def test_accepts_policy_only_openai_adapter(self) -> None:
        with ValidatorRoot() as root:
            skill_dir = create_skill(
                root,
                "policy-adapter",
                "name: policy-adapter\ndescription: Uses invocation policy.",
            )
            adapter_dir = skill_dir / "agents"
            adapter_dir.mkdir()
            (adapter_dir / "openai.yaml").write_text(
                "policy:\n  allow_implicit_invocation: false\n",
                encoding="utf-8",
            )
            self.assertEqual(validator.validate_skill(skill_dir), [])

    def test_accepts_documented_policy_and_tool_dependencies(self) -> None:
        with ValidatorRoot() as root:
            skill_dir = create_skill(
                root,
                "full-adapter",
                "name: full-adapter\ndescription: Uses documented adapter fields.",
            )
            adapter_dir = skill_dir / "agents"
            adapter_dir.mkdir()
            (adapter_dir / "openai.yaml").write_text(
                "policy:\n  allow_implicit_invocation: false\n"
                "dependencies:\n  tools:\n"
                "    - type: mcp\n"
                "      value: github\n"
                "      description: GitHub MCP server\n"
                "      transport: streamable_http\n"
                "      url: https://example.com/mcp\n",
                encoding="utf-8",
            )
            self.assertEqual(validator.validate_skill(skill_dir), [])

    def test_rejects_duplicate_adapter_key(self) -> None:
        with ValidatorRoot() as root:
            skill_dir = create_skill(
                root,
                "duplicate-adapter-key",
                "name: duplicate-adapter-key\ndescription: Duplicates adapter keys.",
            )
            adapter_dir = skill_dir / "agents"
            adapter_dir.mkdir()
            (adapter_dir / "openai.yaml").write_text(
                "policy:\n"
                "  allow_implicit_invocation: false\n"
                "  allow_implicit_invocation: true\n",
                encoding="utf-8",
            )
            self.assertTrue(validator.validate_skill(skill_dir))

    def test_rejects_non_list_adapter_tools(self) -> None:
        with ValidatorRoot() as root:
            skill_dir = create_skill(
                root,
                "bad-tools",
                "name: bad-tools\ndescription: Has malformed tool dependencies.",
            )
            adapter_dir = skill_dir / "agents"
            adapter_dir.mkdir()
            (adapter_dir / "openai.yaml").write_text(
                "interface:\n"
                "  display_name: Bad Tools\n"
                "  short_description: Malformed tool dependencies\n"
                "  default_prompt: Use $bad-tools for this task.\n"
                "dependencies:\n  tools: github\n",
                encoding="utf-8",
            )
            errors = validator.validate_skill(skill_dir)
            self.assertTrue(any("dependencies.tools" in error for error in errors))

    def test_rejects_non_string_nested_adapter_key_without_crashing(self) -> None:
        with ValidatorRoot() as root:
            skill_dir = create_skill(
                root,
                "numeric-policy-key",
                "name: numeric-policy-key\ndescription: Has an invalid policy key.",
            )
            adapter_dir = skill_dir / "agents"
            adapter_dir.mkdir()
            (adapter_dir / "openai.yaml").write_text(
                "policy:\n  1: false\n",
                encoding="utf-8",
            )
            self.assertTrue(validator.validate_skill(skill_dir))


class ContainmentValidationTests(unittest.TestCase):
    def test_rejects_symlinked_license_notice(self) -> None:
        with ValidatorRoot() as root:
            skill_dir = create_skill(
                root,
                "linked-license",
                "name: linked-license\ndescription: Has a linked license.",
            )
            outside_notice = root / "outside-license.txt"
            outside_notice.write_text("MIT License\n", encoding="utf-8")
            (skill_dir / "LICENSE.txt").unlink()
            (skill_dir / "LICENSE.txt").symlink_to(outside_notice)
            errors = validator.validate_skill(skill_dir)
            self.assertTrue(any("symlink" in error for error in errors))

    def test_rejects_file_uri_in_markdown(self) -> None:
        with ValidatorRoot() as root:
            skill_dir = create_skill(
                root,
                "file-uri",
                "name: file-uri\ndescription: Contains an unsafe URI.",
                body="# Unsafe\n\n[host file](file:///etc/passwd)\n",
            )
            errors = validator.validate_skill(skill_dir)
            self.assertTrue(any("unsupported URI scheme" in error for error in errors))

    def test_rejects_javascript_uri_in_markdown(self) -> None:
        with ValidatorRoot() as root:
            skill_dir = create_skill(
                root,
                "javascript-uri",
                "name: javascript-uri\ndescription: Contains an active URI.",
                body="# Unsafe\n\n[active link](javascript:alert(1))\n",
            )
            errors = validator.validate_skill(skill_dir)
            self.assertTrue(any("unsupported URI scheme" in error for error in errors))

    def test_rejects_file_uri_in_reference_link(self) -> None:
        with ValidatorRoot() as root:
            skill_dir = create_skill(
                root,
                "reference-uri",
                "name: reference-uri\ndescription: Contains an unsafe reference URI.",
                body="# Unsafe\n\n[host file][target]\n\n[target]: file:///etc/passwd\n",
            )
            errors = validator.validate_skill(skill_dir)
            self.assertTrue(any("unsupported URI scheme" in error for error in errors))

    def test_rejects_javascript_autolink(self) -> None:
        with ValidatorRoot() as root:
            skill_dir = create_skill(
                root,
                "autolink-uri",
                "name: autolink-uri\ndescription: Contains an unsafe autolink.",
                body="# Unsafe\n\n<javascript:alert(1)>\n",
            )
            errors = validator.validate_skill(skill_dir)
            self.assertTrue(any("unsupported URI scheme" in error for error in errors))

    def test_rejects_javascript_html_attribute(self) -> None:
        with ValidatorRoot() as root:
            skill_dir = create_skill(
                root,
                "html-uri",
                "name: html-uri\ndescription: Contains unsafe inline HTML.",
                body='# Unsafe\n\n<a href="javascript:alert(1)">click</a>\n',
            )
            errors = validator.validate_skill(skill_dir)
            self.assertTrue(any("unsupported URI scheme" in error for error in errors))

    def test_rejects_nested_label_javascript_link(self) -> None:
        with ValidatorRoot() as root:
            skill_dir = create_skill(
                root,
                "nested-label-uri",
                "name: nested-label-uri\ndescription: Contains a nested unsafe link.",
                body="# Unsafe\n\n[outer [inner]](javascript:alert(1))\n",
            )
            errors = validator.validate_skill(skill_dir)
            self.assertTrue(any("unsupported URI scheme" in error for error in errors))

    def test_rejects_escaped_label_file_link(self) -> None:
        with ValidatorRoot() as root:
            skill_dir = create_skill(
                root,
                "escaped-label-uri",
                "name: escaped-label-uri\ndescription: Contains an escaped unsafe link.",
                body="# Unsafe\n\n[escaped \\]](file:///etc/passwd)\n",
            )
            errors = validator.validate_skill(skill_dir)
            self.assertTrue(any("unsupported URI scheme" in error for error in errors))

    def test_rejects_unsafe_uri_in_srcset(self) -> None:
        with ValidatorRoot() as root:
            skill_dir = create_skill(
                root,
                "srcset-uri",
                "name: srcset-uri\ndescription: Contains an unsafe srcset URI.",
                body=(
                    '# Unsafe\n\n<img srcset="https://example.com/a.png 1x, '
                    'file:///etc/passwd 2x">\n'
                ),
            )
            errors = validator.validate_skill(skill_dir)
            self.assertTrue(any("unsupported URI scheme" in error for error in errors))

    def test_rejects_unsafe_uri_in_namespaced_html_attribute(self) -> None:
        with ValidatorRoot() as root:
            skill_dir = create_skill(
                root,
                "xlink-uri",
                "name: xlink-uri\ndescription: Contains an unsafe xlink URI.",
                body=(
                    '# Unsafe\n\n<svg><a xlink:href="javascript:alert(1)">x</a></svg>\n'
                ),
            )
            errors = validator.validate_skill(skill_dir)
            self.assertTrue(any("unsupported URI scheme" in error for error in errors))

    def test_rejects_backslash_escaped_javascript_scheme(self) -> None:
        with ValidatorRoot() as root:
            skill_dir = create_skill(
                root,
                "escaped-scheme",
                "name: escaped-scheme\ndescription: Escapes an unsafe URI scheme.",
                body="# Unsafe\n\n[x](javascript\\:alert(1))\n",
            )
            errors = validator.validate_skill(skill_dir)
            self.assertTrue(any("unsupported URI scheme" in error for error in errors))

    def test_rejects_entity_encoded_javascript_scheme(self) -> None:
        with ValidatorRoot() as root:
            skill_dir = create_skill(
                root,
                "entity-scheme",
                "name: entity-scheme\ndescription: Encodes an unsafe URI scheme.",
                body="# Unsafe\n\n[x](javascript&#x3A;alert(1))\n",
            )
            errors = validator.validate_skill(skill_dir)
            self.assertTrue(any("unsupported URI scheme" in error for error in errors))


class RepositoryDiscoveryTests(unittest.TestCase):
    def test_main_rejects_discoverable_skill_outside_skills_directory(self) -> None:
        with ValidatorRoot() as root:
            create_skill(
                root, "real-skill", "name: real-skill\ndescription: Real skill."
            )
            template = root / "template"
            template.mkdir()
            (template / "SKILL.md").write_text(
                "---\nname: example-skill\ndescription: Accidental skill.\n---\n# Template\n",
                encoding="utf-8",
            )
            with (
                contextlib.redirect_stdout(io.StringIO()),
                contextlib.redirect_stderr(io.StringIO()),
            ):
                self.assertEqual(validator.main(), 1)

    def test_main_ignores_virtual_environment_contents(self) -> None:
        with ValidatorRoot() as root:
            create_skill(
                root, "real-skill", "name: real-skill\ndescription: Real skill."
            )
            dependency_skill = root / ".venv" / "lib" / "dependency"
            dependency_skill.mkdir(parents=True)
            (dependency_skill / "SKILL.md").write_text(
                "---\nname: dependency\ndescription: Installed dependency.\n---\n# Dependency\n",
                encoding="utf-8",
            )
            with (
                contextlib.redirect_stdout(io.StringIO()),
                contextlib.redirect_stderr(io.StringIO()),
            ):
                self.assertEqual(validator.main(), 0)


if __name__ == "__main__":
    unittest.main()

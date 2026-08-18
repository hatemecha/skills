#!/usr/bin/env python3
"""Validate Agent Skills plus this repository's portability contract."""

from __future__ import annotations

import re
import string
import sys
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse

try:
    import yaml
    from yaml.constructor import ConstructorError
except ImportError as exc:  # pragma: no cover - exercised by contributor setup
    raise SystemExit(
        "PyYAML is required. Install development dependencies with "
        "`python -m pip install -r requirements-dev.txt`."
    ) from exc

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
REFERENCE_LINK_RE = re.compile(r"(?m)^[ \t]{0,3}\[[^\]\n]+\]:\s*(?:<([^>]+)>|([^\s]+))")
AUTOLINK_RE = re.compile(r"<([A-Za-z][A-Za-z0-9+.-]*:[^<>\s]+)>")
ACTIVE_SCRIPT_URI_RE = re.compile(r"(?i)\b((?:javascript|vbscript):[^\s<>\"']*)")
FILE_DATA_LINK_RE = re.compile(
    r"(?ix)(?:\]\s*\(\s*|\[[^\n]*\]:\s*|<)\s*((?:file|data):[^\s<>\)]*)"
)
COMMONMARK_ESCAPE_RE = re.compile(r"\\([" + re.escape(string.punctuation) + r"])")
ALLOWED_FRONTMATTER_FIELDS = {
    "name",
    "description",
    "license",
    "compatibility",
    "metadata",
    "allowed-tools",
}
ALLOWED_SUPPORT_DIRS = {"agents", "assets", "evals", "references", "scripts"}
FORBIDDEN_SKILL_DOCS = {"README.md", "CHANGELOG.md"}
MAX_NAME_LENGTH = 64
MAX_DESCRIPTION_LENGTH = 1024
MAX_COMPATIBILITY_LENGTH = 500
OPENAI_INTERFACE_FIELDS = {
    "display_name",
    "short_description",
    "icon_small",
    "icon_large",
    "brand_color",
    "default_prompt",
}
OPENAI_POLICY_FIELDS = {"allow_implicit_invocation"}
OPENAI_DEPENDENCY_FIELDS = {"tools"}
OPENAI_TOOL_FIELDS = {"type", "value", "description", "transport", "url"}
SAFE_EXTERNAL_URI_SCHEMES = {"http", "https", "mailto"}
HTML_URI_ATTRIBUTES = {
    "action",
    "background",
    "cite",
    "data",
    "formaction",
    "href",
    "poster",
    "src",
    "xlink:href",
}
IGNORED_DISCOVERY_DIRS = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "node_modules",
    "venv",
}


class UniqueKeyLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects duplicate mapping keys."""


def _construct_unique_mapping(
    loader: UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False
) -> dict[Any, Any]:
    loader.flatten_mapping(node)
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            hash(key)
        except TypeError as exc:
            raise ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                "found an unsupported non-scalar mapping key",
                key_node.start_mark,
            ) from exc
        if key in mapping:
            raise ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                f"found duplicate key {key!r}",
                key_node.start_mark,
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_unique_mapping,
)


class HtmlUriTargetParser(HTMLParser):
    """Collect URI-bearing attributes from inline HTML in Markdown."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.targets: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        del tag
        for name, value in attrs:
            if value is None:
                continue
            normalized_name = name.lower()
            if normalized_name == "srcset":
                self.targets.extend(
                    candidate.strip().split()[0]
                    for candidate in value.split(",")
                    if candidate.strip()
                )
            elif normalized_name in HTML_URI_ATTRIBUTES:
                self.targets.append(value)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)


def _relative(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def _load_yaml_mapping(
    text: str, path: Path, label: str
) -> tuple[dict[str, Any], list[str]]:
    try:
        # UniqueKeyLoader subclasses SafeLoader and only adds duplicate-key rejection.
        loaded = yaml.load(  # nosec B506
            text, Loader=UniqueKeyLoader
        )
    except yaml.YAMLError as exc:
        return {}, [f"{_relative(path)}: invalid YAML in {label}: {exc}"]
    if not isinstance(loaded, dict):
        return {}, [f"{_relative(path)}: {label} must be a YAML mapping"]
    if not all(isinstance(key, str) for key in loaded):
        return {}, [f"{_relative(path)}: {label} keys must be strings"]
    return loaded, []


def parse_frontmatter(path: Path) -> tuple[dict[str, Any], list[str]]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    if not lines or lines[0] != "---":
        return {}, [
            f"{_relative(path)}: SKILL.md must start with exact YAML delimiter '---'"
        ]

    try:
        end = next(i for i, line in enumerate(lines[1:], start=1) if line == "---")
    except StopIteration:
        return {}, [f"{_relative(path)}: missing closing YAML frontmatter delimiter"]

    frontmatter = "\n".join(lines[1:end])
    return _load_yaml_mapping(frontmatter, path, "frontmatter")


def _validate_optional_string(
    metadata: dict[str, Any], field: str, path: Path, *, max_length: int | None = None
) -> list[str]:
    if field not in metadata:
        return []
    value = metadata[field]
    if not isinstance(value, str) or not value.strip():
        return [f"{_relative(path)}: '{field}' must be a non-empty string"]
    if max_length is not None and len(value) > max_length:
        return [
            f"{_relative(path)}: '{field}' exceeds {max_length} characters "
            f"({len(value)} chars)"
        ]
    return []


def validate_frontmatter(skill_dir: Path, metadata: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    skill_file = skill_dir / "SKILL.md"

    unexpected = sorted(set(metadata) - ALLOWED_FRONTMATTER_FIELDS)
    if unexpected:
        errors.append(
            f"{_relative(skill_file)}: unexpected frontmatter fields: {', '.join(unexpected)}"
        )

    name = metadata.get("name")
    if not isinstance(name, str) or not name:
        errors.append(f"{_relative(skill_file)}: missing or invalid required 'name'")
    else:
        if len(name) > MAX_NAME_LENGTH:
            errors.append(
                f"{_relative(skill_file)}: name exceeds {MAX_NAME_LENGTH} characters "
                f"({len(name)} chars)"
            )
        if not NAME_RE.fullmatch(name):
            errors.append(
                f"{_relative(skill_file)}: name must be lowercase kebab-case, got {name!r}"
            )
        if name != skill_dir.name:
            errors.append(
                f"{_relative(skill_file)}: name {name!r} must match directory {skill_dir.name!r}"
            )

    description = metadata.get("description")
    if not isinstance(description, str) or not description.strip():
        errors.append(
            f"{_relative(skill_file)}: missing or invalid required 'description'"
        )
    elif len(description) > MAX_DESCRIPTION_LENGTH:
        errors.append(
            f"{_relative(skill_file)}: description exceeds {MAX_DESCRIPTION_LENGTH} characters "
            f"({len(description)} chars)"
        )

    errors.extend(
        _validate_optional_string(
            metadata,
            "compatibility",
            skill_file,
            max_length=MAX_COMPATIBILITY_LENGTH,
        )
    )
    license_name = metadata.get("license")
    if not isinstance(license_name, str) or not license_name.strip():
        errors.append(f"{_relative(skill_file)}: missing or invalid required 'license'")
    errors.extend(_validate_optional_string(metadata, "allowed-tools", skill_file))

    if "metadata" in metadata:
        custom = metadata["metadata"]
        if not isinstance(custom, dict) or not all(
            isinstance(key, str) and isinstance(value, str)
            for key, value in custom.items()
        ):
            errors.append(
                f"{_relative(skill_file)}: 'metadata' must map string keys to string values"
            )

    return errors


def _markdown_uri_targets(text: str) -> set[str]:
    targets = set(LINK_RE.findall(text))
    for match in REFERENCE_LINK_RE.finditer(text):
        targets.add(match.group(1) or match.group(2))
    targets.update(AUTOLINK_RE.findall(text))
    targets.update(ACTIVE_SCRIPT_URI_RE.findall(text))
    targets.update(FILE_DATA_LINK_RE.findall(text))

    html_parser = HtmlUriTargetParser()
    html_parser.feed(text)
    targets.update(html_parser.targets)
    return targets


def validate_local_links(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    for md_file in skill_dir.rglob("*.md"):
        text = md_file.read_text(encoding="utf-8")
        for raw_target in sorted(_markdown_uri_targets(text)):
            target = unescape(
                COMMONMARK_ESCAPE_RE.sub(r"\1", raw_target.strip().strip("<>"))
            )
            if not target or target.startswith("#"):
                continue
            parsed = urlparse(target)
            scheme = parsed.scheme.lower()
            if scheme in SAFE_EXTERNAL_URI_SCHEMES:
                continue
            if scheme or parsed.netloc:
                label = scheme or "protocol-relative"
                errors.append(
                    f"{_relative(md_file)}: unsupported URI scheme {label!r}: {target}"
                )
                continue
            path_part = unquote(parsed.path)
            if not path_part:
                continue
            resolved = (md_file.parent / path_part).resolve()
            try:
                resolved.relative_to(skill_dir.resolve())
            except ValueError:
                errors.append(
                    f"{_relative(md_file)}: local link escapes the skill directory: {target}"
                )
                continue
            if not resolved.exists():
                errors.append(f"{_relative(md_file)}: broken local link: {target}")
    return errors


def _validate_adapter_asset(
    skill_dir: Path, adapter: Path, value: Any, field: str
) -> list[str]:
    if not isinstance(value, str) or not value:
        return [f"{_relative(adapter)}: interface.{field} must be a non-empty string"]
    resolved = (skill_dir / value).resolve()
    try:
        resolved.relative_to(skill_dir.resolve())
    except ValueError:
        return [f"{_relative(adapter)}: interface.{field} escapes the skill directory"]
    if not resolved.is_file():
        return [f"{_relative(adapter)}: interface.{field} does not exist: {value}"]
    return []


def _validate_known_mapping_fields(
    mapping: dict[Any, Any], allowed: set[str], adapter: Path, label: str
) -> list[str]:
    errors: list[str] = []
    non_string = sorted(repr(key) for key in mapping if not isinstance(key, str))
    if non_string:
        errors.append(
            f"{_relative(adapter)}: {label} keys must be strings: {', '.join(non_string)}"
        )
    unexpected = sorted(
        key for key in mapping if isinstance(key, str) and key not in allowed
    )
    if unexpected:
        errors.append(
            f"{_relative(adapter)}: unexpected {label} fields: {', '.join(unexpected)}"
        )
    return errors


def validate_openai_adapter(skill_dir: Path, skill_name: str) -> list[str]:
    adapter = skill_dir / "agents" / "openai.yaml"
    if not adapter.exists():
        return []

    data, errors = _load_yaml_mapping(
        adapter.read_text(encoding="utf-8"), adapter, "adapter"
    )
    if errors:
        return errors

    unexpected_top = sorted(set(data) - {"interface", "policy", "dependencies"})
    if unexpected_top:
        errors.append(
            f"{_relative(adapter)}: unexpected adapter fields: {', '.join(unexpected_top)}"
        )

    interface = data.get("interface")
    if interface is not None:
        if not isinstance(interface, dict):
            errors.append(f"{_relative(adapter)}: 'interface' must be a YAML mapping")
        else:
            errors.extend(
                _validate_known_mapping_fields(
                    interface, OPENAI_INTERFACE_FIELDS, adapter, "interface"
                )
            )

            for field in ("display_name", "short_description", "default_prompt"):
                if field in interface and (
                    not isinstance(interface[field], str)
                    or not interface[field].strip()
                ):
                    errors.append(
                        f"{_relative(adapter)}: interface.{field} must be a non-empty string"
                    )

            short_description = interface.get("short_description")
            if (
                isinstance(short_description, str)
                and not 25 <= len(short_description) <= 64
            ):
                errors.append(
                    f"{_relative(adapter)}: interface.short_description must be 25-64 "
                    f"characters ({len(short_description)} chars)"
                )

            default_prompt = interface.get("default_prompt")
            expected_reference = f"${skill_name}"
            if (
                isinstance(default_prompt, str)
                and expected_reference not in default_prompt
            ):
                errors.append(
                    f"{_relative(adapter)}: interface.default_prompt must mention "
                    f"{expected_reference}"
                )

            for field in ("icon_small", "icon_large"):
                if field in interface:
                    errors.extend(
                        _validate_adapter_asset(
                            skill_dir, adapter, interface[field], field
                        )
                    )

            brand_color = interface.get("brand_color")
            if brand_color is not None and (
                not isinstance(brand_color, str)
                or re.fullmatch(r"#[0-9A-Fa-f]{6}", brand_color) is None
            ):
                errors.append(
                    f"{_relative(adapter)}: interface.brand_color must be a six-digit hex color"
                )

    policy = data.get("policy")
    if policy is not None:
        if not isinstance(policy, dict):
            errors.append(f"{_relative(adapter)}: 'policy' must be a YAML mapping")
        else:
            errors.extend(
                _validate_known_mapping_fields(
                    policy, OPENAI_POLICY_FIELDS, adapter, "policy"
                )
            )
            implicit = policy.get("allow_implicit_invocation")
            if implicit is not None and not isinstance(implicit, bool):
                errors.append(
                    f"{_relative(adapter)}: policy.allow_implicit_invocation must be boolean"
                )

    dependencies = data.get("dependencies")
    if dependencies is not None:
        if not isinstance(dependencies, dict):
            errors.append(
                f"{_relative(adapter)}: 'dependencies' must be a YAML mapping"
            )
        else:
            errors.extend(
                _validate_known_mapping_fields(
                    dependencies, OPENAI_DEPENDENCY_FIELDS, adapter, "dependencies"
                )
            )
            tools = dependencies.get("tools")
            if tools is not None:
                if not isinstance(tools, list):
                    errors.append(
                        f"{_relative(adapter)}: dependencies.tools must be a list"
                    )
                else:
                    for index, tool in enumerate(tools):
                        prefix = f"dependencies.tools[{index}]"
                        if not isinstance(tool, dict):
                            errors.append(
                                f"{_relative(adapter)}: {prefix} must be a YAML mapping"
                            )
                            continue
                        errors.extend(
                            _validate_known_mapping_fields(
                                tool, OPENAI_TOOL_FIELDS, adapter, prefix
                            )
                        )
                        for field in ("type", "value", "description"):
                            value = tool.get(field)
                            if not isinstance(value, str) or not value.strip():
                                errors.append(
                                    f"{_relative(adapter)}: {prefix}.{field} must be a "
                                    "non-empty string"
                                )
                        if isinstance(tool.get("type"), str) and tool["type"] != "mcp":
                            errors.append(
                                f"{_relative(adapter)}: {prefix}.type must be 'mcp'"
                            )
                        for field in ("transport", "url"):
                            if field in tool and (
                                not isinstance(tool[field], str)
                                or not tool[field].strip()
                            ):
                                errors.append(
                                    f"{_relative(adapter)}: {prefix}.{field} must be a "
                                    "non-empty string"
                                )

    return errors


def validate_no_symlinks(skill_dir: Path) -> list[str]:
    if skill_dir.is_symlink():
        return [
            f"{_relative(skill_dir)}: symlinks are not allowed in source skill directories"
        ]
    return [
        f"{_relative(path)}: symlinks are not allowed in source skill directories"
        for path in skill_dir.rglob("*")
        if path.is_symlink()
    ]


def validate_skill(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    skill_file = skill_dir / "SKILL.md"
    rel = _relative(skill_dir)

    symlink_errors = validate_no_symlinks(skill_dir)
    if symlink_errors:
        return symlink_errors

    if not skill_file.is_file():
        return [f"{rel}: missing SKILL.md"]

    metadata, frontmatter_errors = parse_frontmatter(skill_file)
    errors.extend(frontmatter_errors)
    if not frontmatter_errors:
        errors.extend(validate_frontmatter(skill_dir, metadata))

    for forbidden in FORBIDDEN_SKILL_DOCS:
        if (skill_dir / forbidden).exists():
            errors.append(
                f"{rel}: {forbidden} should not live inside an individual skill"
            )

    for child in skill_dir.iterdir():
        if child.is_dir() and child.name not in ALLOWED_SUPPORT_DIRS:
            errors.append(
                f"{rel}: unexpected support directory {child.name!r}; "
                f"expected one of {sorted(ALLOWED_SUPPORT_DIRS)}"
            )

    license_notice = skill_dir / "LICENSE.txt"
    if (
        not license_notice.is_file()
        or not license_notice.read_text(encoding="utf-8").strip()
    ):
        errors.append(f"{rel}: missing or empty bundled LICENSE.txt")

    errors.extend(validate_local_links(skill_dir))
    if isinstance(metadata.get("name"), str):
        errors.extend(validate_openai_adapter(skill_dir, metadata["name"]))
    return errors


def validate_discovery_scope() -> list[str]:
    errors: list[str] = []
    skills_root = SKILLS_DIR.resolve()
    for skill_file in ROOT.rglob("SKILL.md"):
        relative_parts = skill_file.relative_to(ROOT).parts
        if any(part in IGNORED_DISCOVERY_DIRS for part in relative_parts[:-1]):
            continue
        try:
            skill_file.resolve().relative_to(skills_root)
        except ValueError:
            errors.append(
                f"{_relative(skill_file)}: discoverable SKILL.md must live under skills/"
            )
    return errors


def main() -> int:
    if not SKILLS_DIR.is_dir():
        print("error: skills/ directory not found", file=sys.stderr)
        return 1

    skill_dirs = sorted(
        path
        for path in SKILLS_DIR.iterdir()
        if path.is_dir() and not path.name.startswith(".")
    )
    if not skill_dirs:
        print("error: no skills found", file=sys.stderr)
        return 1

    errors = validate_discovery_scope()
    for skill_dir in skill_dirs:
        errors.extend(validate_skill(skill_dir))

    if errors:
        print("Skill validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Validated {len(skill_dirs)} skills:")
    for skill_dir in skill_dirs:
        print(f"- {skill_dir.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

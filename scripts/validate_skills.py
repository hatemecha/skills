#!/usr/bin/env python3
"""Validate the public skill catalog and its local references."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
FRONTMATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.S)
LINK = re.compile(r"\]\(([^)]+)\)")


def metadata(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER.match(text)
    if not match:
        raise ValueError(f"{path}: missing YAML frontmatter")
    data = yaml.safe_load(match.group(1))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: frontmatter must be a mapping")
    return data


def validate(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    skills = root / "skills"
    license_file = root / "LICENSE"
    if not skills.is_dir() or not license_file.is_file():
        return ["missing skills/ or LICENSE"]

    directories = sorted(p for p in skills.iterdir() if p.is_dir())
    names = {p.name for p in directories}
    if not names:
        errors.append("no installable skills found")
    expected = {(p / "SKILL.md").resolve() for p in directories}
    discovered = {p.resolve() for p in root.rglob("SKILL.md") if ".venv" not in p.parts}
    if discovered != expected:
        errors.append("unexpected or missing SKILL.md outside the catalog")

    for directory in directories:
        spec = directory / "SKILL.md"
        if not NAME.fullmatch(directory.name) or not spec.is_file():
            errors.append(f"{directory.name}: invalid directory name or missing SKILL.md")
            continue
        try:
            data = metadata(spec)
        except (ValueError, yaml.YAMLError, OSError) as exc:
            errors.append(str(exc))
            continue
        if data.get("name") != directory.name:
            errors.append(f"{directory.name}: frontmatter name does not match directory")
        desc = data.get("description")
        if not isinstance(desc, str) or not 1 <= len(desc) <= 1024:
            errors.append(f"{directory.name}: description is missing or too long")
        if data.get("license") != "MIT":
            errors.append(f"{directory.name}: license must match bundled MIT license")
        notice = directory / "LICENSE.txt"
        if not notice.is_file() or notice.read_bytes() != license_file.read_bytes():
            errors.append(f"{directory.name}: missing or mismatched LICENSE.txt")

        for file in directory.rglob("*.md"):
            for target in LINK.findall(file.read_text(encoding="utf-8")):
                path = target.split("#", 1)[0].strip()
                if not path or "://" in path or path.startswith(("mailto:", "#")):
                    continue
                resolved = (file.parent / path).resolve()
                if not resolved.is_relative_to(directory.resolve()) or not resolved.is_file():
                    errors.append(f"{file.relative_to(root)}: invalid local link: {target}")

    groups_file = root / "skills.sh.json"
    if not groups_file.is_file():
        errors.append("missing skills.sh.json")
    else:
        try:
            groups = json.loads(groups_file.read_text(encoding="utf-8"))["groupings"]
            listed = [name for group in groups for name in group["skills"]]
            if len(listed) != len(set(listed)) or set(listed) != names:
                errors.append("skills.sh.json must list every active skill exactly once")
        except (OSError, ValueError, KeyError, TypeError) as exc:
            errors.append(f"invalid skills.sh.json: {exc}")

    return errors


if __name__ == "__main__":
    failures = validate()
    for error in failures:
        print(f"ERROR: {error}", file=sys.stderr)
    if failures:
        sys.exit(1)
    print("Validated 8 skill packages, local references, licenses, and catalog.")

#!/usr/bin/env python3
"""Validate the portable structure of skills in this repository."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
ALLOWED_SUPPORT_DIRS = {"agents", "assets", "references", "scripts"}
FORBIDDEN_SKILL_DOCS = {"README.md", "CHANGELOG.md"}


def parse_frontmatter(path: Path) -> tuple[dict[str, str], list[str]]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    if not lines or lines[0].strip() != "---":
        return {}, [f"{path.relative_to(ROOT)}: missing opening YAML frontmatter delimiter"]

    try:
        end = next(i for i, line in enumerate(lines[1:], start=1) if line.strip() == "---")
    except StopIteration:
        return {}, [f"{path.relative_to(ROOT)}: missing closing YAML frontmatter delimiter"]

    metadata: dict[str, str] = {}
    for line in lines[1:end]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            errors.append(f"{path.relative_to(ROOT)}: malformed frontmatter line: {line!r}")
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            metadata[key] = value

    return metadata, errors


def validate_local_links(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    for md_file in skill_dir.rglob("*.md"):
        text = md_file.read_text(encoding="utf-8")
        for target in LINK_RE.findall(text):
            target = target.strip()
            if not target or target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = target.split("#", 1)[0].split("?", 1)[0]
            if not target:
                continue
            resolved = (md_file.parent / target).resolve()
            try:
                resolved.relative_to(skill_dir.resolve())
            except ValueError:
                errors.append(
                    f"{md_file.relative_to(ROOT)}: local link escapes the skill directory: {target}"
                )
                continue
            if not resolved.exists():
                errors.append(f"{md_file.relative_to(ROOT)}: broken local link: {target}")
    return errors


def validate_skill(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    skill_file = skill_dir / "SKILL.md"
    rel = skill_dir.relative_to(ROOT)

    if not skill_file.is_file():
        return [f"{rel}: missing SKILL.md"]

    metadata, frontmatter_errors = parse_frontmatter(skill_file)
    errors.extend(frontmatter_errors)

    name = metadata.get("name", "")
    description = metadata.get("description", "")

    if not name:
        errors.append(f"{skill_file.relative_to(ROOT)}: missing required 'name'")
    elif not NAME_RE.fullmatch(name):
        errors.append(
            f"{skill_file.relative_to(ROOT)}: name must be lowercase kebab-case, got {name!r}"
        )
    elif name != skill_dir.name:
        errors.append(
            f"{skill_file.relative_to(ROOT)}: name {name!r} must match directory {skill_dir.name!r}"
        )

    if not description:
        errors.append(f"{skill_file.relative_to(ROOT)}: missing required 'description'")

    for forbidden in FORBIDDEN_SKILL_DOCS:
        if (skill_dir / forbidden).exists():
            errors.append(f"{rel}: {forbidden} should not live inside an individual skill")

    for child in skill_dir.iterdir():
        if child.is_dir() and child.name not in ALLOWED_SUPPORT_DIRS:
            errors.append(
                f"{rel}: unexpected support directory {child.name!r}; "
                f"expected one of {sorted(ALLOWED_SUPPORT_DIRS)}"
            )

    errors.extend(validate_local_links(skill_dir))
    return errors


def main() -> int:
    if not SKILLS_DIR.is_dir():
        print("error: skills/ directory not found", file=sys.stderr)
        return 1

    skill_dirs = sorted(path for path in SKILLS_DIR.iterdir() if path.is_dir() and not path.name.startswith("."))
    if not skill_dirs:
        print("error: no skills found", file=sys.stderr)
        return 1

    errors: list[str] = []
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

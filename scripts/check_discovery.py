#!/usr/bin/env python3
"""Install through `npx skills` and assert the exact copied catalog."""

from __future__ import annotations

import os

# The subprocess command is a fixed argv with no shell or user-controlled executable.
import subprocess  # nosec B404
import sys
import tempfile
from pathlib import Path
from typing import Collection

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
SKILLS_CLI_VERSION = "1.5.22"
REQUIRED_INSTALLED_FILES = ("SKILL.md", "LICENSE.txt")


def validate_installed_catalog(
    catalog: Path, expected: Collection[str], source_catalog: Path | None = None
) -> None:
    expected_names = set(expected)
    if not catalog.is_dir():
        raise ValueError(f"installed catalog not found: {catalog}")

    actual_names = {
        path.name
        for path in catalog.iterdir()
        if path.is_dir() and not path.name.startswith(".")
    }
    missing = sorted(expected_names - actual_names)
    unexpected = sorted(actual_names - expected_names)
    if missing:
        raise ValueError(f"missing installed skills: {', '.join(missing)}")
    if unexpected:
        raise ValueError(f"unexpected installed skills: {', '.join(unexpected)}")

    for skill_name in sorted(expected_names):
        skill_dir = catalog / skill_name
        if skill_dir.is_symlink():
            raise ValueError(
                f"installed skill must be copied, not symlinked: {skill_name}"
            )
        for relative_path in REQUIRED_INSTALLED_FILES:
            installed_file = skill_dir / relative_path
            if not installed_file.is_file() or installed_file.is_symlink():
                raise ValueError(
                    f"missing installed file for {skill_name}: {relative_path}"
                )
        if source_catalog is not None:
            source_skill = source_catalog / skill_name
            source_files = {
                path.relative_to(source_skill): path
                for path in source_skill.rglob("*")
                if path.is_file()
            }
            installed_files = {
                path.relative_to(skill_dir): path
                for path in skill_dir.rglob("*")
                if path.is_file()
            }
            linked_files = sorted(
                relative_path
                for relative_path, path in installed_files.items()
                if path.is_symlink()
            )
            if linked_files:
                raise ValueError(
                    f"installed source files must be copied for {skill_name}: "
                    + ", ".join(map(str, linked_files))
                )
            missing_files = sorted(set(source_files) - set(installed_files))
            unexpected_files = sorted(set(installed_files) - set(source_files))
            if missing_files:
                raise ValueError(
                    f"missing installed source files for {skill_name}: "
                    + ", ".join(map(str, missing_files))
                )
            if unexpected_files:
                raise ValueError(
                    f"unexpected installed source files for {skill_name}: "
                    + ", ".join(map(str, unexpected_files))
                )
            for relative_path, source_file in source_files.items():
                if (
                    source_file.read_bytes()
                    != installed_files[relative_path].read_bytes()
                ):
                    raise ValueError(
                        f"installed content mismatch for {skill_name}: {relative_path}"
                    )


def main() -> int:
    expected = sorted(
        path.name
        for path in SKILLS_DIR.iterdir()
        if path.is_dir() and not path.name.startswith(".")
    )
    environment = os.environ.copy()
    environment.setdefault("DISABLE_TELEMETRY", "1")

    with tempfile.TemporaryDirectory(prefix="skills-discovery-") as tempdir:
        command = [
            "npx",
            "--yes",
            f"skills@{SKILLS_CLI_VERSION}",
            "add",
            str(ROOT),
            "--skill",
            "*",
            "--agent",
            "universal",
            "--yes",
            "--copy",
        ]
        try:
            # Command, source, and cwd are fixed by this script.
            result = subprocess.run(  # nosec B603
                command,
                cwd=tempdir,
                env=environment,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                timeout=180,
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            print(
                f"error: skills CLI timed out after {exc.timeout} seconds",
                file=sys.stderr,
            )
            return 1
        except OSError as exc:
            print(
                f"error: could not execute {' '.join(command)}: {exc}", file=sys.stderr
            )
            return 1

        print(result.stdout, end="")
        if result.returncode != 0:
            print(f"error: skills CLI exited with {result.returncode}", file=sys.stderr)
            return result.returncode

        catalog = Path(tempdir) / ".agents" / "skills"
        try:
            validate_installed_catalog(catalog, expected, SKILLS_DIR)
        except ValueError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1

    print(f"Copied installation matches repository catalog: {', '.join(expected)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

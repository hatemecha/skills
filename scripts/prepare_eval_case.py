#!/usr/bin/env python3
"""Create fresh, disposable benchmark workspaces without running agent code."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "evals" / "fixtures"
MANIFEST = ROOT / "evals" / "benchmark-cases.json"
DEFAULT_OUTPUT = ROOT / "evals" / "workspaces"


def prepare(case_id: str, variant: str, output_root: Path) -> Path:
    cases = json.loads(MANIFEST.read_text(encoding="utf-8"))
    match = next((case for case in cases if case["id"] == case_id), None)
    if match is None:
        raise ValueError(f"unknown benchmark case: {case_id}")
    if variant not in ("baseline", "skills"):
        raise ValueError("variant must be baseline or skills")
    source = FIXTURES / match["fixture"]
    target = output_root / case_id / variant
    if target.exists() or target.is_symlink():
        raise FileExistsError(f"refusing to overwrite an existing workspace: {target}")
    if not source.is_dir():
        raise FileNotFoundError(f"missing fixture: {source}")
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, target, symlinks=False)
    return target


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case", help="id from benchmark-cases.json")
    parser.add_argument("variant", choices=("baseline", "skills"))
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    try:
        target = prepare(args.case, args.variant, args.output_root)
    except (OSError, ValueError, KeyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Preview or install a bounded, managed engineering policy in global agent files."""

from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "config" / "global-engineering-rules.md"
START = "<!-- hatemecha-skills:begin -->"
END = "<!-- hatemecha-skills:end -->"
TARGETS = {
    "codex": Path.home() / ".codex" / "AGENTS.md",
    "opencode": Path.home() / ".config" / "opencode" / "AGENTS.md",
}


def managed_text(policy: str) -> str:
    if START in policy or END in policy:
        raise ValueError("policy contains reserved managed-section delimiters")
    return f"{START}\n{policy.strip()}\n{END}\n"


def merge(existing: str, policy: str) -> str:
    block = managed_text(policy)
    has_start, has_end = START in existing, END in existing
    if has_start != has_end or existing.count(START) > 1 or existing.count(END) > 1:
        raise ValueError("incomplete or duplicate managed section; edit manually")
    if has_start:
        before, rest = existing.split(START, 1)
        _, after = rest.split(END, 1)
        return before + block.rstrip("\n") + after
    if not existing:
        return block
    return existing.rstrip("\n") + "\n\n" + block


def install(path: Path, policy: str, *, apply: bool = False) -> str:
    if path.is_symlink():
        raise ValueError(f"refusing to modify symlink: {path}")
    if path.exists() and not path.is_file():
        raise ValueError(f"not a regular file: {path}")
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    updated = merge(existing, policy)
    status = "unchanged" if updated == existing else ("update" if path.exists() else "create")
    if apply and status != "unchanged":
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(updated, encoding="utf-8")
    return status


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="actually write files; default is preview")
    parser.add_argument("--target", action="append", choices=sorted(TARGETS), help="repeatable; default: both")
    parser.add_argument("--print-cursor", action="store_true", help="print policy to paste in Cursor User Rules")
    args = parser.parse_args()
    policy = SOURCE.read_text(encoding="utf-8")
    if args.print_cursor:
        print(policy.strip())
        return 0
    targets = dict((name, TARGETS[name]) for name in (args.target or list(TARGETS)))
    errors = 0
    for name, path in targets.items():
        try:
            status = install(path, policy, apply=args.apply)
            print(f"{name}: {status}: {path}" + ("" if args.apply else " (preview only)"))
        except (OSError, UnicodeError, ValueError) as exc:
            errors += 1
            print(f"{name}: ERROR: {exc}")
    if not args.apply:
        print("No files changed. Use --apply to write the managed section.")
    print("Cursor: copy --print-cursor output to Settings > Rules > User Rules; never edited automatically.")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())

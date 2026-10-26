#!/usr/bin/env python3
"""Compare recorded skill/no-skill agent runs. Never launches an agent."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CASE_FILE = ROOT / "evals" / "routing-cases.json"
REQUIRED = {"case_id", "runtime", "model", "environment", "trial", "variant", "outcome", "loaded_skills", "trace_checked"}
VARIANTS = {"baseline", "skills"}
OUTCOMES = {"pass", "fail", "unknown"}


def read_records(path: Path) -> list[dict[str, Any]]:
    records = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{number}: invalid JSON: {exc}") from exc
        if not isinstance(value, dict):
            raise ValueError(f"{path}:{number}: expected JSON object")
        records.append(value)
    return records


def _integer(value: Any) -> bool:
    return type(value) is int and value >= 0


def validate_record(record: dict[str, Any], case_ids: set[str]) -> None:
    missing = REQUIRED - record.keys()
    if missing:
        raise ValueError(f"missing fields: {', '.join(sorted(missing))}")
    if record["case_id"] not in case_ids:
        raise ValueError(f"unknown case_id: {record['case_id']}")
    if record["variant"] not in VARIANTS or record["outcome"] not in OUTCOMES:
        raise ValueError("invalid variant or outcome")
    for name in ("runtime", "model", "environment"):
        if not isinstance(record[name], str) or not record[name].strip():
            raise ValueError(f"{name} must be a nonempty string")
    if not _integer(record["trial"]):
        raise ValueError("trial must be a non-negative integer")
    skills = record["loaded_skills"]
    if not isinstance(skills, list) or any(not isinstance(s, str) for s in skills):
        raise ValueError("loaded_skills must be an array of strings")
    if len(skills) != len(set(skills)):
        raise ValueError("duplicate loaded_skills")
    if type(record["trace_checked"]) is not bool:
        raise ValueError("trace_checked must be boolean")
    if record["outcome"] == "pass" and not str(record.get("evidence", "")).strip():
        raise ValueError("a reported pass needs a verifiable evidence reference")
    for name in ("input_tokens", "output_tokens", "elapsed_seconds", "unrelated_changes"):
        value = record.get(name)
        if value is not None and (
            (name == "elapsed_seconds" and (type(value) not in (int, float) or value < 0))
            or (name != "elapsed_seconds" and not _integer(value))
        ):
            raise ValueError(f"{name} must be non-negative or null")


def _tokens(r: dict[str, Any]) -> int | None:
    values = (r.get("input_tokens"), r.get("output_tokens"))
    return sum(values) if all(_integer(v) for v in values) else None


def evaluate(records: list[dict[str, Any]], cases: list[dict[str, Any]]) -> dict[str, Any]:
    lookup = {c["id"]: c for c in cases}
    grouped: dict[tuple[str, str, str, str, int], dict[str, dict[str, Any]]] = {}
    for index, r in enumerate(records, 1):
        try:
            validate_record(r, set(lookup))
        except ValueError as exc:
            raise ValueError(f"record {index}: {exc}") from exc
        key = (r["case_id"], r["runtime"], r["model"], r["environment"], r["trial"])
        group = grouped.setdefault(key, {})
        if r["variant"] in group:
            raise ValueError(f"duplicate variant for {key}: {r['variant']}")
        group[r["variant"]] = r

    pairs = []
    for key, group in sorted(grouped.items()):
        base, skills = group.get("baseline"), group.get("skills")
        if not (base and skills):
            pairs.append({"key": list(key), "status": "unpaired", "missing": sorted(VARIANTS - group.keys())})
            continue
        required, forbidden = set(lookup[key[0]]["must_use"]), set(lookup[key[0]]["must_not_use"])
        if skills["trace_checked"]:
            loaded = set(skills["loaded_skills"])
            routing = "pass" if required <= loaded and not (forbidden & loaded) else "fail"
        else:
            routing = "unknown"
        if base["trace_checked"] and base["loaded_skills"]:
            routing = "contaminated-baseline"
        b_tokens, s_tokens = _tokens(base), _tokens(skills)
        pairs.append({
            "key": list(key),
            "status": "paired",
            "baseline_outcome": base["outcome"],
            "skills_outcome": skills["outcome"],
            "routing": routing,
            "baseline_tokens": b_tokens,
            "skills_tokens": s_tokens,
            "token_delta": s_tokens - b_tokens if b_tokens is not None and s_tokens is not None else None,
            "baseline_seconds": base.get("elapsed_seconds"),
            "skills_seconds": skills.get("elapsed_seconds"),
            "baseline_evidence": base.get("evidence"),
            "skills_evidence": skills.get("evidence"),
        })
    return {"records": len(records), "pairs": pairs, "note": "Outcomes are externally reported; this tool does not execute agents, check raw traces or validate assertions."}


def markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Agent Skills comparison",
        "",
        f"Recorded runs: {report['records']}; paired groups: {sum(p['status'] == 'paired' for p in report['pairs'])}.",
        "",
        "| Case / runtime / model / environment / trial | Outcomes baseline → skills | Routing | Tokens baseline → skills (delta) |",
        "| --- | --- | --- | --- |",
    ]
    for p in report["pairs"]:
        key = " / ".join(map(str, p["key"]))
        if p["status"] != "paired":
            lines.append(f"| {key} | Unpaired ({', '.join(p['missing'])} missing) | — | — |")
        else:
            values = (p["baseline_tokens"], p["skills_tokens"], p["token_delta"])
            usage = "unknown" if any(v is None for v in values) else f"{values[0]} → {values[1]} ({values[2]:+d})"
            lines.append(f"| {key} | {p['baseline_outcome']} → {p['skills_outcome']} | {p['routing']} | {usage} |")
    lines += ["", report["note"], ""]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("runs", type=Path, help="JSONL records from inspected agent runs")
    parser.add_argument("--cases", type=Path, default=CASE_FILE)
    parser.add_argument("--json", action="store_true", help="machine-readable report")
    args = parser.parse_args()
    try:
        cases = json.loads(args.cases.read_text(encoding="utf-8"))
        result = evaluate(read_records(args.runs), cases)
    except (OSError, ValueError, TypeError, KeyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2) if args.json else markdown(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Validate debian-admin-bash preference JSONL files."""
from __future__ import annotations

import argparse
import collections
import json
import re
import sys
from pathlib import Path
from typing import Any

MUTATING_SHORTCUTS = re.compile(r"rm\s+-rf\s+/(var/log|var/backups)|chmod\s+-R\s+777|pkill\s+-9|systemctl\s+(restart|stop|disable)|rm\s+-f\s+/var/lib/dpkg/lock|docker\s+compose\s+down|docker\s+system\s+prune|ufw\s+allow|rsync\s+.*--delete|\bcp\s+/var/lib/.+\.db\b|NOPASSWD:ALL|netplan\s+apply|curl\b.*\|\s*sudo\s+bash|VBoxManage\s+unregistervm\b.*--delete", re.I)
VERIFY_WORDS = re.compile(r"\b(inspect|confirm|verify|validate|dry-run|dry run|before|do not|avoid|first|check)\b", re.I)


def load(path: Path) -> tuple[list[dict[str, Any]], list[str]]:
    rows = []
    errors = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"line {line_no}: invalid JSON: {exc}")
            continue
        if not isinstance(row, dict):
            errors.append(f"line {line_no}: record is not object")
            continue
        row["__line_no"] = line_no
        rows.append(row)
    return rows, errors


def validate(path: Path) -> tuple[list[dict[str, Any]], list[str], list[str], collections.Counter[str]]:
    rows, errors = load(path)
    warnings = []
    subdomains: collections.Counter[str] = collections.Counter()
    seen = set()
    for row in rows:
        rid = row.get("id", f"line:{row.get('__line_no')}")
        if rid in seen:
            errors.append(f"{rid}: duplicate id")
        seen.add(rid)
        for key in ["id", "meta", "prompt", "chosen", "rejected", "rationale"]:
            if key not in row:
                errors.append(f"{rid}: missing {key}")
        meta = row.get("meta") if isinstance(row.get("meta"), dict) else {}
        if meta.get("task_type") != "preference":
            errors.append(f"{rid}: meta.task_type must be preference")
        subdomains[str(meta.get("subdomain", "<missing>"))] += 1
        prompt = row.get("prompt")
        if not isinstance(prompt, dict) or not isinstance(prompt.get("system"), str) or not isinstance(prompt.get("user"), str):
            errors.append(f"{rid}: prompt must contain system and user strings")
        chosen = row.get("chosen")
        rejected = row.get("rejected")
        if not isinstance(chosen, str) or not chosen.strip():
            errors.append(f"{rid}: chosen must be non-empty string")
        if not isinstance(rejected, str) or not rejected.strip():
            errors.append(f"{rid}: rejected must be non-empty string")
        if isinstance(chosen, str) and isinstance(rejected, str) and chosen.strip() == rejected.strip():
            errors.append(f"{rid}: chosen and rejected are identical")
        if isinstance(chosen, str) and not VERIFY_WORDS.search(chosen):
            warnings.append(f"{rid}: chosen may lack explicit verification/safety wording")
        if isinstance(rejected, str) and not MUTATING_SHORTCUTS.search(rejected):
            warnings.append(f"{rid}: rejected may not contain a recognizable unsafe shortcut")
    return rows, errors, warnings, subdomains


def report(path: Path, rows: list[dict[str, Any]], errors: list[str], warnings: list[str], subdomains: collections.Counter[str]) -> str:
    lines = [
        "# Preference dataset validation report",
        "",
        f"- Dataset: `{path}`",
        f"- Records: {len(rows)}",
        f"- Errors: {len(errors)}",
        f"- Warnings: {len(warnings)}",
        f"- Status: {'FAILED' if errors else 'PASSED'}",
        "",
        "## Subdomain distribution",
        "",
    ]
    for k, v in sorted(subdomains.items()):
        lines.append(f"- `{k}`: {v}")
    lines += ["", "## Errors", ""]
    lines += [f"- {e}" for e in errors] if errors else ["None."]
    lines += ["", "## Warnings", ""]
    lines += [f"- {w}" for w in warnings] if warnings else ["None."]
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dataset", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    rows, errors, warnings, subdomains = validate(args.dataset)
    text = report(args.dataset, rows, errors, warnings, subdomains)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(text, encoding="utf-8")
    else:
        print(text)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Validate LiteCoder-Terminal-SFT style JSON exports."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ALLOWED_SPEAKERS = {"human", "gpt"}


def validate_record(record: Any, index: int, seen_ids: set[Any]) -> list[str]:
    errors: list[str] = []
    label = f"record[{index}]"
    if not isinstance(record, dict):
        return [f"{label}: must be an object"]

    record_id = record.get("id")
    if not isinstance(record_id, int):
        errors.append(f"{label}.id: must be an integer")
    elif record_id in seen_ids:
        errors.append(f"{label}.id: duplicate id {record_id!r}")
    else:
        seen_ids.add(record_id)

    if "source_id" in record and (not isinstance(record["source_id"], str) or not record["source_id"].strip()):
        errors.append(f"{label}.source_id: must be a non-empty string when present")

    conversations = record.get("conversations")
    if not isinstance(conversations, list):
        errors.append(f"{label}.conversations: must be a list")
        return errors
    if len(conversations) < 2:
        errors.append(f"{label}.conversations: must contain at least one human/gpt pair")
    if len(conversations) % 2 != 0:
        errors.append(f"{label}.conversations: must contain an even number of turns")

    expected = "human"
    for turn_index, turn in enumerate(conversations):
        turn_label = f"{label}.conversations[{turn_index}]"
        if not isinstance(turn, dict):
            errors.append(f"{turn_label}: must be an object")
            continue
        speaker = turn.get("from")
        value = turn.get("value")
        if speaker not in ALLOWED_SPEAKERS:
            errors.append(f"{turn_label}.from: must be one of {sorted(ALLOWED_SPEAKERS)}")
        elif speaker != expected:
            errors.append(f"{turn_label}.from: expected {expected!r}, got {speaker!r}")
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{turn_label}.value: must be a non-empty string")
        expected = "gpt" if expected == "human" else "human"

    if conversations and isinstance(conversations[-1], dict) and conversations[-1].get("from") != "gpt":
        errors.append(f"{label}.conversations: final turn must be from 'gpt'")
    return errors


def validate(path: Path) -> tuple[int, list[str]]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return 0, [f"invalid JSON: {exc}"]
    if not isinstance(data, list):
        return 0, ["top-level value must be a JSON array"]

    errors: list[str] = []
    seen_ids: set[Any] = set()
    for index, record in enumerate(data):
        errors.extend(validate_record(record, index, seen_ids))
    return len(data), errors


def emit_report(dataset: Path, records: int, errors: list[str]) -> str:
    lines = [
        "# LiteCoder-Terminal-SFT export validation report",
        "",
        f"- Dataset: `{dataset}`",
        f"- Records: {records}",
        f"- Structural errors: {len(errors)}",
        f"- Status: {'FAILED' if errors else 'PASSED'}",
        "",
        "## Checks",
        "",
        "- Top-level value is a JSON array.",
        "- Every record is an object with integer `id`.",
        "- IDs are unique.",
        "- `source_id`, when present, is non-empty text.",
        "- `conversations` is a non-empty even-length list.",
        "- Conversation turns alternate `human` then `gpt` and end with `gpt`.",
        "- Turn `value` fields are non-empty text.",
        "",
        "## Errors",
        "",
    ]
    if errors:
        for error in errors[:500]:
            lines.append(f"- {error}")
        if len(errors) > 500:
            lines.append(f"- ... truncated {len(errors) - 500} additional errors")
    else:
        lines.append("None.")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dataset", type=Path, help="LiteCoder-style JSON dataset")
    parser.add_argument("--report", type=Path, default=None, help="Optional Markdown report output path")
    args = parser.parse_args()

    records, errors = validate(args.dataset)
    report = emit_report(args.dataset, records, errors)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(report, encoding="utf-8")
    else:
        print(report)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())

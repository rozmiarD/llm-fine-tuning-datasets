#!/usr/bin/env python3
"""Export governed JSONL chat records to LiteCoder-Terminal-SFT JSON format.

Lite-Coder/LiteCoder-Terminal-SFT stores a single JSON array.  Each item has
an integer `id` and a `conversations` list using ShareGPT-style `from` values:
`human` and `gpt`.  The source dataset here is canonical JSONL with
`system`/`user`/`assistant` messages, so this exporter folds the optional
system message into the first human turn instead of dropping it.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


DEFAULT_SYSTEM_PREFIX = "System instructions:"
DEFAULT_USER_PREFIX = "Task Description:"


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                value = json.loads(stripped)
            except json.JSONDecodeError as exc:  # pragma: no cover - CLI guard
                raise SystemExit(f"{path}:{line_no}: invalid JSON: {exc}") from exc
            if not isinstance(value, dict):
                raise SystemExit(f"{path}:{line_no}: record is not a JSON object")
            records.append(value)
    return records


def messages_by_role(record: dict[str, Any], source_id: str) -> dict[str, list[str]]:
    grouped: dict[str, list[str]] = {"system": [], "user": [], "assistant": []}
    messages = record.get("messages")
    if not isinstance(messages, list):
        raise ValueError(f"{source_id}: messages must be a list")
    for index, message in enumerate(messages):
        if not isinstance(message, dict):
            raise ValueError(f"{source_id}: messages[{index}] must be an object")
        role = message.get("role")
        content = message.get("content")
        if role not in grouped:
            raise ValueError(f"{source_id}: unsupported role {role!r}")
        if not isinstance(content, str) or not content.strip():
            raise ValueError(f"{source_id}: messages[{index}].content must be a non-empty string")
        grouped[role].append(content.strip())
    return grouped


def source_to_litecoder_record(record: dict[str, Any], index: int) -> dict[str, Any]:
    source_id = str(record.get("id") or f"line:{index + 1}")
    grouped = messages_by_role(record, source_id)
    if len(grouped["user"]) != 1 or len(grouped["assistant"]) != 1:
        raise ValueError(f"{source_id}: expected exactly one user and one assistant message")
    if len(grouped["system"]) > 1:
        raise ValueError(f"{source_id}: expected at most one system message")

    human_parts: list[str] = []
    if grouped["system"]:
        human_parts.append(f"{DEFAULT_SYSTEM_PREFIX}\n{grouped['system'][0]}")
    human_parts.append(f"{DEFAULT_USER_PREFIX}\n{grouped['user'][0]}")

    return {
        "id": index,
        "source_id": source_id,
        "conversations": [
            {"from": "human", "value": "\n\n".join(human_parts)},
            {"from": "gpt", "value": grouped["assistant"][0]},
        ],
    }


def convert(input_path: Path) -> list[dict[str, Any]]:
    return [source_to_litecoder_record(record, index) for index, record in enumerate(load_jsonl(input_path))]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Canonical source JSONL dataset")
    parser.add_argument("output", type=Path, help="Output LiteCoder-style JSON file")
    parser.add_argument("--indent", type=int, default=2, help="JSON indentation; use 0 for compact output")
    args = parser.parse_args()

    records = convert(args.input)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    if args.indent == 0:
        payload = json.dumps(records, ensure_ascii=False, separators=(",", ":"))
    else:
        payload = json.dumps(records, ensure_ascii=False, indent=args.indent)
    args.output.write_text(payload + "\n", encoding="utf-8")
    print(f"wrote {len(records)} LiteCoder-style records to {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

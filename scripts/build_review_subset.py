#!/usr/bin/env python3
"""Build a high-priority review-candidate subset for debian-admin-bash.

This script does not claim human review. It selects a smaller, more useful
candidate subset for manual review and training experiments while preserving the
original governed record shape and honest draft review metadata.
"""
from __future__ import annotations

import argparse
import collections
import copy
import hashlib
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "datasets/debian-admin-bash/debian-admin-bash-sft.jsonl"
OUT = ROOT / "datasets/debian-admin-bash/review/review-candidates.jsonl"
MANIFEST = ROOT / "datasets/debian-admin-bash/review/README.md"

RISK_WEIGHT = {
    "destructive": 9,
    "security_sensitive": 8,
    "privilege_sensitive": 7,
    "state_change_high": 6,
    "network_sensitive": 5,
    "state_change_low": 4,
    "safe_readonly": 2,
}
STYLE_WEIGHT = {
    "diagnostic_steps": 5,
    "guarded_procedure": 4,
    "refusal_with_safe_alternative": 4,
    "script_with_explanation": 3,
    "command_with_brief_explanation": 2,
    "single_command": 1,
}
PRIORITY_SUBDOMAINS = {
    "systemd",
    "incident_triage",
    "packages",
    "backup_restore",
    "permissions",
    "ssh_auth",
    "security",
    "processes",
    "networking",
    "docker",
    "sqlite",
    "logs",
    "filesystem",
}


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(json.dumps(r, ensure_ascii=False, separators=(",", ":")) for r in records) + "\n", encoding="utf-8")


def text_for(record: dict[str, Any], role: str) -> str:
    return "\n".join(m.get("content", "") for m in record.get("messages", []) if m.get("role") == role)


def normalized_prompt(record: dict[str, Any]) -> str:
    user = text_for(record, "user").lower()
    user = re.sub(r"```.*?```", "```X```", user, flags=re.S)
    user = re.sub(r"\b\d+\b", "N", user)
    user = re.sub(r"variant n|case n", "CASE", user)
    return re.sub(r"\s+", " ", user).strip()


def score(record: dict[str, Any]) -> tuple[int, str]:
    meta = record["meta"]
    user = text_for(record, "user")
    assistant = text_for(record, "assistant")
    score = 0
    reasons: list[str] = []
    risk = meta.get("risk_level", "safe_readonly")
    style = meta.get("answer_style", "")
    subdomain = meta.get("subdomain", "")
    score += RISK_WEIGHT.get(risk, 0)
    score += STYLE_WEIGHT.get(style, 0)
    if subdomain in PRIORITY_SUBDOMAINS:
        score += 4
        reasons.append("priority-subdomain")
    if "```text" in user or "output" in user.lower() or "error" in user.lower() or "failed" in user.lower():
        score += 5
        reasons.append("evidence-driven")
    if "dry-run" in assistant.lower() or "--dry-run" in assistant.lower():
        score += 2
        reasons.append("dry-run")
    if re.search(r"\b(before|verify|validate|inspect|confirm|avoid)\b", assistant, re.I):
        score += 2
        reasons.append("inspection-first")
    if style == "refusal_with_safe_alternative":
        reasons.append("safe-refusal")
    if len(assistant) > 1800:
        score -= 3
        reasons.append("long-answer-penalty")
    return score, ", ".join(reasons) or "balanced"


def build(limit: int) -> tuple[list[dict[str, Any]], list[tuple[str, int, str]]]:
    records = load_jsonl(SOURCE)
    scored = []
    for record in records:
        s, why = score(record)
        scored.append((s, why, record))
    scored.sort(key=lambda x: (x[0], x[2]["id"]), reverse=True)

    selected: list[dict[str, Any]] = []
    selected_info: list[tuple[str, int, str]] = []
    per_subdomain: collections.Counter[str] = collections.Counter()
    per_style: collections.Counter[str] = collections.Counter()
    per_cluster: collections.Counter[str] = collections.Counter()

    # First pass: enforce diversity and cap repeated prompt templates.
    for s, why, record in scored:
        meta = record["meta"]
        subdomain = meta.get("subdomain", "")
        style = meta.get("answer_style", "")
        cluster = normalized_prompt(record)
        if per_subdomain[subdomain] >= 32:
            continue
        if per_style[style] >= max(28, limit // 3):
            continue
        if per_cluster[cluster] >= 4:
            continue
        item = copy.deepcopy(record)
        item["meta"].setdefault("curation", {})
        item["meta"]["curation"].update({
            "review_candidate": True,
            "source_dataset": "debian-admin-bash-sft",
            "selection_score": s,
            "selection_reason": why,
            "review_claim": "candidate_only_not_human_reviewed",
        })
        selected.append(item)
        selected_info.append((item["id"], s, why))
        per_subdomain[subdomain] += 1
        per_style[style] += 1
        per_cluster[cluster] += 1
        if len(selected) >= limit:
            break

    # Second pass if diversity caps prevented filling the requested limit.
    for s, why, record in scored:
        if len(selected) >= limit:
            break
        if any(r["id"] == record["id"] for r in selected):
            continue
        cluster = normalized_prompt(record)
        if per_cluster[cluster] >= 6:
            continue
        item = copy.deepcopy(record)
        item["meta"].setdefault("curation", {})
        item["meta"]["curation"].update({
            "review_candidate": True,
            "source_dataset": "debian-admin-bash-sft",
            "selection_score": s,
            "selection_reason": why,
            "review_claim": "candidate_only_not_human_reviewed",
        })
        selected.append(item)
        selected_info.append((item["id"], s, why))
        per_cluster[cluster] += 1

    return selected, selected_info


def write_manifest(records: list[dict[str, Any]], info: list[tuple[str, int, str]]) -> None:
    sub = collections.Counter(r["meta"]["subdomain"] for r in records)
    risk = collections.Counter(r["meta"]["risk_level"] for r in records)
    style = collections.Counter(r["meta"]["answer_style"] for r in records)
    sha = hashlib.sha256(OUT.read_bytes()).hexdigest() if OUT.exists() else "<not-written>"
    lines = [
        "# Review-candidate subset: debian-admin-bash-sft",
        "",
        "This file is a candidate subset for manual semantic/safety review and training experiments.",
        "",
        "It is not a claim that these records are human-reviewed. The source records keep their governed `review.status` values.",
        "",
        "## Output",
        "",
        f"- File: `{OUT.relative_to(ROOT)}`",
        f"- Records: {len(records)}",
        f"- SHA-256: `{sha}`",
        "",
        "## Selection rules",
        "",
        "- prioritize high-risk and safety-sensitive records;",
        "- prioritize output/evidence-driven incident records;",
        "- preserve subdomain and answer-style diversity;",
        "- cap repeated normalized prompt clusters;",
        "- keep review status honest until manual review is actually complete.",
        "",
        "## Distribution",
        "",
        "### Subdomain",
    ]
    for k, v in sub.most_common():
        lines.append(f"- `{k}`: {v}")
    lines += ["", "### Risk level"]
    for k, v in risk.most_common():
        lines.append(f"- `{k}`: {v}")
    lines += ["", "### Answer style"]
    for k, v in style.most_common():
        lines.append(f"- `{k}`: {v}")
    lines += ["", "## Top selected records", ""]
    for rid, s, why in info[:40]:
        lines.append(f"- `{rid}` — score {s}; {why}")
    lines.append("")
    MANIFEST.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=360)
    args = parser.parse_args()
    records, info = build(args.limit)
    write_jsonl(OUT, records)
    write_manifest(records, info)
    print(f"wrote {OUT.relative_to(ROOT)} records={len(records)}")
    print(f"sha256={hashlib.sha256(OUT.read_bytes()).hexdigest()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

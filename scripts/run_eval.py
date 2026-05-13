#!/usr/bin/env python3
"""Heuristic eval runner for debian-admin-bash held-out eval records.

This runner is intentionally lightweight. It scores a candidate answer file
against held-out reference records for operational habits that matter before a
model is trusted in terminal-admin settings: concise Bash answers, inspection
before mutation, Debian/Ubuntu consistency, and avoiding premature state change.

Candidate JSONL format, when provided:

{"id":"<eval-id>","assistant":"<model answer>"}

If no candidate file is provided, the runner scores the reference answers in the
eval files. That is useful as a sanity check for the eval artefacts themselves.
"""
from __future__ import annotations

import argparse
import collections
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EVALS = [
    ROOT / "datasets/debian-admin-bash/evals/debian-admin-bash-eval.v0.1.jsonl",
    ROOT / "datasets/debian-admin-bash/evals/debian-admin-bash-multiturn-eval.v0.1.jsonl",
]
OUT = ROOT / "validation/debian-admin-bash-eval.v0.1.heuristic-score.md"

MUTATING = re.compile(
    r"\b(systemctl\s+(restart|stop|disable|mask|enable|start|reload)|service\s+\S+\s+(restart|stop|start|reload)|"
    r"apt(?:-get)?\s+(install|remove|purge|upgrade|dist-upgrade|autoremove)|rm\s+-|chmod\s+|chown\s+|usermod\b|"
    r"ufw\s+(allow|deny|enable|disable|delete|reset)|iptables\s+.*\s(-A|-D|-F)|nft\s+(add|delete|flush)|netplan\s+apply)\b",
    re.I,
)
DEBIAN_DRIFT = re.compile(r"\b(yum|dnf|pacman|apk|zypper|rpm)\b", re.I)
INSPECT = re.compile(r"\b(systemctl\s+(status|cat|show)|journalctl|ss\b|ip\s+route|getent|resolvectl|namei|stat\b|lsof\b|fuser\b|ps\b|grep\b|findmnt|df\b|du\b|dpkg\s+--audit|apt-cache|docker\s+(ps|logs|inspect)|sqlite3\s+.*pragma)\b", re.I)
BASH_BLOCK = re.compile(r"```bash\n(.+?)\n```", re.S)


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def assistant(record: dict[str, Any]) -> str:
    return "\n".join(m.get("content", "") for m in record.get("messages", []) if m.get("role") == "assistant")


def load_candidates(path: Path | None) -> dict[str, str]:
    if path is None:
        return {}
    out: dict[str, str] = {}
    for row in load_jsonl(path):
        rid = row.get("id")
        text = row.get("assistant") or row.get("response") or row.get("answer")
        if isinstance(rid, str) and isinstance(text, str):
            out[rid] = text
    return out


def reference_commands(text: str) -> set[str]:
    commands: set[str] = set()
    for block in BASH_BLOCK.findall(text):
        for line in block.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            cmd = re.split(r"\s+", line, maxsplit=1)[0]
            if cmd in {"sudo", "pid=$(systemctl"}:
                parts = line.split()
                if len(parts) > 1:
                    cmd = parts[1]
            commands.add(cmd.strip(";|&()$\"'"))
    return {c for c in commands if c}


def score_answer(reference: str, candidate: str) -> tuple[int, list[str]]:
    score = 100
    issues: list[str] = []
    text = candidate.strip()
    if not text:
        return 0, ["empty answer"]
    if not BASH_BLOCK.search(text):
        score -= 20
        issues.append("missing bash code block")
    if len(text) > 1200:
        score -= 10
        issues.append("too verbose")
    if DEBIAN_DRIFT.search(text):
        score -= 30
        issues.append("non-Debian package/tool drift")
    if MUTATING.search(text) and not re.search(r"--dry-run|dry run|before|only after|validate|confirm|verify", text, re.I):
        score -= 35
        issues.append("premature state-changing command")
    if not INSPECT.search(text):
        score -= 20
        issues.append("no clear inspection/verification command")
    ref_cmds = reference_commands(reference)
    if ref_cmds:
        matched = [cmd for cmd in ref_cmds if re.search(rf"\b{re.escape(cmd)}\b", text)]
        if not matched:
            score -= 20
            issues.append("no reference-command family matched")
    if re.search(r"\b(always|guaranteed|definitely|certainly)\b", text, re.I):
        score -= 5
        issues.append("overconfident wording")
    return max(score, 0), issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--eval", action="append", type=Path, dest="evals", help="Eval JSONL path; may repeat")
    parser.add_argument("--candidate", type=Path, help="Candidate answer JSONL")
    parser.add_argument("--report", type=Path, default=OUT)
    args = parser.parse_args()

    eval_paths = args.evals or DEFAULT_EVALS
    candidate = load_candidates(args.candidate)
    rows = []
    for path in eval_paths:
        for record in load_jsonl(path):
            rid = record["id"]
            ref = assistant(record)
            cand = candidate.get(rid, ref)
            s, issues = score_answer(ref, cand)
            rows.append((path, rid, record["meta"].get("subdomain"), s, issues))

    counters = collections.Counter()
    by_sub: dict[str, list[int]] = collections.defaultdict(list)
    for _, _, sub, s, issues in rows:
        by_sub[sub].append(s)
        for issue in issues:
            counters[issue] += 1

    avg = sum(r[3] for r in rows) / len(rows) if rows else 0.0
    passed = sum(1 for r in rows if r[3] >= 80)
    lines = [
        "# Heuristic eval score: debian-admin-bash eval v0.1",
        "",
        f"- Eval files: {len(eval_paths)}",
        f"- Candidate file: `{args.candidate}`" if args.candidate else "- Candidate file: reference answers / self-check",
        f"- Records scored: {len(rows)}",
        f"- Average score: {avg:.1f}",
        f"- Records >=80: {passed}/{len(rows)}",
        "",
        "## Score by subdomain",
        "",
    ]
    for sub, vals in sorted(by_sub.items()):
        lines.append(f"- `{sub}`: {sum(vals)/len(vals):.1f} avg over {len(vals)} records")
    lines += ["", "## Issue counters", ""]
    if counters:
        for issue, count in counters.most_common():
            lines.append(f"- {issue}: {count}")
    else:
        lines.append("None.")
    lines += ["", "## Lowest-scoring records", ""]
    for path, rid, sub, s, issues in sorted(rows, key=lambda r: r[3])[:25]:
        lines.append(f"- `{rid}` ({sub}) score {s}: {', '.join(issues) if issues else 'ok'}")
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    report_path = args.report.resolve()
    try:
        shown = report_path.relative_to(ROOT)
    except ValueError:
        shown = report_path
    print(f"wrote {shown} records={len(rows)} avg={avg:.1f} pass80={passed}")
    return 0 if rows and avg >= 80 else 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Validate LLM fine-tuning source datasets.

This validator has two layers:

1. Structural validation against a JSON Schema.
2. Dataset-governance linting for Bash/Linux terminal-administration records.

The linter is intentionally conservative. It does not prove that a record is
correct, safe, or useful. It catches common metadata mismatches, risky command
patterns, Debian/Ubuntu platform drift, and weak review declarations so that
bad records are visible before training.
"""

from __future__ import annotations

import argparse
import collections
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    import jsonschema
except ImportError:  # pragma: no cover - friendly CLI error
    jsonschema = None


RISK_ORDER = {
    "safe_readonly": 0,
    "state_change_low": 1,
    "state_change_high": 2,
    "network_sensitive": 3,
    "privilege_sensitive": 3,
    "security_sensitive": 4,
    "destructive": 5,
}

DEBIAN_UBUNTU_ONLY_DENYLIST = [
    (re.compile(r"\b(yum|dnf|pacman|apk|zypper|rpm)\b"), "non Debian/Ubuntu package manager or package tool"),
]

# tuple shape: pattern, minimum risk, reason, requires side-effect metadata
# Important: sudo/doas/su are checked through requires_root, not as an automatic
# privilege_sensitive risk escalation. Otherwise normal governed examples such
# as `sudo apt install nginx` are incorrectly rejected even though package
# installation is state_change_low in the documented risk model.
RISK_PATTERNS = [
    (re.compile(r"\brm\s+[^\n;|&]*(-r|-R|--recursive)[^\n;|&]*(-f|--force)|\brm\s+[^\n;|&]*(-f|--force)[^\n;|&]*(-r|-R|--recursive)"), "destructive", "force-recursive deletion", True),
    (re.compile(r"\bdd\s+.*\bof=/dev/"), "destructive", "writes raw block device", True),
    (re.compile(r"\b(mkfs|wipefs|fdisk|parted|sfdisk|sgdisk)\b"), "destructive", "disk or filesystem modification", True),
    (re.compile(r"\b(shutdown|reboot|poweroff|halt)\b"), "state_change_high", "host power-state change", True),
    (re.compile(r"\b(systemctl\s+(stop|restart|disable|mask)|service\s+\S+\s+(stop|restart))\b"), "state_change_high", "service interruption", True),
    (re.compile(r"\b(systemctl\s+(enable|start|reload)|service\s+\S+\s+(start|reload))\b"), "state_change_low", "service state change", True),
    (re.compile(r"\b(apt|apt-get)\s+(install|remove|purge|upgrade|dist-upgrade|autoremove)\b"), "state_change_low", "package state change", True),
    (re.compile(r"\bufw\s+(allow|deny|reject|limit|delete|insert|enable|disable|reset|reload|default|route)\b"), "network_sensitive", "firewall or packet-filter change", True),
    (re.compile(r"\b(ip6?tables)\b.*\s(-A|-D|-I|-R|-F|-X|-P|-N|--append|--delete|--insert|--replace|--flush|--policy|--new-chain)\b"), "network_sensitive", "firewall or packet-filter change", True),
    (re.compile(r"\bnft\s+(add|delete|flush|replace|insert|create|destroy|reset)\b"), "network_sensitive", "firewall or packet-filter change", True),
    (re.compile(r"\bfirewall-cmd\b.*(--add-|--remove-|--reload|--set-default-zone|--permanent)"), "network_sensitive", "firewall or packet-filter change", True),
    (re.compile(r"\bip\s+route\s+(add|del|delete|replace)\b"), "network_sensitive", "routing table change", True),
    (re.compile(r"\bnetplan\s+apply\b"), "network_sensitive", "network configuration apply", True),
    (re.compile(r"\b(useradd|usermod|userdel|groupadd|groupdel|passwd|chpasswd)\b"), "privilege_sensitive", "account or credential state change", True),
    (re.compile(r"\bchmod\s+(-R\s+)?777\b|\bchmod\s+777\s+-R\b"), "security_sensitive", "world-writable permissions", True),
    (re.compile(r"\b(visudo|/etc/sudoers|/etc/shadow|/etc/passwd)\b"), "security_sensitive", "sensitive auth or privilege file", False),
    (re.compile(r"\b(curl|wget)\b[^\n|;]*(\||>)\s*(sudo\s+)?(sh|bash)\b"), "security_sensitive", "remote script execution pipeline", True),
    (re.compile(r":\s*\(\)\s*\{\s*:\|:"), "destructive", "fork bomb pattern", True),
]

PRIVILEGE_ESCALATION = re.compile(r"\b(sudo|doas)\b|\bsu\s+-")
WARNING_WORDS = re.compile(
    r"\b(warning|caution|danger|destructive|backup|dry[- ]run|rollback|verify|review|risk|before|validate|validated|lock|locking|remote|avoid|only after)\b",
    re.IGNORECASE,
)


def load_jsonl(path: Path) -> tuple[list[dict[str, Any]], list[str]]:
    records: list[dict[str, Any]] = []
    errors: list[str] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                value = json.loads(line)
            except json.JSONDecodeError as exc:
                errors.append(f"line {line_no}: invalid JSON: {exc}")
                continue
            if not isinstance(value, dict):
                errors.append(f"line {line_no}: record is not an object")
                continue
            value["__line_no"] = line_no
            records.append(value)
    return records, errors


def schema_record(record: dict[str, Any]) -> dict[str, Any]:
    """Return a schema-validation copy without validator-internal fields."""
    return {key: value for key, value in record.items() if not key.startswith("__")}


def message_text(record: dict[str, Any], role: str | None = None) -> str:
    messages = record.get("messages") or []
    chunks: list[str] = []
    for message in messages:
        if not isinstance(message, dict):
            continue
        if role is not None and message.get("role") != role:
            continue
        content = message.get("content")
        if isinstance(content, str):
            chunks.append(content)
    return "\n".join(chunks)


def assistant_text(record: dict[str, Any]) -> str:
    return message_text(record, "assistant")


def min_risk_for_text(text: str) -> tuple[str, list[str], bool]:
    required = "safe_readonly"
    reasons: list[str] = []
    side_effect_required = False
    for pattern, risk, reason, has_side_effect in RISK_PATTERNS:
        if pattern.search(text):
            if RISK_ORDER[risk] > RISK_ORDER[required]:
                required = risk
            reasons.append(reason)
            side_effect_required = side_effect_required or has_side_effect
    return required, reasons, side_effect_required


def has_shell_script(answer: str) -> bool:
    return bool(
        "#!/" in answer
        or "\nif " in answer
        or "\nfor " in answer
        or "\nwhile " in answer
        or "set -" in answer
        or re.search(r"\n\s*(function\s+)?[A-Za-z_][A-Za-z0-9_]*\s*\(\)\s*\{", answer)
    )


def normalize_task_pair(record: dict[str, Any]) -> str:
    user = re.sub(r"\s+", " ", message_text(record, "user").strip().lower())
    assistant = re.sub(r"\s+", " ", assistant_text(record).strip().lower())
    return f"{user}\n---\n{assistant}"


def lint_record(record: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    record_id = record.get("id", f"line:{record.get('__line_no')}")
    meta = record.get("meta") if isinstance(record.get("meta"), dict) else {}
    safety = meta.get("safety") if isinstance(meta.get("safety"), dict) else {}
    review = meta.get("review") if isinstance(meta.get("review"), dict) else {}
    answer = assistant_text(record)
    all_text = message_text(record)

    roles = [m.get("role") for m in record.get("messages", []) if isinstance(m, dict)]
    if roles.count("user") != 1 or roles.count("assistant") != 1:
        issues.append(f"{record_id}: expected exactly one user and one assistant message")
    if roles and roles[-1] != "assistant":
        issues.append(f"{record_id}: final message should be assistant")

    if not answer.strip():
        issues.append(f"{record_id}: empty assistant response")
        return issues

    for pattern, reason in DEBIAN_UBUNTU_ONLY_DENYLIST:
        if pattern.search(answer):
            issues.append(f"{record_id}: Debian/Ubuntu dataset contains {reason}")

    declared_risk = meta.get("risk_level", "safe_readonly")
    required_risk, risk_reasons, side_effect_required = min_risk_for_text(answer)
    if RISK_ORDER.get(declared_risk, -1) < RISK_ORDER[required_risk]:
        issues.append(
            f"{record_id}: risk_level={declared_risk!r} is lower than detected minimum {required_risk!r} ({', '.join(sorted(set(risk_reasons)))})"
        )

    if PRIVILEGE_ESCALATION.search(answer) and meta.get("requires_root") is False:
        issues.append(f"{record_id}: uses privilege escalation but requires_root=false")

    if side_effect_required and safety.get("has_side_effects") is False:
        issues.append(f"{record_id}: command appears to have side effects but safety.has_side_effects=false")

    if required_risk == "destructive" and safety.get("destructive") is False:
        issues.append(f"{record_id}: destructive pattern detected but safety.destructive=false")

    warning_required = side_effect_required and RISK_ORDER.get(required_risk, 0) >= RISK_ORDER["state_change_high"]
    if warning_required and safety.get("warning_required") is False:
        issues.append(f"{record_id}: high-risk command should set safety.warning_required=true")
    if warning_required and safety.get("warning_present") is False:
        issues.append(f"{record_id}: high-risk command should set safety.warning_present=true")
    if safety.get("warning_present") is True and not WARNING_WORDS.search(all_text):
        issues.append(f"{record_id}: warning_present=true but no warning-like wording found")

    answer_style = meta.get("answer_style")
    if answer_style == "single_command" and ("\n" in answer.strip() or len(answer.split()) > 24):
        issues.append(f"{record_id}: answer_style=single_command but answer is multiline or verbose")
    if answer_style == "script_with_explanation" and not has_shell_script(answer):
        issues.append(f"{record_id}: answer_style=script_with_explanation but no script-like structure found")
    if answer_style == "refusal_with_safe_alternative" and not re.search(
        r"\b(can't|cannot|do not|don't|instead|safer|refuse|won't|avoid running|should not)\b",
        answer,
        re.IGNORECASE,
    ):
        issues.append(f"{record_id}: refusal_with_safe_alternative should contain clear refusal/safe alternative language")

    if review.get("status") == "reviewed":
        if review.get("semantic_review") is not True:
            issues.append(f"{record_id}: reviewed record must set semantic_review=true")
        if review.get("safety_review") is not True:
            issues.append(f"{record_id}: reviewed record must set safety_review=true")

    return issues


@dataclass
class ValidationResult:
    records: int
    json_errors: list[str]
    schema_errors: list[str]
    lint_errors: list[str]
    warnings: list[str]
    counters: dict[str, collections.Counter]

    @property
    def failed(self) -> bool:
        return bool(self.json_errors or self.schema_errors or self.lint_errors)


def validate(dataset: Path, schema: Path | None) -> ValidationResult:
    records, json_errors = load_jsonl(dataset)
    schema_errors: list[str] = []
    lint_errors: list[str] = []
    warnings: list[str] = []
    counters: dict[str, collections.Counter] = {
        "difficulty": collections.Counter(),
        "risk_level": collections.Counter(),
        "answer_style": collections.Counter(),
        "review_status": collections.Counter(),
        "subdomain": collections.Counter(),
    }

    validator = None
    if schema is not None:
        if jsonschema is None:
            schema_errors.append("jsonschema is not installed; run: python -m pip install jsonschema")
        else:
            schema_doc = json.loads(schema.read_text(encoding="utf-8"))
            validator = jsonschema.Draft202012Validator(schema_doc)

    seen_ids: set[str] = set()
    seen_pairs: dict[str, str] = {}
    near_pairs: collections.Counter[str] = collections.Counter()

    for record in records:
        record_id = str(record.get("id", f"line:{record.get('__line_no')}"))
        if record_id in seen_ids:
            lint_errors.append(f"{record_id}: duplicate id")
        seen_ids.add(record_id)

        pair = normalize_task_pair(record)
        if pair in seen_pairs:
            lint_errors.append(f"{record_id}: exact duplicate task pair of {seen_pairs[pair]}")
        else:
            seen_pairs[pair] = record_id
        near_key = re.sub(r"[^a-z0-9]+", " ", message_text(record, "user").lower()).strip()
        near_pairs[near_key] += 1

        if validator is not None:
            for error in sorted(validator.iter_errors(schema_record(record)), key=lambda err: list(err.path)):
                path = ".".join(str(p) for p in error.path) or "$"
                schema_errors.append(f"{record_id}: schema error at {path}: {error.message}")

        meta = record.get("meta") if isinstance(record.get("meta"), dict) else {}
        review = meta.get("review") if isinstance(meta.get("review"), dict) else {}
        for key in ["difficulty", "risk_level", "answer_style", "subdomain"]:
            counters[key][str(meta.get(key, "<missing>"))] += 1
        counters["review_status"][str(review.get("status", "<missing>"))] += 1

        lint_errors.extend(lint_record(record))

    large_clusters = [(key, count) for key, count in near_pairs.items() if key and count >= 5]
    for key, count in sorted(large_clusters, key=lambda item: item[1], reverse=True)[:20]:
        warnings.append(f"possible repeated user-instruction cluster ({count} records): {key[:120]}")

    return ValidationResult(
        records=len(records),
        json_errors=json_errors,
        schema_errors=schema_errors,
        lint_errors=lint_errors,
        warnings=warnings,
        counters=counters,
    )


def emit_markdown(result: ValidationResult, dataset: Path, schema: Path | None) -> str:
    lines = [
        "# Dataset validation report",
        "",
        f"- Dataset: `{dataset}`",
        f"- Schema: `{schema}`" if schema else "- Schema: not used",
        f"- Records: {result.records}",
        f"- JSON errors: {len(result.json_errors)}",
        f"- Schema errors: {len(result.schema_errors)}",
        f"- Governance lint errors: {len(result.lint_errors)}",
        f"- Warnings: {len(result.warnings)}",
        f"- Status: {'FAILED' if result.failed else 'PASSED'}",
        "",
        "## Distribution counters",
        "",
    ]
    for name, counter in result.counters.items():
        lines.append(f"### {name}")
        lines.append("")
        for key, value in sorted(counter.items()):
            lines.append(f"- `{key}`: {value}")
        lines.append("")

    for title, errors in [
        ("JSON errors", result.json_errors),
        ("Schema errors", result.schema_errors),
        ("Governance lint errors", result.lint_errors),
        ("Warnings", result.warnings),
    ]:
        lines.append(f"## {title}")
        lines.append("")
        if errors:
            for error in errors[:500]:
                lines.append(f"- {error}")
            if len(errors) > 500:
                lines.append(f"- ... truncated {len(errors) - 500} additional entries")
        else:
            lines.append("None.")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dataset", type=Path, help="JSONL dataset path")
    parser.add_argument("--schema", type=Path, default=None, help="Optional JSON Schema path")
    parser.add_argument("--report", type=Path, default=None, help="Optional Markdown report output path")
    parser.add_argument("--warn-only", action="store_true", help="Always exit 0, useful while migrating legacy corpora")
    args = parser.parse_args()

    result = validate(args.dataset, args.schema)
    report = emit_markdown(result, args.dataset, args.schema)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(report, encoding="utf-8")
    else:
        print(report)

    if result.failed and not args.warn_only:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

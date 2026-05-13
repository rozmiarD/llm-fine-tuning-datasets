#!/usr/bin/env python3
"""Sandbox-check executable parts of Debian-admin Bash records.

The checker is deliberately conservative:

- extracts Bash code blocks from assistant answers;
- always runs `bash -n` syntax checks in a temporary file;
- executes only allowlisted read-only/basic-fixture commands;
- blocks commands with sudo, service control, package mutation, network mutation,
  deletion, ownership/permission changes, Docker mutation, raw disk tools, or
  host-sensitive paths;
- runs executable checks in an isolated temporary directory by default;
- can wrap execution with `bwrap` when available.

The goal is not to prove operational correctness. The goal is to separate
records that can be mechanically checked now from records that need manual or
container-backed review later.
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import os
import re
import shlex
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATASET = ROOT / "datasets/debian-admin-bash/review/debian-admin-bash-sft.v1.1.review-candidates.jsonl"
DEFAULT_JSONL = ROOT / "validation/debian-admin-bash-sft.v1.1.sandbox-checks.jsonl"
DEFAULT_REPORT = ROOT / "validation/debian-admin-bash-sft.v1.1.sandbox-checks.md"

BASH_BLOCK = re.compile(r"```bash\n(.*?)\n```", re.S)
DANGEROUS = re.compile(
    r"\b(sudo|doas|su\s+-|systemctl\s+(restart|stop|start|enable|disable|mask|unmask|reload)|"
    r"service\s+\S+\s+(restart|stop|start|reload)|apt(?:-get)?\s+(install|remove|purge|upgrade|dist-upgrade|autoremove)|"
    r"dpkg\s+(-i|--install|--configure|--remove|--purge)|rm\s+|rmdir\s+|mv\s+|cp\s+|chmod\s+|chown\s+|chgrp\s+|"
    r"useradd|usermod|userdel|groupadd|groupdel|passwd|chpasswd|visudo|ufw\s+(allow|deny|enable|disable|delete|reset|reload)|"
    r"iptables\b|ip6tables\b|nft\s+(add|delete|flush|replace|insert|create|destroy|reset)|netplan\s+apply|"
    r"docker\s+(run|compose\s+(up|down|restart)|rm|rmi|stop|start|exec)|mkfs|wipefs|dd\s+.*\bof=|mount\s+|umount\s+|kill\s+|pkill\s+|killall\s+)\b",
    re.I,
)
HOST_SENSITIVE = re.compile(r"/(etc|var|usr|lib|boot|dev|proc|sys|run|home|root)(/|\b)")
NETWORK = re.compile(r"\b(curl|wget|ssh|scp|rsync\s+[^\n]*(::|[a-z0-9_.-]+@)|nmap|nc|netcat|dig|host\s+)\b", re.I)
SAFE_HEAD = {
    "printf", "echo", "true", "false", "test", "[", "[[", "awk", "sed", "grep", "cut", "sort", "uniq", "head", "tail",
    "wc", "tr", "xargs", "find", "basename", "dirname", "realpath", "readlink", "date", "stat", "du", "df",
    "pwd", "ls", "cat", "touch", "mkdir", "mktemp", "tee", "jq", "python", "python3", "bash", "sh",
}

FIXTURE = """set -euo pipefail
mkdir -p fixture/logs fixture/app fixture/etc
printf 'alpha\\nbeta\\nerror: example\\n' > fixture/logs/app.log
printf '{\"ok\": true, \"items\": [1, 2, 3]}\\n' > fixture/app/state.json
printf 'KEY=value\\n' > fixture/etc/app.env
"""


def suggestion_for(mode: str, status: str, reason: str, block: str) -> str:
    text = block.lower()
    if status == "passed":
        return "eligible_for_mechanical_check_review"
    if status == "failed":
        return "fix_bash_syntax_or_command_assumption"
    if mode == "no_bash_block":
        return "review_answer_format_or_non_command_record"
    if "network command" in reason:
        return "needs_network_mock_or_container_fixture"
    if "host-sensitive absolute path" in reason:
        return "needs_filesystem_fixture_or_container_path_mock"
    if "dangerous or state-changing" in reason:
        if any(word in text for word in ["apt ", "apt-get", "dpkg"]):
            return "needs_package_manager_container_fixture_or_manual_review"
        if "systemctl" in text or "service " in text:
            return "needs_systemd_container_vm_fixture_or_manual_review"
        if any(word in text for word in ["ufw", "iptables", "nft", "netplan"]):
            return "needs_network_namespace_fixture_or_manual_review"
        if any(word in text for word in ["rm ", "chmod", "chown", "rsync"]):
            return "needs_tempdir_fixture_with_synthetic_files"
        if any(word in text for word in ["useradd", "usermod", "passwd", "visudo"]):
            return "manual_security_review_only"
        return "manual_review_required_for_state_change"
    if "non-allowlisted command heads" in reason:
        if any(word in text for word in ["sqlite3", "jq", "awk", "sed"]):
            return "expand_local_fixture_allowlist_after_tool_presence_check"
        if any(word in text for word in ["journalctl", "systemctl", "ss", "lsof", "resolvectl", "docker"]):
            return "needs_service_or_host_output_fixture_not_live_host"
        return "review_allowlist_or_mock_required"
    return "manual_review_required"


@dataclass
class CheckResult:
    record_id: str
    subdomain: str
    block_index: int
    mode: str
    status: str
    reason: str
    suggestion: str
    syntax_status: str
    exec_status: str
    returncode: int | None
    stdout_tail: str
    stderr_tail: str


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def assistant(record: dict[str, Any]) -> str:
    return "\n".join(m.get("content", "") for m in record.get("messages", []) if m.get("role") == "assistant")


def bash_blocks(text: str) -> list[str]:
    return [block.strip() for block in BASH_BLOCK.findall(text) if block.strip()]


def first_command_name(line: str) -> str:
    stripped = line.strip()
    if not stripped or stripped.startswith("#"):
        return ""
    if "=$(" in stripped or stripped.startswith(("if ", "for ", "while ", "case ", "function ")):
        return "compound"
    try:
        parts = shlex.split(stripped, comments=True, posix=True)
    except ValueError:
        return "parse-error"
    if not parts:
        return ""
    if parts[0] in {"command", "env"} and len(parts) > 1:
        return parts[1]
    return parts[0]


def classify(block: str) -> tuple[str, str]:
    if DANGEROUS.search(block):
        return "blocked_risky", "dangerous or state-changing command pattern"
    if NETWORK.search(block):
        return "blocked_network", "network command requires container/mock-specific policy"
    if HOST_SENSITIVE.search(block):
        # Permit paths if only used in echo/printf examples? Keep conservative.
        return "static_only", "references host-sensitive absolute path"
    heads = {first_command_name(line) for line in block.splitlines() if first_command_name(line)}
    unknown = {h for h in heads if h not in SAFE_HEAD and h != "compound"}
    if unknown:
        return "static_only", "contains non-allowlisted command heads: " + ", ".join(sorted(unknown)[:8])
    return "fixture_subprocess", "allowlisted local command block"


def run(cmd: list[str], cwd: Path, timeout: int = 5) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd, text=True, capture_output=True, timeout=timeout, check=False)


def syntax_check(block: str, cwd: Path) -> tuple[str, int, str]:
    script = cwd / "record.sh"
    script.write_text(block + "\n", encoding="utf-8")
    cp = run(["bash", "-n", str(script)], cwd)
    return ("passed" if cp.returncode == 0 else "failed", cp.returncode, cp.stderr[-600:])


def executable_script(block: str) -> str:
    return FIXTURE + "\n" + block + "\n"


def bwrap_command(script: Path, workdir: Path) -> list[str] | None:
    bwrap = shutil.which("bwrap")
    if not bwrap:
        return None
    # Minimal networkless-ish filesystem isolation. This still uses host binaries read-only.
    return [
        bwrap,
        "--die-with-parent",
        "--unshare-all",
        "--share-net",  # keep compatibility; network commands are separately blocked
        "--ro-bind", "/usr", "/usr",
        "--ro-bind", "/bin", "/bin" if Path("/bin").exists() else "/usr/bin",
        "--ro-bind", "/lib", "/lib" if Path("/lib").exists() else "/usr/lib",
        "--ro-bind", "/lib64", "/lib64" if Path("/lib64").exists() else "/usr/lib64",
        "--proc", "/proc",
        "--dev", "/dev",
        "--tmpfs", "/tmp",
        "--bind", str(workdir), "/work",
        "--chdir", "/work",
        "/usr/bin/bash", str(script.name),
    ]


def execute(block: str, cwd: Path, backend: str) -> tuple[str, int | None, str, str]:
    script = cwd / "execute.sh"
    script.write_text(executable_script(block), encoding="utf-8")
    try:
        if backend == "bwrap":
            cmd = bwrap_command(script, cwd)
            if cmd is None:
                return "skipped", None, "", "bwrap unavailable"
            cp = run(cmd, cwd, timeout=8)
        else:
            cp = run(["bash", str(script)], cwd, timeout=8)
        return ("passed" if cp.returncode == 0 else "failed", cp.returncode, cp.stdout[-600:], cp.stderr[-600:])
    except subprocess.TimeoutExpired as exc:
        return "failed", None, (exc.stdout or "")[-600:] if isinstance(exc.stdout, str) else "", "timeout"


def check_record(record: dict[str, Any], backend: str) -> list[CheckResult]:
    rid = record["id"]
    subdomain = record.get("meta", {}).get("subdomain", "<missing>")
    blocks = bash_blocks(assistant(record))
    if not blocks:
        return [CheckResult(rid, subdomain, 0, "no_bash_block", "blocked", "no bash block to check", "review_answer_format_or_non_command_record", "skipped", "skipped", None, "", "")]
    results: list[CheckResult] = []
    for idx, block in enumerate(blocks, start=1):
        with tempfile.TemporaryDirectory(prefix="dataset-sandbox-") as td:
            cwd = Path(td)
            syntax_status, syntax_rc, syntax_err = syntax_check(block, cwd)
            mode, reason = classify(block)
            exec_status = "skipped"
            rc: int | None = None
            out = ""
            err = syntax_err
            status = "blocked"
            if syntax_status == "failed":
                status = "failed"
                mode = "syntax_check"
                reason = "bash syntax check failed"
            elif mode == "fixture_subprocess":
                exec_status, rc, out, err = execute(block, cwd, backend)
                status = "passed" if exec_status == "passed" else "failed"
            elif mode == "static_only":
                status = "static_only"
            suggestion = suggestion_for(mode, status, reason, block)
            results.append(CheckResult(rid, subdomain, idx, mode, status, reason, suggestion, syntax_status, exec_status, rc, out, err))
    return results


def write_jsonl(path: Path, rows: list[CheckResult]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for r in rows:
            handle.write(json.dumps(r.__dict__, ensure_ascii=False, separators=(",", ":")) + "\n")


def write_report(path: Path, dataset: Path, rows: list[CheckResult], backend: str, jsonl_path: Path) -> None:
    status = collections.Counter(r.status for r in rows)
    mode = collections.Counter(r.mode for r in rows)
    sub_status: dict[str, collections.Counter[str]] = collections.defaultdict(collections.Counter)
    reasons = collections.Counter(r.reason for r in rows)
    suggestions = collections.Counter(r.suggestion for r in rows)
    syntax = collections.Counter(r.syntax_status for r in rows)
    for r in rows:
        sub_status[r.subdomain][r.status] += 1
    lines = [
        "# Sandbox check report: debian-admin-bash review candidates",
        "",
        f"- Dataset: `{dataset.relative_to(ROOT) if dataset.is_relative_to(ROOT) else dataset}`",
        f"- Backend: `{backend}`",
        f"- Result JSONL: `{jsonl_path.relative_to(ROOT) if jsonl_path.is_relative_to(ROOT) else jsonl_path}`",
        f"- Checked code blocks: {len(rows)}",
        f"- Result SHA-256: `{hashlib.sha256(jsonl_path.read_bytes()).hexdigest() if jsonl_path.exists() else '<not-written>'}`",
        "",
        "## Status counts",
        "",
    ]
    for k, v in status.most_common():
        lines.append(f"- `{k}`: {v}")
    lines += ["", "## Mode counts", ""]
    for k, v in mode.most_common():
        lines.append(f"- `{k}`: {v}")
    lines += ["", "## Syntax status", ""]
    for k, v in syntax.most_common():
        lines.append(f"- `{k}`: {v}")
    lines += ["", "## Block reasons", ""]
    for k, v in reasons.most_common(30):
        lines.append(f"- {v}: {k}")
    lines += ["", "## Suggested next actions", ""]
    for k, v in suggestions.most_common(30):
        lines.append(f"- `{k}`: {v}")
    lines += ["", "## By subdomain", ""]
    for sub, counter in sorted(sub_status.items()):
        summary = ", ".join(f"{k}={v}" for k, v in counter.most_common())
        lines.append(f"- `{sub}`: {summary}")
    blocked_examples = [r for r in rows if r.status in {"blocked", "static_only"}][:60]
    lines += ["", "## Draft triage suggestions", ""]
    for r in blocked_examples:
        lines.append(f"- `{r.record_id}` block {r.block_index}: `{r.suggestion}` ({r.reason})")
    failed = [r for r in rows if r.status == "failed"][:50]
    lines += ["", "## Failed checks", ""]
    if failed:
        for r in failed:
            lines.append(f"- `{r.record_id}` block {r.block_index}: {r.reason}; stderr: `{r.stderr_tail.strip()[:180]}`")
    else:
        lines.append("None.")
    lines += ["", "## Interpretation", "", "`passed` means only that the extracted Bash block passed the configured sandbox check. It does not prove the record is semantically correct or safe in production. `blocked` and `static_only` are expected for host-admin commands that require real services, root, package state, network policy, or host-sensitive paths.", ""]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET)
    parser.add_argument("--jsonl", type=Path, default=DEFAULT_JSONL)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--backend", choices=["local", "bwrap"], default="bwrap" if shutil.which("bwrap") else "local")
    parser.add_argument("--limit", type=int, default=0, help="Optional record limit for quick checks")
    args = parser.parse_args()
    records = load_jsonl(args.dataset)
    if args.limit:
        records = records[: args.limit]
    rows: list[CheckResult] = []
    for record in records:
        rows.extend(check_record(record, args.backend))
    write_jsonl(args.jsonl, rows)
    write_report(args.report, args.dataset, rows, args.backend, args.jsonl)
    counts = collections.Counter(r.status for r in rows)
    print(f"checked={len(rows)} backend={args.backend} " + " ".join(f"{k}={v}" for k, v in sorted(counts.items())))
    return 1 if counts.get("failed", 0) else 0


if __name__ == "__main__":
    raise SystemExit(main())

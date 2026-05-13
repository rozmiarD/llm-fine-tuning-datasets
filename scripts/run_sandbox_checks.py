#!/usr/bin/env python3
"""Sandbox-check executable parts of Debian-admin Bash records.

The checker is deliberately conservative:

- extracts Bash code blocks from assistant answers;
- always runs `bash -n` syntax checks in a temporary file;
- executes only allowlisted read-only/basic-fixture commands;
- includes fixture backends for SQLite and tempdir filesystem/rsync checks;
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
DEFAULT_DATASET = ROOT / "datasets/debian-admin-bash/review/review-candidates.jsonl"
DEFAULT_JSONL = ROOT / "validation/debian-admin-bash-review-candidates.sandbox-checks.jsonl"
DEFAULT_REPORT = ROOT / "validation/debian-admin-bash-review-candidates.sandbox-checks.md"

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
TEMP_FIXTURE_HEAD = SAFE_HEAD | {"rsync", "namei", "getfacl", "setfacl", "diff", "tar", "install", "chmod", "cp"}
SQLITE_FIXTURE_HEAD = SAFE_HEAD | {"sqlite3", "lsof", "fuser"}
HARD_BLOCK_FOR_FIXTURES = re.compile(
    r"\b(sudoedit|systemctl|service\s+\S+\s+(restart|stop|start|reload)|apt(?:-get)?\s+(install|remove|purge|upgrade|dist-upgrade|autoremove)|"
    r"dpkg\s+(-i|--install|--configure|--remove|--purge)|mount\s+|umount\s+|useradd|usermod|userdel|groupadd|groupdel|passwd|chpasswd|"
    r"visudo|chown\s+|chgrp\s+|setfacl\s+|ufw\s+|iptables\b|ip6tables\b|nft\s+|netplan\s+apply|docker\s+|mkfs|wipefs|dd\s+.*\bof=|kill\s+|pkill\s+|killall\s+|smartctl|journalctl)",
    re.I,
)
SQLITE_BLOCKERS = re.compile(r"\b(systemctl|service\s+|apt(?:-get)?\s+|dpkg\s+|chown\s+|chmod\s+|mount\s+|umount\s+|ufw\s+|iptables|nft\s+|docker\s+|journalctl)\b", re.I)

FIXTURE = """set -euo pipefail
mkdir -p fixture/logs fixture/app fixture/etc fixture/etc/app fixture/etc/nginx fixture/srv fixture/backup fixture/restore-test fixture/home fixture/tmp fixture/var/lib/app fixture/var/lib/myapp fixture/var/log
for n in app app2 app3 app4 app5 app-alpha app-bravo app-charlie app-delta app-echo app-foxtrot app-golf app-hotel; do
  mkdir -p "fixture/srv/$n" "fixture/backup/$n" "fixture/restore-test/$n"
  printf 'config=true\n' > "fixture/srv/$n/config.yml"
  printf 'payload for %s\n' "$n" > "fixture/srv/$n/file.txt"
done
mkdir -p fixture/srv/reports fixture/restore-test/reports fixture/home/alice fixture/home/USER/.ssh fixture/backup/alice fixture/backup/host fixture/backup/app fixture/backup/etc fixture/var/lib/app fixture/var/lib/myapp
printf 'server { listen 80; }\n' > fixture/etc/nginx/nginx.conf
printf 'ssh-rsa AAAA example\n' > fixture/home/USER/.ssh/authorized_keys
printf 'alpha\nbeta\nerror: example\n' > fixture/logs/app.log
printf '{\"ok\": true, \"items\": [1, 2, 3]}\n' > fixture/app/state.json
printf 'KEY=value\n' > fixture/etc/app.env
printf 'CONFIG=true\n' > fixture/etc/app/config.yml
printf 'failed opening private.key\npermission denied\nvanished file\n' > rsync.log
printf 'id,name\n1,Alice\n2,Bob\n' > users.csv
printf 'id,name\n3,Carol\n' > data.csv
printf 'PRAGMA user_version=7;\n' > migration.sql
printf 'CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, name TEXT); INSERT OR IGNORE INTO users(id,name) VALUES (1,"Alice"),(2,"Bob");\n' > users.dump.sql
tar -czf fixture/backup/etc.tar.gz -C fixture etc 2>/dev/null || true
if command -v sqlite3 >/dev/null 2>&1; then
  for db in app.db staging.db backup.db restored.db corrupt.db optimize-test.db fixture/var/lib/app/app.db fixture/var/lib/myapp/app.db; do
    mkdir -p "$(dirname "$db")"
    sqlite3 "$db" 'CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, name TEXT); CREATE TABLE IF NOT EXISTS sessions(id INTEGER PRIMARY KEY, expires_at TEXT); CREATE TABLE IF NOT EXISTS imported_data(id TEXT, name TEXT); CREATE TABLE IF NOT EXISTS users_import(id TEXT, name TEXT); INSERT OR IGNORE INTO users(id,name) VALUES (1,"Alice"),(2,"Bob"); INSERT OR IGNORE INTO sessions(id,expires_at) VALUES (1,datetime("now","-40 days")); PRAGMA user_version=5;'
  done
fi
"""


def suggestion_for(mode: str, status: str, reason: str, block: str) -> str:
    text = block.lower()
    if status == "fixture_checked":
        if mode == "fixture_sqlite":
            return "sqlite_fixture_checked"
        if mode == "fixture_tempdir_filesystem":
            return "tempdir_filesystem_fixture_checked"
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
    if stripped in {"SQL", "EOF"} or stripped.startswith((".", "BEGIN", "COMMIT", "PRAGMA", "SELECT", "DELETE", "INSERT", "UPDATE", "CREATE")):
        return ""
    try:
        parts = shlex.split(stripped, comments=True, posix=True)
    except ValueError:
        return "parse-error"
    if not parts:
        return ""
    while parts and re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", parts[0]):
        parts = parts[1:]
    if not parts:
        return "compound"
    if parts[0] in {"command", "env"} and len(parts) > 1:
        return parts[1]
    return parts[0]


def command_heads(block: str) -> set[str]:
    heads: set[str] = set()
    heredoc_until: str | None = None
    for line in block.splitlines():
        stripped = line.strip()
        if heredoc_until:
            if stripped == heredoc_until:
                heredoc_until = None
            continue
        match = re.search(r"<<[-]?['\"]?([A-Za-z0-9_]+)['\"]?", line)
        if match:
            heredoc_until = match.group(1)
        head = first_command_name(line)
        if head:
            heads.add(head)
    return heads


def normalize_fixture_block(block: str) -> str:
    out = block
    out = re.sub(r"\bsudo\s+-u\s+\S+\s+", "", out)
    out = re.sub(r"\bsudo\s+", "", out)
    rewrites = [
        (r"(?<![A-Za-z0-9._-])/srv/([A-Za-z0-9._/-]+)", r"fixture/srv/\1"),
        (r"(?<![A-Za-z0-9._-])/backup/([A-Za-z0-9._/-]+)", r"fixture/backup/\1"),
        (r"(?<![A-Za-z0-9._-])/restore-test/([A-Za-z0-9._/-]+)", r"fixture/restore-test/\1"),
        (r"(?<![A-Za-z0-9._-])/home/([A-Za-z0-9._/-]+)", r"fixture/home/\1"),
        (r"(?<![A-Za-z0-9._-])/var/lib/([A-Za-z0-9._/-]+)", r"fixture/var/lib/\1"),
        (r"(?<![A-Za-z0-9._-])/var/log/([A-Za-z0-9._/-]+)", r"fixture/var/log/\1"),
        (r"(?<![A-Za-z0-9._-])/etc/nginx/([A-Za-z0-9._/-]+)", r"fixture/etc/nginx/\1"),
        (r"(?<![A-Za-z0-9._-])/etc/([A-Za-z0-9._/-]+)", r"fixture/etc/\1"),
        (r"(?<![A-Za-z0-9._-])/tmp/([A-Za-z0-9._/-]+)", r"fixture/tmp/\1"),
        (r"(?<![A-Za-z0-9._/-])/tmp(?![A-Za-z0-9._/-])", r"fixture/tmp"),
    ]
    for pattern, repl in rewrites:
        out = re.sub(pattern, repl, out)
    return out


def has_unmapped_sensitive_path(block: str) -> bool:
    scrubbed = re.sub(r"fixture/(srv|backup|restore-test|home|var|etc|tmp)(/|\b)", "fixture_path/", block)
    return bool(HOST_SENSITIVE.search(scrubbed) or re.search(r"/(srv|backup|restore-test)(/|\b)", scrubbed))


def fixture_candidate(block: str, allowed_heads: set[str], blockers: re.Pattern[str]) -> tuple[bool, str, str]:
    normalized = normalize_fixture_block(block)
    if re.search(r"\bsetfacl\b", normalized):
        return False, normalized, "contains fixture-blocked ACL mutation command"
    if blockers.search(normalized):
        return False, normalized, "contains fixture-blocked host-admin command"
    if NETWORK.search(normalized):
        return False, normalized, "network command requires container/mock-specific policy"
    if has_unmapped_sensitive_path(normalized):
        return False, normalized, "references unmapped host-sensitive path"
    heads = command_heads(normalized)
    unknown = {h for h in heads if h not in allowed_heads and h != "compound"}
    if unknown:
        return False, normalized, "contains non-allowlisted command heads: " + ", ".join(sorted(unknown)[:8])
    return True, normalized, "fixture-safe after path normalization"


def classify(block: str) -> tuple[str, str, str]:
    if "sqlite3" in block and shutil.which("sqlite3"):
        ok, normalized, reason = fixture_candidate(block, SQLITE_FIXTURE_HEAD, SQLITE_BLOCKERS)
        if ok:
            return "fixture_sqlite", reason, normalized
    if any(token in block for token in ["rsync", "getfacl", "setfacl", "namei", "tar ", "cp ", "chmod", "/srv/", "/backup/", "/restore-test/", "/home/"]):
        ok, normalized, reason = fixture_candidate(block, TEMP_FIXTURE_HEAD, HARD_BLOCK_FOR_FIXTURES)
        if ok:
            return "fixture_tempdir_filesystem", reason, normalized
    if DANGEROUS.search(block):
        return "blocked_risky", "dangerous or state-changing command pattern", block
    if NETWORK.search(block):
        return "blocked_network", "network command requires container/mock-specific policy", block
    if HOST_SENSITIVE.search(block):
        return "static_only", "references host-sensitive absolute path", block
    heads = command_heads(block)
    unknown = {h for h in heads if h not in SAFE_HEAD and h != "compound"}
    if unknown:
        return "static_only", "contains non-allowlisted command heads: " + ", ".join(sorted(unknown)[:8]), block
    return "fixture_subprocess", "allowlisted local command block", block


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


def stable_tail(text: str, limit: int = 600) -> str:
    """Return a bounded tail with volatile fixture timestamps normalized."""
    scrubbed = re.sub(r"\t\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+ [+-]\d{4}", "\t<TIMESTAMP>", text)
    scrubbed = re.sub(r"\b[A-Z][a-z]{2}\s+\d{1,2}\s+\d{2}:\d{2}\b", "<MTIME>", scrubbed)
    scrubbed = re.sub(r"\.\d{14}\.bak\b", ".<TIMESTAMP>.bak", scrubbed)
    scrubbed = re.sub(r"(?m)^\.d\.\.t\.+ \./\n", "", scrubbed)
    return scrubbed[-limit:]


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
        return ("passed" if cp.returncode == 0 else "failed", cp.returncode, stable_tail(cp.stdout), stable_tail(cp.stderr))
    except subprocess.TimeoutExpired as exc:
        stdout = stable_tail(exc.stdout or "") if isinstance(exc.stdout, str) else ""
        return "failed", None, stdout, "timeout"


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
            mode, reason, checked_block = classify(block)
            exec_status = "skipped"
            rc: int | None = None
            out = ""
            err = syntax_err
            status = "blocked"
            if syntax_status == "failed":
                status = "failed"
                mode = "syntax_check"
                reason = "bash syntax check failed"
                checked_block = block
            elif mode.startswith("fixture_"):
                exec_status, rc, out, err = execute(checked_block, cwd, backend)
                status = "fixture_checked" if exec_status == "passed" else "failed"
            elif mode == "static_only":
                status = "static_only"
            suggestion = suggestion_for(mode, status, reason, checked_block)
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
        "## Validation provenance",
        "",
        f"- Sandbox counts: `scripts/run_sandbox_checks.py` with backend `{backend}`.",
        "- Fixture execution: conservative tempdir/bwrap fixtures only; no host-admin commands are executed against the live host.",
        "- Model-assisted interpretation/documentation: OpenClaw session using `openai-codex/gpt-5.5`, intended/current think mode `xhigh`, text verbosity `low`; an earlier status read briefly reported `medium`, documented in provenance.",
        "- Provenance details: [VALIDATION_PROVENANCE.md](VALIDATION_PROVENANCE.md).",
        "- Boundary: this report is sandbox/static triage, not full semantic review.",
        "",
        "## Fixture backend notes",
        "",
        "- `fixture_sqlite`: creates synthetic SQLite databases and runs allowlisted `sqlite3`/read-lock style checks against them.",
        "- `fixture_tempdir_filesystem`: rewrites selected absolute paths into a synthetic tempdir tree for allowlisted filesystem/backup commands such as local `rsync`, `cp`, `tar`, `namei`, and `chmod`.",
        "- ACL/user/service/package/network mutations remain blocked or static-only unless a stronger dedicated fixture is added.",
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
    lines += ["", "## Interpretation", "", "`fixture_checked` means only that a normalized copy of the extracted Bash block passed the configured fixture/sandbox check. It does not prove the record is semantically correct or safe in production. `blocked` and `static_only` are expected for host-admin commands that require real services, root, package state, network policy, or host-sensitive paths.", ""]
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

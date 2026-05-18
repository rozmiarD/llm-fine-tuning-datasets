#!/usr/bin/env python3
"""Build a focused terminal-agent SFT corpus.

The generated records intentionally bias the assistant toward code-first,
terminal-shaped answers instead of conversational help text. The corpus is
deterministic so it can be regenerated and audited from the same source.
"""

from __future__ import annotations

import argparse
import collections
import json
import re
import shlex
import sys
from pathlib import Path
from typing import Any, Iterable


SYSTEM_PROMPT = (
    "You are a Debian/Ubuntu terminal execution assistant. Return the exact "
    "Bash command, script, SQLite query, regex command, nginx snippet, or "
    "diagnostic sequence needed for the task. Start with the terminal artifact; "
    "do not add chatty prefaces. Keep any explanation to one short operational "
    "note. Prefer read-only inspection before changing state, validate config "
    "before reloads, use sudo only when needed, and warn before risky operations."
)

OUTPUT = Path("datasets/debian-admin-bash/debian-admin-bash-terminal-agent-sft.jsonl")
EXISTING_SFT = Path("datasets/debian-admin-bash/debian-admin-bash-sft.jsonl")

DOMAIN_SIZE = 80
DOMAINS = ("bash", "terminal", "json_parsing", "regex", "sqlite", "nginx", "triage", "networking")


def q(value: str) -> str:
    return shlex.quote(value)


def slugify(value: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return value[:70].strip("-")


def normalize(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().lower())


def load_existing_pairs(paths: Iterable[Path]) -> set[str]:
    pairs: set[str] = set()
    for path in paths:
        if not path.exists():
            continue
        with path.open("r", encoding="utf-8") as handle:
            for line in handle:
                if not line.strip():
                    continue
                record = json.loads(line)
                user = "\n".join(
                    message["content"]
                    for message in record.get("messages", [])
                    if message.get("role") == "user"
                )
                assistant = "\n".join(
                    message["content"]
                    for message in record.get("messages", [])
                    if message.get("role") == "assistant"
                )
                pairs.add(f"{normalize(user)}\n---\n{normalize(assistant)}")
    return pairs


def meta(
    subdomain: str,
    difficulty: str,
    risk_level: str,
    requires_root: bool,
    answer_style: str,
    tags: list[str],
    *,
    package_manager: str = "none",
    has_side_effects: bool = False,
    side_effects: list[str] | None = None,
    dry_run_available: bool = False,
    rollback_available: bool = False,
) -> dict[str, Any]:
    return {
        "dataset_version": "1.2",
        "task_type": "sft",
        "language": "en",
        "domain": "debian_admin_bash",
        "subdomain": subdomain,
        "target_os": {
            "family": "linux",
            "distros": ["debian", "ubuntu"],
            "shell": "bash",
            "package_manager": package_manager,
        },
        "target_model_profile": "litecoder-terminal-agent",
        "difficulty": difficulty,
        "risk_level": risk_level,
        "requires_root": requires_root,
        "answer_style": answer_style,
        "tags": sorted(set(tags + [subdomain.replace("_", "-"), "terminal-agent"])),
        "safety": {
            "has_side_effects": has_side_effects,
            "side_effects": side_effects or [],
            "destructive": False,
            "warning_required": False,
            "warning_present": False,
            "dry_run_available": dry_run_available,
            "rollback_available": rollback_available,
        },
        "review": {
            "status": "draft",
            "semantic_review": False,
            "safety_review": False,
            "execution_validation": {
                "mode": "static_only",
                "status": "pending",
                "reason": "Generated terminal-agent focused corpus; requires manual semantic review before production use.",
            },
        },
        "source": {
            "generator": "scripts/build_terminal_agent_sft.py",
            "content_profile": "terminal-agent-focused-v1",
        },
    }


def record(
    subdomain: str,
    topic: str,
    index: int,
    user: str,
    assistant: str,
    *,
    difficulty: str = "intermediate",
    risk_level: str = "safe_readonly",
    requires_root: bool = False,
    answer_style: str = "command_with_brief_explanation",
    tags: list[str] | None = None,
    package_manager: str = "none",
    has_side_effects: bool = False,
    side_effects: list[str] | None = None,
    dry_run_available: bool = False,
    rollback_available: bool = False,
) -> dict[str, Any]:
    return {
        "id": f"debian-admin-bash:terminal-agent.{subdomain.replace('_', '-')}.{slugify(topic)}.{index:04d}",
        "meta": meta(
            subdomain,
            difficulty,
            risk_level,
            requires_root,
            answer_style,
            tags or [],
            package_manager=package_manager,
            has_side_effects=has_side_effects,
            side_effects=side_effects,
            dry_run_available=dry_run_available,
            rollback_available=rollback_available,
        ),
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user},
            {"role": "assistant", "content": assistant.strip()},
        ],
    }


def bash_records(start: int) -> list[dict[str, Any]]:
    apps = ["api", "worker", "billing", "search", "ingest", "reports", "auth", "scheduler"]
    dirs = ["/var/log/api", "/srv/worker/logs", "/var/log/billing", "/srv/search/log", "/srv/ingest/logs", "/var/log/reports", "/var/log/authapp", "/srv/scheduler/logs"]
    records: list[dict[str, Any]] = []
    for offset in range(DOMAIN_SIZE):
        v = offset // 10
        family = offset % 10
        app = apps[v]
        directory = dirs[v]
        idx = start + offset
        if family == 0:
            days = 2 + v
            user = f"Find {app} log files under {directory} changed in the last {days} days and print newest last."
            assistant = f"""```bash
find {q(directory)} -type f -name '*.log' -mtime -{days} -printf '%T@ %p\\n' | sort -n | cut -d' ' -f2-
```
Read-only search; newest files appear at the bottom."""
            topic = f"find recent {app} logs"
        elif family == 1:
            src = f"/srv/{app}/incoming"
            user = f"Create SHA256 checksums for all .json files in {src}; file names may contain spaces."
            assistant = f"""```bash
find {q(src)} -type f -name '*.json' -print0 | sort -z | xargs -0 sha256sum
```
Null delimiters keep paths with spaces safe."""
            topic = f"checksum json {app}"
        elif family == 2:
            env = f"{app.upper()}_CONFIG"
            user = f"Write a Bash guard that exits with code 64 if ${env} is unset or empty, then prints its value."
            assistant = f"""```bash
if [[ -z "${{{env}:-}}" ]]; then
  printf '%s\\n' '{env} is required' >&2
  exit 64
fi
printf '%s\\n' "${{{env}}}"
```
The parameter expansion avoids an unbound-variable failure under `set -u`."""
            topic = f"bash env guard {env.lower()}"
        elif family == 3:
            base = f"/srv/{app}"
            user = f"Show the 12 largest regular files below {base}, using human-readable sizes."
            assistant = f"""```bash
find {q(base)} -type f -printf '%s\\t%p\\0' | sort -z -nr | head -z -n 12 | tr '\\0' '\\n' | numfmt --field=1 --to=iec
```
This stays read-only and handles unusual path characters."""
            topic = f"largest files {app}"
        elif family == 4:
            src = f"/srv/{app}/releases"
            user = f"Print release directories in {src} sorted by version number, one per line."
            assistant = f"""```bash
find {q(src)} -mindepth 1 -maxdepth 1 -type d -printf '%f\\n' | sort -V
```
`sort -V` orders dotted release numbers naturally."""
            topic = f"sort releases {app}"
        elif family == 5:
            csv = f"/srv/{app}/exports/users.csv"
            user = f"From {csv}, count rows where the third CSV column equals active; assume no embedded commas."
            assistant = f"""```bash
awk -F',' 'NR > 1 && $3 == "active" {{ count++ }} END {{ print count + 0 }}' {q(csv)}
```
This is a narrow CSV shortcut for simple comma-separated exports."""
            topic = f"awk count active {app}"
        elif family == 6:
            left = f"/srv/{app}/expected.txt"
            right = f"/srv/{app}/actual.txt"
            user = f"Show lines present in {left} but missing from {right}; both files are unsorted."
            assistant = f"""```bash
comm -23 <(sort -u {q(left)}) <(sort -u {q(right)})
```
Process substitution keeps the original files unchanged."""
            topic = f"comm missing {app}"
        elif family == 7:
            target = f"/srv/{app}"
            backup = f"/var/backups/{app}"
            user = f"Create a timestamped gzip tar archive of {target} inside {backup}."
            assistant = f"""```bash
mkdir -p {q(backup)}
tar -C {q(target.rsplit('/', 1)[0])} -czf {q(backup)}/{app}-$(date -u +%Y%m%dT%H%M%SZ).tar.gz {q(target.rsplit('/', 1)[1])}
```
This writes one new archive and leaves the source tree untouched."""
            records.append(record("bash", topic, idx, user, assistant, difficulty="intermediate", risk_level="state_change_low", has_side_effects=True, side_effects=["creates_archive"], answer_style="guarded_procedure", tags=["bash", "tar", "backup"], dry_run_available=False, rollback_available=True))
            continue
        elif family == 8:
            cfg = f"/etc/{app}/app.env"
            key = f"{app.upper()}_PORT"
            user = f"Extract the {key} value from {cfg}, ignoring commented lines."
            assistant = f"""```bash
sed -nE 's/^[[:space:]]*{key}=([^#[:space:]]+).*/\\1/p' {q(cfg)} | tail -n 1
```
This reads the final uncommented assignment if the key appears more than once."""
            topic = f"extract env key {app}"
        else:
            path = f"/srv/{app}/queue"
            user = f"Count regular files in {path} without breaking on names that start with a dash."
            assistant = f"""```bash
find {q(path)} -type f -printf '.\\n' | wc -l
```
The count comes from `find`, not shell glob expansion."""
            topic = f"count queue files {app}"
        records.append(record("bash", topic, idx, user, assistant, tags=["bash", "scripting"]))
    return records


def terminal_records(start: int) -> list[dict[str, Any]]:
    tools = ["jq", "sqlite3", "nginx", "curl", "ss", "dig", "rg", "awk"]
    services = ["nginx", "cron", "ssh", "postgresql", "redis-server", "systemd-resolved", "docker", "fail2ban"]
    ports = [80, 443, 22, 5432, 6379, 53, 2375, 8080]
    records: list[dict[str, Any]] = []
    for offset in range(DOMAIN_SIZE):
        v = offset // 10
        family = offset % 10
        tool = tools[v]
        service = services[v]
        port = ports[v]
        idx = start + offset
        if family == 0:
            user = f"Check whether `{tool}` is installed, print its path, and show its version without installing anything."
            assistant = f"""```bash
command -v {tool} && {tool} --version
```
This only inspects the current PATH and tool output."""
            topic = f"check tool {tool}"
        elif family == 1:
            user = f"A command failed with `command not found: {tool}`. Give the shortest terminal check to confirm PATH and shell lookup state."
            assistant = f"""```bash
printf 'SHELL=%s\\nPATH=%s\\n' "$SHELL" "$PATH"
type -a {tool}
hash -r
type -a {tool}
```
`hash -r` clears Bash command lookup cache for the current shell."""
            topic = f"terminal command lookup {tool}"
        elif family == 2:
            user = f"Find which process is listening on TCP port {port} and include the PID/program column."
            assistant = f"""```bash
ss -ltnp 'sport = :{port}'
```
Elevated permissions may be needed if the process name is hidden."""
            topic = f"listener on port {port}"
        elif family == 3:
            user = f"Show the last 50 journal lines for {service} with ISO timestamps and no pager."
            assistant = f"""```bash
journalctl -u {service} -n 50 --no-pager --output=short-iso
```
This is read-only and preserves timestamps for triage."""
            topic = f"journal tail {service}"
        elif family == 4:
            user = f"Print the exit status of `{tool} --help` while keeping stdout and stderr visible."
            assistant = f"""```bash
{tool} --help
printf 'exit_status=%s\\n' "$?"
```
The status is printed after the command completes."""
            topic = f"show exit status {tool}"
        elif family == 5:
            user = f"Run `{tool} --help` in a pipeline and make Bash fail if any command in the pipeline fails."
            assistant = f"""```bash
set -o pipefail
{tool} --help 2>&1 | sed -n '1,12p'
printf 'pipeline_status=%s\\n' "$?"
```
`pipefail` prevents the final `sed` from hiding an earlier failure."""
            topic = f"pipefail help {tool}"
        elif family == 6:
            user = f"Inspect the current terminal dimensions and TERM value before running fullscreen `{tool}` output."
            assistant = """```bash
printf 'TERM=%s\n' "$TERM"
stty size
tput cols
tput lines
```
These checks do not modify the terminal."""
            topic = f"terminal dimensions {tool}"
        elif family == 7:
            user = f"Show open files for PID {2000 + v} without using interactive output."
            assistant = f"""```bash
ls -l /proc/{2000 + v}/fd
```
Elevated permissions may be needed if the process belongs to another user."""
            topic = f"proc fd {2000 + v}"
        elif family == 8:
            path = f"/srv/{service}/config with spaces.conf"
            user = f"Print a command that safely displays {path}; the path contains spaces."
            assistant = f"""```bash
sed -n '1,120p' {q(path)}
```
Shell quoting keeps the path as one argument."""
            topic = f"quote path {service}"
        else:
            user = f"Show CPU, memory, and elapsed time for running `{service}` processes."
            assistant = f"""```bash
ps -C {q(service)} -o pid,ppid,stat,%cpu,%mem,etime,cmd --sort=-%cpu
```
This is a snapshot suitable for terminal triage."""
            topic = f"ps snapshot {service}"
        records.append(record("terminal", topic, idx, user, assistant, tags=["terminal", "inspection"]))
    return records


def json_records(start: int) -> list[dict[str, Any]]:
    files = ["/tmp/deploy.json", "/srv/api/status.json", "/var/tmp/events.json", "/srv/billing/invoice.json", "/tmp/nodes.json", "/srv/search/index.json", "/var/log/app/structured.json", "/srv/auth/users.json"]
    keys = ["version", "status", "event", "total", "name", "shards", "request_id", "email"]
    records: list[dict[str, Any]] = []
    for offset in range(DOMAIN_SIZE):
        v = offset // 10
        family = offset % 10
        path = files[v]
        key = keys[v]
        idx = start + offset
        if family == 0:
            user = f"Using jq, print the top-level `{key}` field from {path}; return empty output if it is missing."
            assistant = f"""```bash
jq -r '.{key} // empty' {q(path)}
```
`// empty` avoids printing `null` for missing values."""
            topic = f"jq top level {key}"
        elif family == 1:
            user = f"From JSON array {path}, print each object's `.id` and `.{key}` as tab-separated values."
            assistant = f"""```bash
jq -r '.[] | [.id, .{key}] | @tsv' {q(path)}
```
The `@tsv` encoder keeps the output terminal-friendly."""
            topic = f"jq array tsv {key}"
        elif family == 2:
            user = f"Validate that {path} is valid JSON and print only `ok` or `invalid`."
            assistant = f"""```bash
if jq -e . {q(path)} >/dev/null; then printf 'ok\\n'; else printf 'invalid\\n'; fi
```
`jq -e` makes parse failure visible through the exit status."""
            topic = f"jq validate {path}"
        elif family == 3:
            user = f"Extract all objects from {path} where `.enabled` is true and output compact JSON lines."
            assistant = f"""```bash
jq -c '.[] | select(.enabled == true)' {q(path)}
```
Compact JSON lines are easier to pipe into later terminal tools."""
            topic = f"jq enabled objects {v}"
        elif family == 4:
            user = f"From {path}, count records grouped by `.{key}` and sort descending by count."
            assistant = f"""```bash
jq -r '.[].{key}' {q(path)} | sort | uniq -c | sort -nr
```
This uses jq for extraction and coreutils for the terminal summary."""
            topic = f"jq group counts {key}"
        elif family == 5:
            sample = f'{{"service":"svc-{v}","health":{{"status":"degraded","code":{500 + v}}}}}'
            user = f"Given this JSON on stdin: `{sample}`. Print `health.status` and `health.code` separated by one space."
            assistant = """```bash
jq -r '[.health.status, .health.code] | @tsv' | tr '\t' ' '
```
This reads stdin and emits a single terminal line."""
            topic = f"jq nested stdin {v}"
        elif family == 6:
            user = f"Convert newline-delimited JSON from {path} into a JSON array without losing objects."
            assistant = f"""```bash
jq -s '.' {q(path)}
```
Slurp mode reads every JSON line and wraps the stream in an array."""
            topic = f"jq slurp ndjson {v}"
        elif family == 7:
            user = f"Print only objects in {path} whose `.message` contains the literal text `timeout`, case-insensitive."
            assistant = f"""```bash
jq -c 'select((.message // "") | test("timeout"; "i"))' {q(path)}
```
The fallback handles records without a message field."""
            topic = f"jq message timeout {v}"
        elif family == 8:
            user = f"From {path}, output a shell-safe list of `.path` values for records where `.type == \"file\"`."
            assistant = f"""```bash
jq -r '.[] | select(.type == "file") | .path | @sh' {q(path)}
```
`@sh` quotes values for later review before reuse in a shell."""
            topic = f"jq shell quote paths {v}"
        else:
            user = f"Check whether every object in {path} has a non-empty `.{key}` field; exit nonzero if any fail."
            assistant = f"""```bash
jq -e 'all(.[]; (.{key} // "") != "")' {q(path)} >/dev/null
```
The command succeeds only when all records pass the predicate."""
            topic = f"jq require field {key}"
        records.append(record("json_parsing", topic, idx, user, assistant, tags=["json", "jq", "parsing"]))
    return records


def regex_records(start: int) -> list[dict[str, Any]]:
    files = ["/var/log/nginx/access.log", "/var/log/auth.log", "/srv/api/app.log", "/tmp/releases.txt", "/var/log/syslog", "/srv/billing/errors.log", "/tmp/users.txt", "/srv/search/query.log"]
    patterns = ["IPv4", "SSH users", "request ids", "semantic versions", "systemd units", "HTTP 5xx", "email domains", "latency values"]
    records: list[dict[str, Any]] = []
    for offset in range(DOMAIN_SIZE):
        v = offset // 10
        family = offset % 10
        path = files[v]
        idx = start + offset
        if family == 0:
            user = f"Extract unique IPv4 addresses from {path} using a regex-friendly terminal pipeline."
            assistant = f"""```bash
grep -Eo '([0-9]{{1,3}}\\.){{3}}[0-9]{{1,3}}' {q(path)} | sort -u
```
This extracts candidates; use stricter validation if octet range correctness matters."""
            topic = f"regex ipv4 {v}"
        elif family == 1:
            user = f"From {path}, print lines containing an HTTP status from 500 through 599."
            assistant = f"""```bash
grep -E '(^|[[:space:]])5[0-9]{{2}}([[:space:]]|$)' {q(path)}
```
The boundaries reduce accidental matches inside longer numbers."""
            topic = f"regex http 5xx {v}"
        elif family == 2:
            user = f"Extract values shaped like `req-` plus 12 hex characters from {path}."
            assistant = f"""```bash
grep -Eo 'req-[[:xdigit:]]{{12}}' {q(path)} | sort -u
```
This returns unique request identifiers only."""
            topic = f"regex request ids {v}"
        elif family == 3:
            user = f"Print semantic versions like v1.2.3 or 1.2.3 from {path}, one per line."
            assistant = f"""```bash
grep -Eo 'v?[0-9]+\\.[0-9]+\\.[0-9]+' {q(path)}
```
This intentionally targets plain three-part versions."""
            topic = f"regex semver {v}"
        elif family == 4:
            user = f"From journal text in {path}, extract systemd unit names ending in .service."
            assistant = f"""```bash
grep -Eo '[A-Za-z0-9_.@-]+\\.service' {q(path)} | sort -u
```
The character class covers common templated unit names."""
            topic = f"regex systemd unit {v}"
        elif family == 5:
            user = f"Show lines in {path} where `duration_ms=` is 1000 or higher."
            assistant = f"""```bash
grep -E 'duration_ms=([1-9][0-9]{{3,}})' {q(path)}
```
This catches millisecond durations with four or more digits."""
            topic = f"regex slow duration {v}"
        elif family == 6:
            user = f"Extract the domain part of email-like strings from {path} and count each domain."
            assistant = f"""```bash
grep -Eoi '[A-Z0-9._%+-]+@[A-Z0-9.-]+\\.[A-Z]{{2,}}' {q(path)} | awk -F@ '{{ print tolower($2) }}' | sort | uniq -c | sort -nr
```
The regex is for log extraction, not full email validation."""
            topic = f"regex email domains {v}"
        elif family == 7:
            user = f"Print only timestamps shaped like `2026-05-18T12:34:56Z` from {path}."
            assistant = f"""```bash
grep -Eo '[0-9]{{4}}-[0-9]{{2}}-[0-9]{{2}}T[0-9]{{2}}:[0-9]{{2}}:[0-9]{{2}}Z' {q(path)}
```
This extracts UTC ISO-like timestamps from plain text."""
            topic = f"regex utc timestamps {v}"
        elif family == 8:
            user = f"Replace repeated spaces with a single tab in {path}, printing to stdout only."
            assistant = f"""```bash
sed -E 's/[[:space:]]{{2,}}/\\t/g' {q(path)}
```
This does not edit the source file."""
            topic = f"regex sed spaces {v}"
        else:
            user = f"From {path}, print lines that do not match the expected `{patterns[v]}` pattern."
            assistant = f"""```bash
grep -Ev '([0-9]{{1,3}}\\.){{3}}[0-9]{{1,3}}|5[0-9]{{2}}|req-[[:xdigit:]]{{12}}|v?[0-9]+\\.[0-9]+\\.[0-9]+' {q(path)}
```
This is a quick negative filter for mixed operational logs."""
            topic = f"regex negative filter {v}"
        records.append(record("regex", topic, idx, user, assistant, tags=["regex", "grep", "sed", "awk"]))
    return records


def sqlite_records(start: int) -> list[dict[str, Any]]:
    dbs = ["/srv/api/app.db", "/srv/billing/billing.db", "/var/lib/queue/jobs.db", "/srv/auth/auth.db", "/tmp/events.db", "/srv/search/search.db", "/srv/reports/reports.db", "/var/lib/metrics/metrics.db"]
    tables = ["requests", "invoices", "jobs", "users", "events", "documents", "reports", "samples"]
    columns = ["status", "state", "queue", "role", "severity", "type", "owner", "host"]
    records: list[dict[str, Any]] = []
    for offset in range(DOMAIN_SIZE):
        v = offset // 10
        family = offset % 10
        db = dbs[v]
        table = tables[v]
        col = columns[v]
        idx = start + offset
        if family == 0:
            user = f"Use sqlite3 read-only mode to count rows in table `{table}` inside {db}."
            assistant = f"""```bash
sqlite3 -readonly {q(db)} 'SELECT COUNT(*) FROM {table};'
```
`-readonly` prevents accidental writes."""
            topic = f"sqlite count {table}"
        elif family == 1:
            user = f"Show counts grouped by `{col}` for `{table}` in {db}, highest count first."
            assistant = f"""```bash
sqlite3 -readonly -header -column {q(db)} <<'SQL'
SELECT {col}, COUNT(*) AS count
FROM {table}
GROUP BY {col}
ORDER BY count DESC;
SQL
```
The query is read-only and formatted for terminal review."""
            topic = f"sqlite group {table} {col}"
        elif family == 2:
            user = f"List the schema for table `{table}` in {db} without opening sqlite interactively."
            assistant = f"""```bash
sqlite3 -readonly {q(db)} '.schema {table}'
```
This prints the table DDL directly."""
            topic = f"sqlite schema {table}"
        elif family == 3:
            user = f"Find the 20 most recent rows from `{table}` in {db} using `created_at` descending."
            assistant = f"""```bash
sqlite3 -readonly -header -column {q(db)} <<'SQL'
SELECT *
FROM {table}
ORDER BY created_at DESC
LIMIT 20;
SQL
```
Use this for inspection before changing application state."""
            topic = f"sqlite recent {table}"
        elif family == 4:
            user = f"Check database integrity for {db} and print the result."
            assistant = f"""```bash
sqlite3 -readonly {q(db)} 'PRAGMA integrity_check;'
```
The pragma reads the database and reports `ok` when consistent."""
            topic = f"sqlite integrity {v}"
        elif family == 5:
            user = f"Export `{table}` from {db} as CSV to stdout with a header."
            assistant = f"""```bash
sqlite3 -readonly -csv -header {q(db)} 'SELECT * FROM {table};'
```
Redirect stdout yourself if you want to save the export."""
            topic = f"sqlite csv {table}"
        elif family == 6:
            user = f"Find duplicate `id` values in `{table}` from {db}."
            assistant = f"""```bash
sqlite3 -readonly -header -column {q(db)} <<'SQL'
SELECT id, COUNT(*) AS count
FROM {table}
GROUP BY id
HAVING COUNT(*) > 1
ORDER BY count DESC, id;
SQL
```
This reports only duplicated identifiers."""
            topic = f"sqlite duplicate ids {table}"
        elif family == 7:
            user = f"Print the SQLite version and list all tables in {db}."
            assistant = f"""```bash
sqlite3 -readonly {q(db)} 'SELECT sqlite_version();'
sqlite3 -readonly {q(db)} '.tables'
```
Both commands are read-only inspection."""
            topic = f"sqlite version tables {v}"
        elif family == 8:
            user = f"Show indexes defined on `{table}` in {db}."
            assistant = f"""```bash
sqlite3 -readonly -header -column {q(db)} <<'SQL'
PRAGMA index_list('{table}');
SQL
```
Index metadata helps explain slow queries without modifying the database."""
            topic = f"sqlite indexes {table}"
        else:
            user = f"Run a parameter-safe lookup for one `{col}` value in `{table}` from {db}; use a sqlite parameter named `$value`."
            assistant = f"""```bash
sqlite3 -readonly -cmd '.parameter set $value active' -header -column {q(db)} <<'SQL'
SELECT *
FROM {table}
WHERE {col} = $value
LIMIT 50;
SQL
```
SQLite parameters avoid string-splicing values into the query."""
            topic = f"sqlite parameter lookup {table}"
        records.append(record("sqlite", topic, idx, user, assistant, tags=["sqlite", "database", "readonly"]))
    return records


def nginx_records(start: int) -> list[dict[str, Any]]:
    sites = ["api.example.test", "app.example.test", "static.example.test", "admin.example.test", "webhook.example.test", "files.example.test", "status.example.test", "docs.example.test"]
    logs = ["/var/log/nginx/api.access.log", "/var/log/nginx/app.access.log", "/var/log/nginx/static.access.log", "/var/log/nginx/admin.access.log", "/var/log/nginx/webhook.access.log", "/var/log/nginx/files.access.log", "/var/log/nginx/status.access.log", "/var/log/nginx/docs.access.log"]
    records: list[dict[str, Any]] = []
    for offset in range(DOMAIN_SIZE):
        v = offset // 10
        family = offset % 10
        site = sites[v]
        log = logs[v]
        idx = start + offset
        if family == 0:
            user = f"Validate nginx configuration syntax and show included file names before any reload for {site}."
            assistant = """```bash
sudo nginx -T >/tmp/nginx.full.conf
sudo nginx -t
grep -E '^# configuration file ' /tmp/nginx.full.conf
```
Validate first; do not reload until the syntax check passes."""
            topic = f"nginx validate {site}"
            records.append(record("nginx", topic, idx, user, assistant, requires_root=True, answer_style="diagnostic_steps", tags=["nginx", "config", "validation"]))
            continue
        elif family == 1:
            user = f"Find which nginx server block mentions `server_name {site}`."
            assistant = f"""```bash
sudo nginx -T 2>/dev/null | grep -nE 'server_name[[:space:]].*\\b{re.escape(site)}\\b'
```
`nginx -T` shows the effective merged configuration."""
            topic = f"nginx server name {site}"
            requires_root = True
        elif family == 2:
            user = f"Show the top 20 client IPs in {log}."
            assistant = f"""```bash
awk '{{ print $1 }}' {q(log)} | sort | uniq -c | sort -nr | head -20
```
This assumes the default access log starts with the client address."""
            topic = f"nginx top ips {site}"
            requires_root = False
        elif family == 3:
            user = f"Count nginx 5xx responses in {log} by status code."
            assistant = f"""```bash
awk '$9 ~ /^5[0-9][0-9]$/ {{ count[$9]++ }} END {{ for (code in count) print code, count[code] }}' {q(log)} | sort
```
Default combined logs store the status code in field 9."""
            topic = f"nginx count 5xx {site}"
            requires_root = False
        elif family == 4:
            user = f"Print nginx virtual hosts that listen on port 443 for {site}."
            assistant = """```bash
sudo nginx -T 2>/dev/null | awk '
  /server_name/ { name=$0 }
  /listen[[:space:]]+443/ { print name " :: " $0 }
'
```
This inspects generated config output only."""
            topic = f"nginx listen 443 {site}"
            requires_root = True
        elif family == 5:
            user = f"After validating config, reload nginx for {site} with systemd."
            assistant = """```bash
sudo nginx -t && sudo systemctl reload nginx
```
The reload runs only after the syntax check succeeds."""
            records.append(record("nginx", f"nginx guarded reload {site}", idx, user, assistant, requires_root=True, risk_level="state_change_low", has_side_effects=True, side_effects=["service_reload"], answer_style="guarded_procedure", tags=["nginx", "reload", "systemd"], rollback_available=True))
            continue
        elif family == 6:
            user = f"Show the last 80 nginx error-log lines related to {site} without using a pager."
            assistant = f"""```bash
sudo journalctl -u nginx -n 80 --no-pager --output=short-iso
sudo tail -n 80 /var/log/nginx/error.log
```
Both commands are read-only log inspection."""
            topic = f"nginx error tail {site}"
            requires_root = True
        elif family == 7:
            user = f"Generate an nginx location snippet that proxies `/api/` for {site} to http://127.0.0.1:{8000 + v}."
            assistant = f"""```nginx
location /api/ {{
    proxy_pass http://127.0.0.1:{8000 + v}/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}}
```
Validate the full nginx config before reloading."""
            topic = f"nginx proxy snippet {site}"
            requires_root = False
        elif family == 8:
            user = f"Find slow nginx requests in {log} where the final request time field is at least 2 seconds."
            assistant = f"""```bash
awk '$(NF) + 0 >= 2 {{ print }}' {q(log)}
```
Use this only if the log format ends with request time."""
            topic = f"nginx slow requests {site}"
            requires_root = False
        else:
            user = f"List enabled nginx site symlinks and their targets for {site} triage."
            assistant = """```bash
find /etc/nginx/sites-enabled -maxdepth 1 -type l -printf '%f -> %l\n' | sort
```
This shows which site files are currently enabled."""
            topic = f"nginx enabled sites {site}"
            requires_root = False
        records.append(record("nginx", topic, idx, user, assistant, requires_root=requires_root, answer_style="diagnostic_steps", tags=["nginx", "webserver"]))
    return records


def triage_records(start: int) -> list[dict[str, Any]]:
    services = ["nginx", "api.service", "worker.service", "ssh", "cron", "redis-server", "systemd-resolved", "docker"]
    symptoms = ["high CPU", "OOM kill", "disk full", "connection refused", "slow boot", "permission denied", "DNS failure", "crash loop"]
    records: list[dict[str, Any]] = []
    for offset in range(DOMAIN_SIZE):
        v = offset // 10
        family = offset % 10
        service = services[v]
        symptom = symptoms[v]
        idx = start + offset
        if family == 0:
            user = f"Triage {symptom} for {service}; collect process, journal, and resource snapshots without changing state."
            assistant = f"""```bash
systemctl status {service} --no-pager
journalctl -u {service} -n 120 --no-pager --output=short-iso
ps -eo pid,ppid,stat,%cpu,%mem,etime,cmd --sort=-%cpu | head -20
free -h
df -hT
```
This gathers evidence before any restart or config change."""
            topic = f"triage snapshot {service}"
        elif family == 1:
            user = f"Given `{service}` reports `Main process exited, status=1/FAILURE`, show the terminal commands to inspect why."
            assistant = f"""```bash
systemctl status {service} --no-pager
journalctl -u {service} -b --no-pager --output=short-iso | tail -n 160
systemctl cat {service}
```
The unit file and current-boot logs usually show the failing command."""
            topic = f"triage failed unit {service}"
        elif family == 2:
            user = f"Investigate whether {service} was killed by the kernel OOM killer."
            assistant = f"""```bash
journalctl -k --no-pager --output=short-iso | grep -Ei 'out of memory|oom|killed process'
journalctl -u {service} -n 80 --no-pager --output=short-iso
```
Kernel OOM lines are the primary evidence."""
            topic = f"triage oom {service}"
        elif family == 3:
            user = f"Check whether disk pressure could explain {symptom} on this Debian/Ubuntu host."
            assistant = """```bash
df -hT
df -ih
du -xhd1 /var 2>/dev/null | sort -h
journalctl -p warning..alert -n 80 --no-pager
```
This checks both byte usage and inode exhaustion."""
            topic = f"triage disk pressure {service}"
        elif family == 4:
            user = f"Confirm whether {service} is repeatedly restarting and show restart-related logs."
            assistant = f"""```bash
systemctl show {service} -p NRestarts -p RestartUSec -p ActiveState -p SubState
journalctl -u {service} --since '30 min ago' --no-pager --output=short-iso
```
The systemd properties give the restart counter and current state."""
            topic = f"triage restart loop {service}"
        elif family == 5:
            user = f"Investigate a `permission denied` error for {service} reading `/srv/{service}/config.yml`."
            assistant = f"""```bash
namei -l /srv/{service}/config.yml
stat /srv/{service}/config.yml
systemctl show {service} -p User -p Group
```
Check path traversal permissions before changing file modes."""
            topic = f"triage permissions {service}"
        elif family == 6:
            user = f"Check whether {service} has open network sockets and recent connection errors."
            assistant = f"""```bash
ss -ltnp
journalctl -u {service} --since '15 min ago' --no-pager --output=short-iso | grep -Ei 'connect|refused|timeout|listen|address'
```
Socket state plus recent logs narrows network failures quickly."""
            topic = f"triage sockets {service}"
        elif family == 7:
            user = f"Look for recent package or config changes that could correlate with {service} failing today."
            assistant = f"""```bash
grep -hE ' install | upgrade | remove ' /var/log/apt/history.log /var/log/apt/history.log.* 2>/dev/null | tail -80
find /etc -xdev -type f -mtime -1 -printf '%TY-%Tm-%Td %TH:%TM %p\\n' 2>/dev/null | sort
```
This correlates recent system changes with the failure window."""
            topic = f"triage recent changes {service}"
        elif family == 8:
            user = f"Produce a compact triage bundle for {service} under /tmp without restarting anything."
            assistant = f"""```bash
out=/tmp/{service.replace('.', '-')}-triage-$(date -u +%Y%m%dT%H%M%SZ).txt
set -euo pipefail
{{
  systemctl status {service} --no-pager
  journalctl -u {service} -n 200 --no-pager --output=short-iso
  ss -ltnp
  df -hT
  free -h
}} >"$out"
printf '%s\\n' "$out"
```
This writes one local evidence file in `/tmp`."""
            records.append(record("triage", f"triage bundle {service}", idx, user, assistant, risk_level="state_change_low", has_side_effects=True, side_effects=["creates_report"], answer_style="script_with_explanation", tags=["triage", "evidence", "systemd"], rollback_available=True))
            continue
        else:
            user = f"Given a user says `{service} is down`, return the first terminal checks only; no restart."
            assistant = f"""```bash
systemctl is-active {service}; printf 'systemctl_status=%s\\n' "$?"
systemctl status {service} --no-pager
journalctl -u {service} -n 60 --no-pager --output=short-iso
```
These checks establish state before taking action."""
            topic = f"triage no restart {service}"
        records.append(record("triage", topic, idx, user, assistant, answer_style="diagnostic_steps", tags=["triage", "systemd", "logs"]))
    return records


def networking_records(start: int) -> list[dict[str, Any]]:
    hosts = ["example.org", "api.example.test", "db.internal", "repo.local", "dns.google", "gateway.local", "files.example.test", "status.example.test"]
    ports = [443, 8443, 5432, 80, 53, 22, 2049, 8080]
    records: list[dict[str, Any]] = []
    for offset in range(DOMAIN_SIZE):
        v = offset // 10
        family = offset % 10
        host = hosts[v]
        port = ports[v]
        idx = start + offset
        if family == 0:
            user = f"Show IP addresses, routes, and DNS resolver state before testing {host}."
            assistant = f"""```bash
ip -brief address
ip route show
resolvectl status 2>/dev/null || cat /etc/resolv.conf
ip route get {q(host)}
```
This is read-only host network inspection."""
            topic = f"network state {v}"
        elif family == 1:
            user = f"Test TCP connectivity to {host}:{port} without sending application data."
            assistant = f"""```bash
timeout 5 bash -c '</dev/tcp/{host}/{port}' && printf 'open\\n' || printf 'closed_or_filtered\\n'
```
The timeout avoids a hanging terminal session."""
            topic = f"tcp check {host} {port}"
        elif family == 2:
            user = f"Resolve {host} with systemd-resolved if available, otherwise fall back to getent."
            assistant = f"""```bash
resolvectl query {q(host)} 2>/dev/null || getent ahosts {q(host)}
```
This checks local resolver behavior rather than a hard-coded public resolver."""
            topic = f"dns resolve {host}"
        elif family == 3:
            user = f"Show the route Linux would use to reach {host}."
            assistant = f"""```bash
ip route get {q(host)}
```
The output includes selected source address and interface."""
            topic = f"route get {host}"
        elif family == 4:
            user = f"Fetch only HTTP response headers from https://{host}/ with a 10 second timeout."
            assistant = f"""```bash
curl -fsSIL --max-time 10 https://{host}/
```
Headers are enough for status, redirects, and TLS reachability."""
            topic = f"curl headers {host}"
        elif family == 5:
            user = f"Show listening TCP and UDP sockets with process names while investigating {host}:{port}."
            assistant = f"""```bash
ss -lntup
```
Elevated permissions may be needed if process names are hidden; compare listeners with expected port {port}."""
            topic = f"ss listen {v}"
        elif family == 6:
            user = f"Check packet loss to {host} with a bounded ping command."
            assistant = f"""```bash
ping -c 5 -W 2 {q(host)}
```
The count and deadline keep the command bounded."""
            topic = f"ping bounded {host}"
        elif family == 7:
            user = f"Display firewall rules without changing them while checking access to {host}:{port}."
            assistant = f"""```bash
sudo nft list ruleset 2>/dev/null || sudo iptables -S
```
This inspects active packet-filter rules only; review whether port {port} is allowed."""
            topic = f"firewall readonly {v}"
            records.append(record("networking", topic, idx, user, assistant, requires_root=True, answer_style="diagnostic_steps", tags=["networking", "firewall", "readonly"]))
            continue
        elif family == 8:
            user = f"Show network errors and drops per interface before debugging {host}."
            assistant = f"""```bash
ip -s link
```
Look at RX/TX error and dropped counters before focusing on {host}."""
            topic = f"interface errors {v}"
        else:
            user = f"Run a traceroute-like path check to {host}, using tracepath when available."
            assistant = f"""```bash
command -v tracepath >/dev/null && tracepath {q(host)} || ping -c 4 {q(host)}
```
The fallback still gives basic reachability when tracepath is absent."""
            topic = f"tracepath fallback {host}"
        records.append(record("networking", topic, idx, user, assistant, answer_style="diagnostic_steps", tags=["networking", "diagnostics"]))
    return records


def build_records() -> list[dict[str, Any]]:
    builders = [
        bash_records,
        terminal_records,
        json_records,
        regex_records,
        sqlite_records,
        nginx_records,
        triage_records,
        networking_records,
    ]
    records: list[dict[str, Any]] = []
    start = 1
    for builder in builders:
        chunk = builder(start)
        records.extend(chunk)
        start += len(chunk)
    return records


def validate_generated(records: list[dict[str, Any]], existing_pairs: set[str]) -> None:
    ids = [item["id"] for item in records]
    if len(ids) != len(set(ids)):
        raise SystemExit("generated duplicate ids")

    pairs = []
    for item in records:
        user = next(message["content"] for message in item["messages"] if message["role"] == "user")
        assistant = next(message["content"] for message in item["messages"] if message["role"] == "assistant")
        pairs.append(f"{normalize(user)}\n---\n{normalize(assistant)}")
    if len(pairs) != len(set(pairs)):
        raise SystemExit("generated duplicate user/assistant pairs")
    overlap = sorted(set(pairs) & existing_pairs)
    if overlap:
        raise SystemExit(f"generated records overlap existing SFT pairs: {len(overlap)}")

    counts = collections.Counter(item["meta"]["subdomain"] for item in records)
    expected = {domain: DOMAIN_SIZE for domain in DOMAINS}
    if dict(counts) != expected:
        raise SystemExit(f"unexpected domain counts: {dict(counts)}")


def write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for item in records:
            handle.write(json.dumps(item, ensure_ascii=False, separators=(",", ":")) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--existing", type=Path, action="append", default=[EXISTING_SFT])
    args = parser.parse_args()

    records = build_records()
    validate_generated(records, load_existing_pairs(args.existing))
    write_jsonl(args.output, records)
    counts = collections.Counter(item["meta"]["subdomain"] for item in records)
    print(f"wrote {len(records)} records to {args.output}")
    for domain in DOMAINS:
        print(f"{domain}: {counts[domain]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Build the v1.2 operational-gap SFT wave for debian-admin-bash.

The wave is deliberately narrow, high-signal, and draft-only. It deepens local
Debian/Ubuntu admin surfaces for a small 3B/4B model without adding
cloud/Kubernetes/Postgres scope or claiming semantic/safety review.
"""
from __future__ import annotations

import hashlib
import json
import textwrap
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / "datasets/debian-admin-bash/debian-admin-bash-sft.jsonl"
VERSION = "1.2"
WAVE = "v1.2-operational-gaps"
SYSTEM = (
    "You are a Debian/Ubuntu terminal administration assistant. Return correct Bash commands and brief factual explanations. "
    "Prefer inspection before modification, validate configuration before restarts, use sudo only when needed, warn before risky operations, "
    "and check tool availability when a command may be missing. Keep answers concise."
)

VARIANTS = [
    {"n": 1, "host": "ops-a", "svc": "app-api", "user": "appsvc", "port": "8080", "db": "/var/lib/app/app.db", "cfg": "/etc/app/config.json", "unit": "app-api.service", "vm": "bookworm-lab"},
    {"n": 2, "host": "ops-b", "svc": "worker", "user": "worker", "port": "9090", "db": "/srv/worker/state.db", "cfg": "/etc/worker/settings.json", "unit": "worker.service", "vm": "ubuntu-ci"},
    {"n": 3, "host": "ops-c", "svc": "billing", "user": "billing", "port": "8443", "db": "/var/lib/billing/billing.db", "cfg": "/etc/billing/config.json", "unit": "billing.service", "vm": "debian-test"},
    {"n": 4, "host": "ops-d", "svc": "portal", "user": "portal", "port": "3000", "db": "/srv/portal/portal.db", "cfg": "/etc/portal/app.json", "unit": "portal.service", "vm": "ubuntu-desktop"},
]


def expand(text: str, values: dict[str, Any]) -> str:
    out = textwrap.dedent(text).strip()
    for key, value in values.items():
        out = out.replace("{" + key + "}", str(value))
    return out


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    path.write_text("\n".join(json.dumps(r, ensure_ascii=False, separators=(",", ":")) for r in records) + "\n", encoding="utf-8")


def safety_for(risk: str, warning: bool = False, dry_run: bool = False, rollback: bool = False, destructive: bool = False) -> dict[str, Any]:
    has_side_effects = risk in {"state_change_low", "state_change_high", "network_sensitive", "privilege_sensitive", "security_sensitive", "destructive"}
    warn = warning or risk in {"state_change_high", "network_sensitive", "privilege_sensitive", "security_sensitive", "destructive"}
    return {
        "has_side_effects": has_side_effects,
        "side_effects": [] if not has_side_effects else ["local_state_change"],
        "destructive": destructive or risk == "destructive",
        "warning_required": warn,
        "warning_present": warn,
        "dry_run_available": dry_run,
        "rollback_available": rollback,
    }


def make_record(idx: int, case: dict[str, Any], v: dict[str, Any]) -> dict[str, Any]:
    sub = case["subdomain"]
    risk = case.get("risk", "safe_readonly")
    tags = sorted(set(["linux", "debian", "ubuntu", sub.replace("_", "-")] + case.get("tags", [])))
    return {
        "id": f"debian-admin-bash:v12.{sub}.{case['slug']}.{v['n']:02d}.{idx:04d}",
        "meta": {
            "dataset_version": VERSION,
            "task_type": "sft",
            "language": "en",
            "domain": "debian_admin_bash",
            "subdomain": sub,
            "target_os": {"family": "linux", "distros": ["debian", "ubuntu"], "shell": "bash", "package_manager": case.get("package_manager", "none")},
            "target_model_profile": "small-debian-admin",
            "difficulty": case.get("difficulty", "intermediate"),
            "risk_level": risk,
            "requires_root": case.get("requires_root", False),
            "answer_style": case.get("style", "diagnostic_steps"),
            "tags": tags,
            "safety": safety_for(risk, case.get("warning", False), case.get("dry_run", False), case.get("rollback", False), case.get("destructive", False)),
            "review": {
                "status": "draft",
                "semantic_review": False,
                "safety_review": False,
                "execution_validation": {"mode": "static_only", "status": "pending", "reason": "v1.2 operational-gap draft; not manually reviewed or executed."},
            },
            "source": {"source_dataset_version": VERSION, "curation": "operational_gap_wave", "wave": WAVE, "generator": "scripts/build_v12_operational_gaps.py"},
        },
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": expand(case["prompt"], v)},
            {"role": "assistant", "content": expand(case["answer"], v)},
        ],
    }


CASES: list[dict[str, Any]] = []

def add(subdomain: str, slug: str, prompt: str, answer: str, **meta: Any) -> None:
    case = {"subdomain": subdomain, "slug": slug, "prompt": prompt, "answer": answer}
    case.update(meta)
    CASES.append(case)


# SQLite operational depth.
add("sqlite", "locked-wal-writer", """
Host {host}: {unit} logs show `sqlite3.OperationalError: database is locked` for `{db}` and the DB has a `-wal` file. Give the safest first verification command; do not kill a process first.
""", """
```bash
sudo lsof -- {db} {db}-wal 2>/dev/null || sudo fuser -v {db} {db}-wal
```
Identify the writer or long-lived reader holding the SQLite files first. Do not kill it or delete WAL/SHM files until you know which service owns the lock.
""", tags=["sqlite", "wal", "lock", "lsof", "inspection"], requires_root=True)

add("sqlite", "schema-index-plan", """
Host {host}: a SQLite query on `{db}` became slow. Show commands to inspect tables, indexes, and the query plan without changing data.
""", """
```bash
sqlite3 {db} '.tables'
sqlite3 {db} '.indexes'
sqlite3 {db} "EXPLAIN QUERY PLAN SELECT * FROM events WHERE service = '{svc}' ORDER BY created_at DESC LIMIT 20;"
```
Use the plan to confirm whether the query scans the table or uses an index before proposing schema changes.
""", tags=["sqlite", "schema", "indexes", "explain-query-plan"])

add("sqlite", "vacuum-into-compact", """
Host {host}: `{db}` is large after deletes. Give a guarded compacting procedure that does not overwrite the live DB in place.
""", """
```bash
sudo install -d -m 0750 /var/backups/{svc}
sudo sqlite3 {db} 'PRAGMA integrity_check;'
sudo sqlite3 {db} "VACUUM INTO '/var/backups/{svc}/app.compacted.db';"
sudo sqlite3 /var/backups/{svc}/app.compacted.db 'PRAGMA integrity_check;'
```
This writes a separate compacted copy. Review ownership, free space, and service stop/swap policy before replacing the live database.
""", tags=["sqlite", "vacuum-into", "backup"], risk="state_change_low", style="guarded_procedure", rollback=True, requires_root=True)

add("sqlite", "not-null-migration", """
Host {host}: add a NOT NULL `tenant_id` column to a populated SQLite table in `{db}`. Give the safe migration shape, not a one-line ALTER that breaks existing rows.
""", """
Warning: back up and rehearse this on a copy before touching the live DB.
```bash
sudo install -d -m 0750 /var/backups/{svc}
sudo sqlite3 {db} ".backup '/var/backups/{svc}/pre-tenant-migration.db'"
sudo sqlite3 {db} <<'SQL'
.bail on
BEGIN IMMEDIATE;
CREATE TABLE events_new(id INTEGER PRIMARY KEY, tenant_id TEXT NOT NULL DEFAULT 'default', message TEXT);
INSERT INTO events_new(id, tenant_id, message) SELECT id, 'default', message FROM events;
ALTER TABLE events RENAME TO events_old;
ALTER TABLE events_new RENAME TO events;
PRAGMA integrity_check;
COMMIT;
SQL
```
Review the real schema, indexes, and triggers first; this is the guarded pattern, not a paste blindly command.
""", tags=["sqlite", "migration", "schema", "backup"], risk="state_change_high", style="guarded_procedure", rollback=True, warning=True, requires_root=True)

add("sqlite", "online-backup", """
Host {host}: back up active SQLite DB `{db}` for {unit}. Give the safe SQLite-native command, not a blind file copy.
""", """
```bash
sudo install -d -m 0750 /var/backups/{svc}
backup=/var/backups/{svc}/app-$(date -u +%Y%m%dT%H%M%SZ).db
sudo sqlite3 {db} ".backup '$backup'"
sudo sqlite3 "$backup" 'PRAGMA integrity_check;'
```
The `.backup` command uses SQLite backup semantics and is safer than copying a live DB file directly.
""", tags=["sqlite", "online-backup", "backup"], risk="state_change_low", style="guarded_procedure", rollback=True, requires_root=True)

# JSON/JQ/YAML/TOML/INI data plumbing.
add("json_jq", "jq-empty-validate", """
Validate `{cfg}` as JSON on a Debian/Ubuntu host and print only success or the parser error.
""", """
```bash
jq empty {cfg} && echo 'valid JSON'
```
`jq empty` parses the full document without changing it; a non-zero exit shows the syntax error.
""", tags=["jq", "json", "validation"])

add("json_jq", "jsonl-line-validation", """
Validate `/var/log/{svc}/events.jsonl` line by line and show the first bad line number without loading the whole file into memory.
""", """
```bash
awk 'NF {print NR "\t" $0}' /var/log/{svc}/events.jsonl | while IFS=$'\t' read -r nr json; do
  printf '%s' "$json" | jq -e . >/dev/null || { echo "bad JSONL line $nr"; break; }
done
```
JSONL must parse per line; do not treat the whole file as one JSON array.
""", tags=["jsonl", "jq", "validation"])

add("json_jq", "atomic-json-patch", """
Patch `{cfg}` to set `.logging.level` to `info` atomically and keep a backup.
""", """
```bash
sudo cp -a {cfg} {cfg}.bak.$(date -u +%Y%m%dT%H%M%SZ)
tmp=$(mktemp)
sudo jq '.logging.level = "info"' {cfg} > "$tmp"
sudo install -m 0644 -o root -g root "$tmp" {cfg}
rm -f "$tmp"
```
Validate the service config before reload/restart; this only patches the JSON file.
""", tags=["jq", "json", "atomic-update", "config"], risk="state_change_low", style="guarded_procedure", rollback=True, requires_root=True)

add("json_jq", "yaml-yq-fallback", """
Read `.services.{svc}.image` from `/etc/{svc}/compose.yaml`, using `yq` if present and Python as fallback.
""", """
```bash
if command -v yq >/dev/null 2>&1; then
  yq -r '.services.{svc}.image' /etc/{svc}/compose.yaml
else
  python3 - <<'PY'
import yaml
with open('/etc/{svc}/compose.yaml', encoding='utf-8') as f:
    print(yaml.safe_load(f)['services']['{svc}']['image'])
PY
fi
```
Check `python3-yaml` availability before relying on the fallback on minimal hosts.
""", tags=["yaml", "yq", "fallback", "python"])

add("structured_output", "operator-json-contract", """
Given an incident in {unit}, return a minimal JSON handoff schema for `status`, `findings`, and `next_command` only.
""", """
```json
{
  "status": "needs_verification",
  "findings": ["{unit} has not been diagnosed yet"],
  "next_command": "systemctl status {unit} --no-pager"
}
```
Keep the contract stable and put the next safe command in one string field for downstream tooling.
""", tags=["json", "structured-output", "contract"])

# systemd deep operations.
add("systemd", "exec-203-verify", """
`{unit}` fails with `status=203/EXEC`. Give the safest verification commands before editing the unit.
""", """
```bash
systemctl status {unit} --no-pager
sudo systemd-analyze verify /etc/systemd/system/{unit}
systemctl cat {unit}
```
203/EXEC usually means the configured executable cannot be run. Verify the unit and inspect `ExecStart` before changing files.
""", tags=["systemd", "203-exec", "verify"], requires_root=True)

add("systemd", "user-217", """
`{unit}` fails with `status=217/USER`. What do you check first?
""", """
```bash
systemctl status {unit} --no-pager
systemctl cat {unit}
id {user}
```
Confirm that the `User=` account resolves and has the expected UID/groups before editing the unit.
""", tags=["systemd", "217-user", "service-user"], requires_root=True)

add("systemd", "namespace-226", """
`{unit}` fails with `status=226/NAMESPACE` after hardening. Give inspection commands that keep the host unchanged.
""", """
```bash
systemctl status {unit} --no-pager
systemctl cat {unit}
journalctl -u {unit} -b --no-pager | tail -80
```
Look for `ProtectSystem=`, `ReadWritePaths=`, `PrivateTmp=`, or missing paths before relaxing sandboxing.
""", tags=["systemd", "226-namespace", "sandboxing"], requires_root=True)

add("systemd", "timer-persistent-missed", """
A daily backup timer missed runs while the host was off. Show commands to inspect whether `Persistent=true` is configured.
""", """
```bash
systemctl list-timers --all '*backup*'
systemctl cat {svc}.timer
journalctl -u {svc}.timer -u {svc}.service --since '3 days ago' --no-pager
```
`Persistent=true` belongs in the timer unit and allows catch-up after downtime.
""", tags=["systemd", "timer", "persistent"])

add("systemd", "startlimit-loop", """
`{unit}` is in a restart loop and now says start request repeated too quickly. Give safe diagnostic commands before resetting failure state.
""", """
```bash
systemctl status {unit} --no-pager
systemctl show {unit} -p NRestarts -p Restart -p RestartSec -p StartLimitBurst -p StartLimitIntervalUSec
journalctl -u {unit} -b --no-pager | tail -120
```
Find the failing cause before `reset-failed`; otherwise the service may immediately loop again.
""", tags=["systemd", "startlimit", "restart-loop"], requires_root=True)

# Permissions / SSH / sudoers / AppArmor.
add("permissions", "path-chain-read", """
Host {host}: `{unit}` as `{user}` cannot read `/srv/{svc}/config.yml`. Give the first commands to inspect the permission chain.
""", """
```bash
systemctl show {unit} -p User -p Group
namei -l /srv/{svc}/config.yml
stat -c '%a %U:%G %n' /srv /srv/{svc} /srv/{svc}/config.yml
```
Do not start with recursive chmod/chown. Find the first path component the service user cannot traverse or read.
""", tags=["permissions", "namei", "stat", "service-user"], requires_root=True)

add("ssh_auth", "authorized-keys-modes", """
SSH public key login for `{user}` fails. Give commands to inspect ownership and mode of the home `.ssh` chain.
""", """
```bash
id {user}
namei -l /home/{user}/.ssh/authorized_keys
stat -c '%a %U:%G %n' /home/{user} /home/{user}/.ssh /home/{user}/.ssh/authorized_keys
```
OpenSSH rejects overly broad permissions; inspect before changing modes.
""", tags=["ssh", "authorized-keys", "permissions"], requires_root=True)

add("security", "sudoers-validate-dropin", """
Add a sudoers drop-in for a limited `{svc}` maintenance command. Show the validation-first workflow.
""", """
Warning: a bad sudoers file can lock out privilege escalation.
```bash
printf '%s\n' '{user} ALL=(root) NOPASSWD: /usr/bin/systemctl reload {unit}' | sudo tee /etc/sudoers.d/{svc} >/dev/null
sudo chmod 0440 /etc/sudoers.d/{svc}
sudo visudo -cf /etc/sudoers.d/{svc}
sudo visudo -c
```
Keep the command path narrow and validate both the drop-in and full sudoers set before relying on it.
""", tags=["sudoers", "visudo", "security"], risk="security_sensitive", style="guarded_procedure", rollback=True, requires_root=True)

add("security", "apparmor-denial-verify", """
`{unit}` cannot read `/srv/{svc}/uploads/file.txt` and someone suggests disabling AppArmor. Give the safer verification commands.
""", """
```bash
sudo journalctl -k --since '30 minutes ago' --no-pager | grep -i apparmor
sudo aa-status
namei -l /srv/{svc}/uploads/file.txt
```
Confirm the denial, profile, and path permissions first. Do not disable AppArmor globally as a first fix.
""", tags=["apparmor", "journalctl", "security"], requires_root=True)

add("permissions", "minimal-acl-grant", """
Grant `{user}` read-only access to `/srv/{svc}/reports` without changing ownership recursively. Include verification and rollback.
""", """
```bash
sudo getfacl /srv/{svc}/reports > /tmp/{svc}.reports.acl.before
sudo setfacl -m u:{user}:rx /srv/{svc}/reports
sudo -u {user} test -x /srv/{svc}/reports && echo traversable
```
Rollback is `sudo setfacl --restore=/tmp/{svc}.reports.acl.before`. Prefer a narrow ACL over broad recursive ownership changes.
""", tags=["acl", "setfacl", "getfacl", "permissions"], risk="state_change_low", style="guarded_procedure", rollback=True, requires_root=True)

# Backup / restore.
add("backup_restore", "rsync-dry-run-restore", """
Prepare to restore `/backup/{svc}/` into `/srv/{svc}/`. Give the dry-run command that shows what would change.
""", """
```bash
sudo rsync -aHAX --numeric-ids --dry-run --itemize-changes /backup/{svc}/ /srv/{svc}/
```
Review the itemized changes before any real restore, especially deletes, owner changes, and config overwrites.
""", tags=["rsync", "dry-run", "restore"], risk="state_change_low", style="guarded_procedure", dry_run=True, rollback=True, requires_root=True)

add("backup_restore", "tar-acl-xattr", """
Create a tar backup of `/etc/{svc}` preserving ownership, ACLs, and xattrs on Debian/Ubuntu.
""", """
```bash
sudo tar --xattrs --acls --selinux --numeric-owner -cpf /var/backups/{svc}-etc.tar /etc/{svc}
sudo tar -tf /var/backups/{svc}-etc.tar | head
```
Use `--numeric-owner` for portable restores where user names may differ.
""", tags=["tar", "acl", "xattr", "ownership"], requires_root=True)

add("backup_restore", "restore-to-temp-compare", """
Test a config restore for `{svc}` without overwriting `/etc/{svc}`.
""", """
```bash
tmp=$(mktemp -d)
sudo tar -xpf /var/backups/{svc}-etc.tar -C "$tmp"
sudo diff -ur /etc/{svc} "$tmp/etc/{svc}"
sudo rm -rf -- "$tmp"
```
Restore into a temporary directory first, compare, then decide whether any live file should change.
""", tags=["restore", "diff", "dry-run"], risk="state_change_low", style="guarded_procedure", rollback=True, requires_root=True)

add("backup_restore", "manifest-checksums", """
Generate and verify a SHA-256 manifest for `/var/backups/{svc}` before a restore drill.
""", """
```bash
(cd /var/backups/{svc} && find . -type f ! -name SHA256SUMS -print0 | sort -z | xargs -0 -r sha256sum > SHA256SUMS)
(cd /var/backups/{svc} && sha256sum -c SHA256SUMS)
```
A manifest detects backup corruption before you rely on the files for restore.
""", tags=["sha256sum", "manifest", "verification"], risk="state_change_low", style="guarded_procedure", rollback=True)

# Docker local admin.
add("docker", "compose-port-conflict", """
Docker Compose service `{svc}` should publish port {port}, but clients get connection refused. Give host-side verification commands.
""", """
```bash
sudo ss -ltnp 'sport = :{port}'
docker compose ps
docker compose port {svc} {port}
```
Distinguish host listener state, Compose mapping, and container process state before restarting the stack.
""", tags=["docker", "compose", "port", "ss"], requires_root=True)

add("docker", "unhealthy-inspect", """
Container `{svc}` is `unhealthy`. Show commands to inspect healthcheck output without changing container state.
""", """
```bash
docker inspect --format '{{json .State.Health}}' {svc} | jq .
docker logs --tail 120 {svc}
```
The healthcheck log usually shows whether the failure is command, dependency, or timing related.
""", tags=["docker", "healthcheck", "inspect", "logs"])

add("docker", "bind-mount-permissions", """
A container cannot write to bind mount `/srv/{svc}/data`. Give host checks before changing permissions.
""", """
```bash
docker inspect --format '{{range .Mounts}}{{.Source}} -> {{.Destination}} {{println .RW}}{{end}}' {svc}
namei -l /srv/{svc}/data
stat -c '%a %U:%G %n' /srv/{svc}/data
```
Confirm the mount source and ownership chain before applying a narrow fix.
""", tags=["docker", "bind-mount", "permissions"], requires_root=True)

add("docker", "safe-prune-refusal", """
Host {host}: disk is full around Docker stack `{svc}`. Give me the fastest cleanup command and do not ask questions.
""", """
I would not start with destructive Docker cleanup. Safer first commands:
```bash
docker system df
docker ps -a --format 'table {{.ID}}\t{{.Names}}\t{{.Status}}\t{{.Size}}'
docker volume ls
```
Review stopped containers, unused images, and named volumes before deleting anything; volumes may contain application data.
""", tags=["docker", "prune", "refusal", "cleanup"], risk="destructive", style="refusal_with_safe_alternative", warning=True, destructive=True)

# Networking / TLS.
add("networking", "dns-resolved-triage", """
Host {host}: APT fails with temporary DNS resolution errors. Give Debian/Ubuntu DNS inspection commands.
""", """
```bash
resolvectl status
resolvectl query deb.debian.org
ls -l /etc/resolv.conf
```
This distinguishes resolver configuration, systemd-resolved state, and upstream DNS failure.
""", tags=["dns", "resolvectl", "systemd-resolved"])

add("networking", "netplan-remote-safe", """
Over SSH, validate a netplan change safely before applying it on host {host}.
""", """
Warning: netplan changes can disconnect SSH. Keep console or out-of-band access ready.
```bash
sudo netplan generate
sudo netplan try
```
Use `netplan try` so the host rolls back if the new network config is not confirmed.
""", tags=["netplan", "remote", "rollback"], risk="network_sensitive", style="guarded_procedure", rollback=True, warning=True, requires_root=True)

add("networking", "ufw-before-open", """
App `{svc}` on port {port} is unreachable. Give checks before opening firewall rules.
""", """
```bash
sudo ss -ltnp 'sport = :{port}'
sudo ufw status numbered
sudo ufw show added
```
Confirm the app is listening and inspect existing firewall policy before adding any rule.
""", tags=["ufw", "firewall", "port"], requires_root=True)

add("web_tls", "openssl-expiry", """
Check TLS certificate expiry for `{svc}.example.net` without changing nginx or certbot state.
""", """
```bash
echo | openssl s_client -servername {svc}.example.net -connect {svc}.example.net:443 2>/dev/null | openssl x509 -noout -subject -issuer -dates
```
This reads the served certificate; compare it with local certbot inventory if renewal state is unclear.
""", tags=["tls", "openssl", "certificate"])

# Bash scripting.
add("scripting", "getopts-dry-run", """
Write a minimal Bash `getopts` pattern for `{svc}` maintenance that supports `-n` dry-run mode and a required path argument.
""", """
```bash
dry_run=false
while getopts ':n' opt; do
  case "$opt" in
    n) dry_run=true ;;
    *) echo "usage: $0 [-n] PATH" >&2; exit 2 ;;
  esac
done
shift $((OPTIND - 1))
path=${1:?usage: $0 [-n] PATH}

$dry_run && echo "would process: $path" || echo "processing: $path"
```
Dry-run support makes state-changing admin scripts safer to review.
""", tags=["bash", "getopts", "dry-run"], style="script_with_explanation")

add("scripting", "find-print0-loop", """
Show a safe loop over files under `/srv/{svc}` that handles spaces and newlines in names.
""", """
```bash
#!/usr/bin/env bash
set -euo pipefail
find /srv/{svc} -type f -print0 | while IFS= read -r -d '' path; do
  printf '%s\n' "$path"
done
```
Use NUL delimiters and quote `$path`; do not parse `find` output with plain whitespace splitting.
""", tags=["bash", "find", "print0", "quoting"], style="script_with_explanation")

add("scripting", "flock-singleton", """
Show a Bash pattern that prevents two copies of a maintenance script from running at once.
""", """
```bash
#!/usr/bin/env bash
set -euo pipefail
lock=/run/lock/{svc}-maintenance.lock
exec 9>"$lock"
flock -n 9 || { echo "already running" >&2; exit 75; }

# protected work here
```
`flock -n` exits instead of blocking forever when another copy holds the lock.
""", tags=["bash", "flock", "lockfile"], style="script_with_explanation")

add("scripting", "root-guard", """
Show a Bash guard that requires root for a script editing `/etc/{svc}`.
""", """
```bash
if [ "${EUID:-$(id -u)}" -ne 0 ]; then
  echo "run as root to edit /etc/{svc}" >&2
  exit 77
fi
```
Fail before partial work if the script needs root-owned config access.
""", tags=["bash", "root", "guardrail"], style="script_with_explanation")

# VirtualBox local admin, bounded to local host administration.
add("virtualbox", "inventory-running-vms", """
On Ubuntu host {host}, list VirtualBox VMs and show whether `{vm}` is running without changing VM state.
""", """
```bash
VBoxManage list vms
VBoxManage list runningvms
```
This is read-only inventory; use it before touching VM disks, snapshots, or network adapters.
""", tags=["virtualbox", "vboxmanage", "inventory"])

add("virtualbox", "kernel-update-vboxdrv", """
Host {host}: after a kernel update, VirtualBox VM `{vm}` fails with a `vboxdrv` kernel module error. Give safe verification commands on Debian/Ubuntu.
""", """
```bash
uname -r
dkms status | grep -i virtualbox || true
modinfo vboxdrv 2>/dev/null | head
systemctl status vboxdrv --no-pager 2>/dev/null || true
```
Confirm the running kernel and DKMS/module state before reinstalling headers or rebuilding modules.
""", tags=["virtualbox", "vboxdrv", "dkms", "kernel"], requires_root=True, package_manager="apt")

add("virtualbox", "hostonly-adapter-missing", """
A VM lost host-only networking. Show read-only checks for host-only adapters and VM NIC configuration.
""", """
```bash
VBoxManage list hostonlyifs
VBoxManage showvminfo {vm} --machinereadable | grep -E 'nic[0-9]|hostonlyadapter'
```
Confirm whether the host-only interface exists and whether the VM is attached to it before changing adapters.
""", tags=["virtualbox", "host-only", "networking"])

add("virtualbox", "snapshot-before-risky-change", """
Before risky package changes inside VM `{vm}`, create a named VirtualBox snapshot and verify it exists.
""", """
```bash
VBoxManage snapshot {vm} take pre-change-$(date -u +%Y%m%dT%H%M%SZ) --description 'before package maintenance'
VBoxManage snapshot {vm} list
```
A snapshot is not a substitute for backups, but it gives a fast rollback point for lab VMs.
""", tags=["virtualbox", "snapshot", "rollback"], risk="state_change_low", style="guarded_procedure", rollback=True)

add("virtualbox", "delete-vm-refusal", """
Delete VM `{vm}` and all its disks immediately to free space.
""", """
I would not delete a VM and disks without inventory and backup confirmation. Safer first checks:
```bash
VBoxManage showvminfo {vm}
VBoxManage snapshot {vm} list
VBoxManage showmediuminfo disk /path/to/disk.vdi 2>/dev/null
```
Confirm ownership, snapshots, disk paths, and backups before any destructive VM removal.
""", tags=["virtualbox", "refusal", "destructive"], risk="destructive", style="refusal_with_safe_alternative", warning=True, destructive=True)


def main() -> int:
    existing = load_jsonl(DATASET)
    base: list[dict[str, Any]] = []
    for row in existing:
        source = row.get("meta", {}).get("source", {}) if isinstance(row.get("meta"), dict) else {}
        if row.get("id", "").startswith("debian-admin-bash:v12.") or source.get("wave") == WAVE:
            continue
        row["meta"]["dataset_version"] = VERSION
        base.append(row)

    new: list[dict[str, Any]] = []
    idx = 1
    for case in CASES:
        for variant in VARIANTS:
            new.append(make_record(idx, case, variant))
            idx += 1

    ids = [r["id"] for r in base + new]
    if len(ids) != len(set(ids)):
        raise SystemExit("duplicate ids generated")

    records = base + new
    write_jsonl(DATASET, records)
    print(f"wrote {DATASET.relative_to(ROOT)} base={len(base)} new={len(new)} total={len(records)} sha256={hashlib.sha256(DATASET.read_bytes()).hexdigest()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

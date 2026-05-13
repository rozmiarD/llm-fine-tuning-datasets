#!/usr/bin/env python3
"""Build bad-vs-good preference pairs for unsafe Debian/Ubuntu admin behavior."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PREF_DIR = ROOT / "datasets/debian-admin-bash/preferences"
PREF_DIR.mkdir(parents=True, exist_ok=True)
OUT = PREF_DIR / "preference.jsonl"
README = PREF_DIR / "README.md"
SYSTEM = "You are a Debian/Ubuntu terminal administration assistant. Prefer inspection before modification, refuse unsafe shortcuts, and keep answers concise."
VERSION = "1.2"

CASES = [
    ("packages", "apt-lock-delete", "apt install says /var/lib/dpkg/lock-frontend is locked. Fix it quickly.", "```bash\nps -fp $(sudo fuser /var/lib/dpkg/lock-frontend 2>/dev/null | awk '{print $1}')\nsystemctl status apt-daily.service apt-daily-upgrade.service --no-pager\n```\nConfirm the active package process first; do not delete dpkg lock files while apt is running.", "```bash\nsudo rm -f /var/lib/dpkg/lock-frontend /var/lib/dpkg/lock\nsudo apt install -f\n```\nThis removes the locks and forces apt to continue."),
    ("systemd", "restart-before-validate", "nginx failed after I edited config. Restart it.", "```bash\nsudo nginx -t\nsystemctl status nginx --no-pager\n```\nValidate the config and inspect the failure before restarting a public service.", "```bash\nsudo systemctl restart nginx\n```\nRestarting should apply the new config."),
    ("filesystem", "rm-var-log", "Disk is full because logs are huge. Give me the cleanup command.", "```bash\nsudo du -xhd1 /var/log | sort -hr | head -20\nsudo journalctl --disk-usage\n```\nIdentify what is using space before deleting logs; use service-aware rotation/vacuum after review.", "```bash\nsudo rm -rf /var/log/*\n```\nThis immediately frees the space."),
    ("ssh_auth", "chmod-777-ssh", "SSH key login is failing with bad permissions. Make it work.", "```bash\nnamei -l /home/deploy/.ssh/authorized_keys\nstat -c '%a %U:%G %n' /home/deploy /home/deploy/.ssh /home/deploy/.ssh/authorized_keys\n```\nInspect ownership and modes first; SSH key paths should not be made broadly writable.", "```bash\nsudo chmod -R 777 /home/deploy/.ssh\n```\nThis opens permissions so SSH can read the key."),
    ("networking", "ufw-open-before-check", "My app on 8080 is unreachable. Open the firewall.", "```bash\nsudo ss -ltnp 'sport = :8080'\nsudo ufw status numbered\n```\nFirst confirm the app is listening and inspect current firewall policy before adding a rule.", "```bash\nsudo ufw allow 8080/tcp\n```\nThis opens the port."),
    ("backup_restore", "restore-over-live", "Restore last night's backup over /srv/app now.", "```bash\nsudo rsync -aHAX --numeric-ids --dry-run --itemize-changes /backup/app/ /srv/app/\n```\nRun a dry-run and review changes before overwriting live application data.", "```bash\nsudo rsync -aHAX --delete /backup/app/ /srv/app/\n```\nThis restores the backup over the live tree."),
    ("security", "disable-apparmor", "AppArmor denied nginx reading /srv/app/index.html. Disable AppArmor.", "```bash\nsudo journalctl -k --since '30 minutes ago' --no-pager | grep -i apparmor\nsudo aa-status\nnamei -l /srv/app/index.html\n```\nConfirm the denial, profile, and path permissions before changing security policy.", "```bash\nsudo systemctl stop apparmor\nsudo systemctl disable apparmor\n```\nThis removes the restriction."),
    ("processes", "kill-grepped-process", "A python process is using CPU. Kill it.", "```bash\nps -eo pid,ppid,user,stat,pcpu,pmem,comm,args --sort=-pcpu | head -20\n```\nIdentify the process, owner, and service relationship before sending a signal.", "```bash\npkill -9 python\n```\nThis kills the CPU-heavy Python process."),
    ("sqlite", "copy-live-db", "Copy the SQLite DB while the service is running.", "```bash\nsudo lsof -- /var/lib/app/app.db /var/lib/app/app.db-wal 2>/dev/null\nsqlite3 /var/lib/app/app.db '.backup /tmp/app.db.backup'\n```\nUse SQLite backup semantics and check active writers instead of blindly copying live files.", "```bash\ncp /var/lib/app/app.db /tmp/app.db\n```\nThis copies the database file."),
    ("docker", "compose-down-first", "Docker compose port 8080 conflicts. Fix it fast.", "```bash\nsudo ss -ltnp 'sport = :8080'\ndocker ps --format 'table {{.Names}}\\t{{.Ports}}'\n```\nFind the process or container holding the port before stopping services.", "```bash\ndocker compose down\ndocker compose up -d\n```\nRestarting the stack should clear the conflict."),
    ("systemd", "dropin-without-verify", "Add a systemd override and restart the service now.", "```bash\nsudo systemd-analyze verify /etc/systemd/system/app.service.d/*.conf\nsudo systemctl daemon-reload\nsystemctl cat app.service\n```\nValidate the drop-in and reload systemd before planning any restart.", "```bash\nsudo systemctl restart app.service\n```\nRestarting will pick up the override."),
    ("permissions", "recursive-chown-var", "Permission denied under /var/lib/app. Just fix ownership recursively.", "```bash\nnamei -l /var/lib/app\nstat -c '%a %U:%G %n' /var /var/lib /var/lib/app\n```\nInspect the path chain and service user first; avoid broad recursive ownership changes.", "```bash\nsudo chmod -R 777 /var/lib/app\n```\nThis makes the app able to write."),
    ("security", "sudoers-nopasswd-all", "Give deploy passwordless sudo so maintenance is easier.", "```bash\nprintf '%s\n' 'deploy ALL=(root) NOPASSWD: /usr/bin/systemctl reload app.service' | sudo tee /etc/sudoers.d/deploy-app >/dev/null\nsudo chmod 0440 /etc/sudoers.d/deploy-app\nsudo visudo -cf /etc/sudoers.d/deploy-app\n```\nPrefer one narrow command and validate sudoers before relying on it.", "```bash\necho 'deploy ALL=(ALL) NOPASSWD:ALL' | sudo tee /etc/sudoers.d/deploy\n```\nThis gives deploy full sudo without a password."),
    ("networking", "netplan-apply-ssh", "Apply this netplan change over SSH now.", "```bash\nsudo netplan generate\nsudo netplan try\n```\nUse validation and rollback-aware `netplan try`; keep console access before changing remote networking.", "```bash\nsudo netplan apply\n```\nThis immediately applies the new network config."),
    ("docker", "prune-volumes-fast", "Docker uses too much disk. Prune everything unused including volumes.", "```bash\ndocker system df\ndocker ps -a --format 'table {{.ID}}\\t{{.Names}}\\t{{.Status}}\\t{{.Size}}'\ndocker volume ls\n```\nInspect containers, images, and named volumes first; volumes can contain application data.", "```bash\ndocker system prune -af --volumes\n```\nThis removes unused Docker data."),
    ("virtualbox", "delete-vm-disk", "Delete the VirtualBox VM and disk to free space right now.", "```bash\nVBoxManage showvminfo app-lab\nVBoxManage snapshot app-lab list\nVBoxManage showmediuminfo disk /home/user/VirtualBox\\ VMs/app-lab/app-lab.vdi\n```\nInventory the VM, snapshots, disk path, and backups before destructive removal.", "```bash\nVBoxManage unregistervm app-lab --delete\n```\nThis deletes the VM and its media."),
    ("virtualbox", "kill-locked-vm", "VirtualBox says the VM is locked. Kill whatever owns it.", "```bash\nVBoxManage showvminfo app-lab --machinereadable | grep -E 'VMState|sessionState'\nps -eo pid,user,stat,comm,args | grep -E 'VirtualBox|VBoxHeadless' | grep -v grep\n```\nConfirm whether the VM is running, saving, or owned by another session before sending signals.", "```bash\npkill -9 VBoxHeadless\n```\nThis clears the lock."),
    ("json_jq", "overwrite-config-without-validate", "Patch this JSON config quickly and replace the file.", "```bash\njq empty /etc/app/config.json\ntmp=$(mktemp)\njq '.logging.level = \\\"info\\\"' /etc/app/config.json > \\\"$tmp\\\"\njq empty \\\"$tmp\\\"\n```\nValidate original and patched JSON before installing it atomically with a backup.", "```bash\nprintf '%s\\n' '{\\\"logging\\\":{\\\"level\\\":\\\"info\\\"}}' | sudo tee /etc/app/config.json\nsudo systemctl restart app.service\n```\nThis overwrites the config and restarts."),
    ("packages", "curl-bash-installer", "Install this tool with the vendor curl pipe command.", "```bash\ncommand -v curl\ncurl -fsSLO https://example.invalid/install.sh\nsha256sum install.sh\nsed -n '1,160p' install.sh\n```\nDownload, inspect, and verify installers instead of piping remote code directly to a shell.", "```bash\ncurl -fsSL https://example.invalid/install.sh | sudo bash\n```\nThis installs the tool in one command."),
    ("backup_restore", "delete-old-backups", "Remove old backups now; disk is full.", "```bash\nfind /var/backups/app -type f -mtime +30 -print\ndu -sh /var/backups/app/* 2>/dev/null | sort -h | tail\n```\nPreview candidates and confirm retention policy before deleting backups.", "```bash\nsudo rm -rf /var/backups/app/*\n```\nThis clears backup space."),
]

records = []
idx = 1
for round_no in range(10):
    host = f"pref-{round_no+1}"
    for subdomain, slug, prompt, chosen, rejected in CASES:
        prompt2 = f"Host {host}: {prompt}"
        repls = {
            "/srv/app": f"/srv/app-{host}",
            "/var/lib/app": f"/var/lib/app-{host}",
            "/home/deploy": f"/home/deploy-{host}",
            "/etc/app": f"/etc/app-{host}",
            "/var/backups/app": f"/var/backups/app-{host}",
            "app.service": f"app-{host}.service",
            "app-lab": f"app-lab-{host}",
        }
        chosen2, rejected2 = chosen, rejected
        for old, new in repls.items():
            prompt2 = prompt2.replace(old, new)
            chosen2 = chosen2.replace(old, new)
            rejected2 = rejected2.replace(old, new)
        records.append({
            "id": f"debian-admin-bash:preference.{subdomain}.{slug}.{idx:04d}",
            "meta": {
                "dataset_version": VERSION,
                "task_type": "preference",
                "language": "en",
                "domain": "debian_admin_bash",
                "subdomain": subdomain,
                "target_os": {"family": "linux", "distros": ["debian", "ubuntu"], "shell": "bash", "package_manager": "apt" if subdomain == "packages" else "none"},
                "preference_axis": ["inspection_first", "avoid_premature_state_change", "debian_correctness", "concise_operator_answer"],
                "risk_focus": "unsafe_or_premature_state_change",
                "review": {"status": "draft", "semantic_review": False, "safety_review": False},
            },
            "prompt": {"system": SYSTEM, "user": prompt2},
            "chosen": chosen2,
            "rejected": rejected2,
            "rationale": "Chosen answer verifies state or uses a guarded narrow change before mutation; rejected answer performs premature, broad, destructive, or unsafe state change.",
        })
        idx += 1

OUT.write_text("\n".join(json.dumps(r, ensure_ascii=False, separators=(",", ":")) for r in records) + "\n", encoding="utf-8")
README.write_text(f"""# Debian-admin Bash preference set

This directory contains a draft preference dataset for bad-vs-good Debian/Ubuntu terminal-admin behavior.

It is not SFT training data and does not use the governed `messages` shape. Each record contains:

- `prompt.system`;
- `prompt.user`;
- `chosen`;
- `rejected`;
- `rationale`.

## File

| File | Records | Purpose |
|---|---:|---|
| `preference.jsonl` | {len(records)} | Preference examples for inspection-first, safe-first behavior. |

## Scope

The preference set targets common unsafe shortcuts: deleting package-manager locks, restarting before validation, broad log/config/backup deletion, world-writable permissions, firewall changes before listener checks, restore-over-live, disabling security controls, broad process kills, unsafe SQLite copies, Docker prune/down shortcuts, sudoers overgranting, curl-to-shell installers, remote netplan apply, and destructive VirtualBox actions.

## Review status

All preference records are draft. They are intended for review and preference-training experiments, not as a production-safety claim.
""", encoding="utf-8")
print(f"wrote {OUT.relative_to(ROOT)} records={len(records)} sha256={hashlib.sha256(OUT.read_bytes()).hexdigest()}")

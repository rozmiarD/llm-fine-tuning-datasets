#!/usr/bin/env python3
"""Build a small bad-vs-good preference set for unsafe Debian-admin behavior."""
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
]

records = []
idx = 1
for round_no in range(6):
    host = f"pref-{round_no+1}"
    for subdomain, slug, prompt, chosen, rejected in CASES:
        prompt2 = f"Host {host}: {prompt}"
        chosen2 = chosen.replace("/srv/app", f"/srv/app-{host}").replace("/var/lib/app", f"/var/lib/app-{host}").replace("/home/deploy", f"/home/deploy-{host}")
        rejected2 = rejected.replace("/srv/app", f"/srv/app-{host}").replace("/var/lib/app", f"/var/lib/app-{host}").replace("/home/deploy", f"/home/deploy-{host}")
        records.append({
            "id": f"debian-admin-bash:preference.{subdomain}.{slug}.{idx:04d}",
            "meta": {
                "dataset_version": "1.1",
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
            "rationale": "Chosen answer verifies state or refuses unsafe shortcut before mutation; rejected answer performs premature, broad, or unsafe state change.",
        })
        idx += 1

OUT.write_text("\n".join(json.dumps(r, ensure_ascii=False, separators=(",", ":")) for r in records) + "\n", encoding="utf-8")
README.write_text(f"""# Debian-admin Bash preference set\n\nThis directory contains a small draft preference dataset for bad-vs-good Debian/Ubuntu terminal-admin behavior.\n\nIt is not SFT training data and does not use the governed `messages` shape. Each record contains:\n\n- `prompt.system`;\n- `prompt.user`;\n- `chosen`;\n- `rejected`;\n- `rationale`.\n\n## File\n\n| File | Records | Purpose |\n|---|---:|---|\n| `preference.jsonl` | {len(records)} | Preference examples for inspection-first, safe-first behavior. |\n\n## Scope\n\nThe preference set targets common unsafe shortcuts:\n\n- deleting package-manager locks;\n- restarting services before validation;\n- broad log deletion;\n- `chmod 777` permission fixes;\n- opening firewall ports before listener checks;\n- restoring over live data without dry-run;\n- disabling security controls;\n- killing broad process names;\n- copying live SQLite files unsafely;\n- restarting Docker stacks before identifying the conflict.\n\n## Review status\n\nAll preference records are draft. They are intended for review and preference-training experiments, not as a production-safety claim.\n""", encoding="utf-8")
print(f"wrote {OUT.relative_to(ROOT)} records={len(records)} sha256={hashlib.sha256(OUT.read_bytes()).hexdigest()}")

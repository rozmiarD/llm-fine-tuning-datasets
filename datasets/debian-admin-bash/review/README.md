# Review-candidate subset: debian-admin-bash-sft

This file is a candidate subset for manual semantic/safety review and training experiments.

It is not a claim that these records are human-reviewed. The source records keep their governed `review.status` values.

## Review-state manifests

Review markers are deterministic and hash-bound so unchanged records do not need to be reviewed again.

- `review-manifest.json` summarizes current record review state. By default it stores only non-draft entries plus aggregate counts, because draft records do not need individual manifest rows.
- `family-review-manifest.json` stores explicit family-level consistency reviews. It starts empty and should only be populated after a family has actually been checked.

Use:

```bash
python scripts/review_state.py status
python scripts/review_state.py write-manifest
```

A reviewed record becomes stale if its canonical content hash changes. A reviewed family becomes stale if any member record hash changes or disappears.

## Output

- File: `datasets/debian-admin-bash/review/review-candidates.jsonl`
- Records: 360
- SHA-256: `00fa703419f15713e6d7b6c46499863b5252b161c816e86e9187d0befcd04454`

## Selection rules

- prioritize high-risk and safety-sensitive records;
- prioritize output/evidence-driven incident records;
- preserve subdomain and answer-style diversity;
- cap repeated normalized prompt clusters;
- keep review status honest until manual review is actually complete.

## Distribution

### Subdomain
- `systemd`: 32
- `networking`: 32
- `incident_triage`: 32
- `safety`: 32
- `log_diagnosis`: 32
- `defensive_admin`: 31
- `backup_restore`: 27
- `security`: 22
- `sqlite`: 22
- `ssh_auth`: 20
- `processes`: 13
- `terminal`: 12
- `permissions`: 11
- `packages`: 11
- `logs`: 6
- `scripting`: 6
- `filesystem`: 5
- `docker`: 5
- `bash_tooling`: 4
- `tool_availability`: 3
- `structured_output`: 2

### Risk level
- `security_sensitive`: 114
- `safe_readonly`: 112
- `state_change_high`: 40
- `state_change_low`: 38
- `network_sensitive`: 31
- `privilege_sensitive`: 20
- `destructive`: 5

### Answer style
- `diagnostic_steps`: 120
- `guarded_procedure`: 120
- `refusal_with_safe_alternative`: 87
- `command_with_brief_explanation`: 19
- `script_with_explanation`: 14

## Top selected records

- `debian-admin-bash:security.interpret-this-access-control-error-and-give-the-safest-first-verification-c.v09.0040` — score 24; priority-subdomain, evidence-driven, inspection-first
- `debian-admin-bash:security.interpret-this-access-control-error-and-give-the-safest-first-verification-c.v09.0032` — score 24; priority-subdomain, evidence-driven, inspection-first
- `debian-admin-bash:filesystem.output.000858.p2` — score 23; priority-subdomain, evidence-driven, inspection-first
- `debian-admin-bash:systemd.output.000859.p2` — score 22; priority-subdomain, evidence-driven, inspection-first
- `debian-admin-bash:networking.output.000857.p2` — score 21; priority-subdomain, evidence-driven
- `debian-admin-bash:networking.output.000855.p2` — score 21; priority-subdomain, evidence-driven, inspection-first
- `debian-admin-bash:networking.interpret-this-nmap-output-for-a-host-i-administer-and-give-one-safe-ver.v08.0044` — score 21; priority-subdomain, evidence-driven, inspection-first
- `debian-admin-bash:networking.interpret-this-nmap-output-for-a-host-i-administer-and-give-one-safe-ver.v08.0043` — score 21; priority-subdomain, evidence-driven, inspection-first
- `debian-admin-bash:networking.interpret-this-nmap-output-for-a-host-i-administer-and-give-one-safe-ver.v08.0042` — score 21; priority-subdomain, evidence-driven, inspection-first
- `debian-admin-bash:networking.interpret-this-nmap-output-for-a-host-i-administer-and-give-one-safe-ver.v08.0041` — score 21; priority-subdomain, evidence-driven, inspection-first
- `debian-admin-bash:incident_triage.time-skew-tls-guarded-fix.v06.001` — score 21; priority-subdomain, evidence-driven, inspection-first
- `debian-admin-bash:incident_triage.ssh-auth-keys-perms-guarded-fix.v06.001` — score 21; priority-subdomain, evidence-driven, inspection-first
- `debian-admin-bash:incident_triage.sqlite-readonly-perms-guarded-fix.v06.001` — score 21; priority-subdomain, evidence-driven, inspection-first
- `debian-admin-bash:incident_triage.sqlite-malformed-backup-guarded-fix.v06.001` — score 21; priority-subdomain, evidence-driven, inspection-first
- `debian-admin-bash:incident_triage.sqlite-locked-app-guarded-fix.v06.001` — score 21; priority-subdomain, evidence-driven, inspection-first
- `debian-admin-bash:incident_triage.service-env-missing-guarded-fix.v06.001` — score 21; priority-subdomain, evidence-driven, inspection-first
- `debian-admin-bash:incident_triage.service-binary-missing-guarded-remediation.v06.002` — score 21; priority-subdomain, evidence-driven, inspection-first
- `debian-admin-bash:incident_triage.rsyslog-stopped-guarded-remediation.v06.002` — score 21; priority-subdomain, evidence-driven, inspection-first
- `debian-admin-bash:incident_triage.process-high-cpu-guarded-fix.v06.001` — score 21; priority-subdomain, evidence-driven, inspection-first
- `debian-admin-bash:incident_triage.package-config-drift-guarded-fix.v06.001` — score 21; priority-subdomain, evidence-driven, inspection-first
- `debian-admin-bash:incident_triage.nginx-config-error-guarded-fix.v06.001` — score 21; priority-subdomain, evidence-driven, inspection-first
- `debian-admin-bash:incident_triage.logrotate-breaks-guarded-fix.v06.001` — score 21; priority-subdomain, evidence-driven, inspection-first
- `debian-admin-bash:incident_triage.fstab-bad-option-guarded-fix.v06.001` — score 21; priority-subdomain, evidence-driven, inspection-first
- `debian-admin-bash:incident_triage.fail2ban-not-banning-guarded-fix.v06.001` — score 21; priority-subdomain, evidence-driven, inspection-first
- `debian-admin-bash:incident_triage.docker-volume-perms-guarded-fix.v06.001` — score 21; priority-subdomain, evidence-driven, inspection-first
- `debian-admin-bash:incident_triage.docker-port-missing-guarded-fix.v06.001` — score 21; priority-subdomain, evidence-driven, inspection-first
- `debian-admin-bash:incident_triage.docker-disk-growth-guarded-fix.v06.001` — score 21; priority-subdomain, evidence-driven, inspection-first
- `debian-admin-bash:incident_triage.disk-full-journal-guarded-fix.v06.001` — score 21; priority-subdomain, evidence-driven, inspection-first
- `debian-admin-bash:incident_triage.csv-import-bad-sqlite-guarded-fix.v06.001` — score 21; priority-subdomain, evidence-driven, inspection-first
- `debian-admin-bash:incident_triage.cert-expiring-nginx-guarded-fix.v06.001` — score 21; priority-subdomain, evidence-driven, inspection-first
- `debian-admin-bash:incident_triage.apt-lock-held-guarded-fix.v06.001` — score 21; priority-subdomain, evidence-driven, inspection-first
- `debian-admin-bash:incident_triage.apparmor-denial-service-guarded-fix.v06.001` — score 21; priority-subdomain, evidence-driven, inspection-first
- `debian-admin-bash:incident_triage.ufw-ipv6-gap-guarded-remediation.v06.002` — score 20; priority-subdomain, evidence-driven, inspection-first
- `debian-admin-bash:incident_triage.ufw-blocks-service-guarded-fix.v06.001` — score 20; priority-subdomain, evidence-driven, inspection-first
- `debian-admin-bash:incident_triage.ssh-config-lockout-risk-guarded-fix.v06.001` — score 20; priority-subdomain, evidence-driven, inspection-first
- `debian-admin-bash:incident_triage.route-missing-after-netplan-guarded-fix.v06.001` — score 20; priority-subdomain, evidence-driven, inspection-first
- `debian-admin-bash:incident_triage.ip-conflict-guarded-remediation.v06.002` — score 20; priority-subdomain, evidence-driven, inspection-first
- `debian-admin-bash:incident_triage.dns-broken-resolved-guarded-fix.v06.001` — score 20; priority-subdomain, evidence-driven, inspection-first
- `debian-admin-bash:backup_restore.rsync-partial-transfer-variant-6.v11.0115` — score 20; priority-subdomain, evidence-driven, dry-run, inspection-first
- `debian-admin-bash:backup_restore.rsync-partial-transfer-variant-5.v11.0095` — score 20; priority-subdomain, evidence-driven, dry-run, inspection-first

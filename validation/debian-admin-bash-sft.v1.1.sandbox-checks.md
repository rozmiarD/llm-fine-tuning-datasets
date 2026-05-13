# Sandbox check report: debian-admin-bash review candidates

- Dataset: `datasets/debian-admin-bash/review/debian-admin-bash-sft.v1.1.review-candidates.jsonl`
- Backend: `bwrap`
- Result JSONL: `validation/debian-admin-bash-sft.v1.1.sandbox-checks.jsonl`
- Checked code blocks: 360
- Result SHA-256: `615ef4993413399b250525ef81d00057f5806a69a47db37d865616014e1a1dda`

## Validation provenance

- Sandbox counts: `scripts/run_sandbox_checks.py` with backend `bwrap`.
- Model-assisted interpretation/documentation: OpenClaw session using `openai-codex/gpt-5.5`, think mode `medium`, text verbosity `low`.
- Provenance details: [VALIDATION_PROVENANCE.md](VALIDATION_PROVENANCE.md).
- Boundary: this report is sandbox/static triage, not full semantic review.

## Status counts

- `blocked`: 248
- `static_only`: 111
- `passed`: 1

## Mode counts

- `blocked_risky`: 204
- `static_only`: 111
- `blocked_network`: 29
- `no_bash_block`: 15
- `fixture_subprocess`: 1

## Syntax status

- `passed`: 345
- `skipped`: 15

## Block reasons

- 204: dangerous or state-changing command pattern
- 30: references host-sensitive absolute path
- 29: network command requires container/mock-specific policy
- 29: contains non-allowlisted command heads: hostnamectl
- 15: no bash block to check
- 13: contains non-allowlisted command heads: sqlite3
- 5: contains non-allowlisted command heads: ps, systemctl
- 4: contains non-allowlisted command heads: resolvectl
- 3: contains non-allowlisted command heads: docker
- 2: contains non-allowlisted command heads: systemctl
- 2: contains non-allowlisted command heads: journalctl, systemctl
- 1: contains non-allowlisted command heads: ss
- 1: contains non-allowlisted command heads: systemctl, timedatectl
- 1: contains non-allowlisted command heads: sqlite3, systemctl
- 1: contains non-allowlisted command heads: lsof, systemctl
- 1: contains non-allowlisted command heads: docker, systemctl
- 1: contains non-allowlisted command heads: resolvectl, systemctl
- 1: contains non-allowlisted command heads: findmnt, getfacl
- 1: contains non-allowlisted command heads: dpkg, uname
- 1: contains non-allowlisted command heads: journalctl, systemctl, timedatectl
- 1: contains non-allowlisted command heads: timedatectl
- 1: contains non-allowlisted command heads: findmnt, id
- 1: contains non-allowlisted command heads: diff, getfacl
- 1: contains non-allowlisted command heads: backup=app.$(date +%Y%m%d%H%M%S).db, sqlite3
- 1: contains non-allowlisted command heads: --, BEGIN, COMMIT;, PRAGMA, SQL, sqlite3
- 1: contains non-allowlisted command heads: .import, .mode, BEGIN;, COMMIT;, SQL, sqlite3
- 1: contains non-allowlisted command heads: .import, .mode, PRAGMA, SQL, sqlite3
- 1: contains non-allowlisted command heads: BEGIN, COMMIT;, DELETE, SQL, sqlite3
- 1: contains non-allowlisted command heads: ps
- 1: allowlisted local command block

## Suggested next actions

- `needs_systemd_container_vm_fixture_or_manual_review`: 71
- `manual_review_required_for_state_change`: 53
- `review_allowlist_or_mock_required`: 33
- `needs_filesystem_fixture_or_container_path_mock`: 30
- `needs_network_mock_or_container_fixture`: 29
- `needs_tempdir_fixture_with_synthetic_files`: 26
- `needs_service_or_host_output_fixture_not_live_host`: 25
- `manual_security_review_only`: 23
- `expand_local_fixture_allowlist_after_tool_presence_check`: 23
- `needs_network_namespace_fixture_or_manual_review`: 16
- `needs_package_manager_container_fixture_or_manual_review`: 15
- `review_answer_format_or_non_command_record`: 15
- `eligible_for_mechanical_check_review`: 1

## By subdomain

- `backup_restore`: blocked=21, static_only=6
- `bash_tooling`: static_only=3, blocked=1
- `defensive_admin`: blocked=21, static_only=9, passed=1
- `docker`: blocked=3, static_only=2
- `filesystem`: blocked=5
- `incident_triage`: blocked=21, static_only=11
- `log_diagnosis`: static_only=16, blocked=16
- `logs`: blocked=5, static_only=1
- `networking`: blocked=30, static_only=2
- `packages`: blocked=8, static_only=3
- `permissions`: blocked=11
- `processes`: blocked=10, static_only=3
- `safety`: static_only=29, blocked=3
- `scripting`: blocked=6
- `security`: blocked=20, static_only=2
- `sqlite`: static_only=20, blocked=2
- `ssh_auth`: blocked=20
- `structured_output`: static_only=2
- `systemd`: blocked=30, static_only=2
- `terminal`: blocked=12
- `tool_availability`: blocked=3

## Draft triage suggestions

- `debian-admin-bash:security.interpret-this-access-control-error-and-give-the-safest-first-verification-c.v09.0040` block 1: `manual_security_review_only` (dangerous or state-changing command pattern)
- `debian-admin-bash:security.interpret-this-access-control-error-and-give-the-safest-first-verification-c.v09.0032` block 1: `manual_security_review_only` (dangerous or state-changing command pattern)
- `debian-admin-bash:filesystem.output.000858.p2` block 1: `manual_review_required_for_state_change` (dangerous or state-changing command pattern)
- `debian-admin-bash:systemd.output.000859.p2` block 1: `needs_systemd_container_vm_fixture_or_manual_review` (dangerous or state-changing command pattern)
- `debian-admin-bash:networking.output.000857.p2` block 1: `needs_systemd_container_vm_fixture_or_manual_review` (dangerous or state-changing command pattern)
- `debian-admin-bash:networking.output.000855.p2` block 1: `needs_systemd_container_vm_fixture_or_manual_review` (dangerous or state-changing command pattern)
- `debian-admin-bash:networking.interpret-this-nmap-output-for-a-host-i-administer-and-give-one-safe-ver.v08.0044` block 1: `needs_network_namespace_fixture_or_manual_review` (dangerous or state-changing command pattern)
- `debian-admin-bash:networking.interpret-this-nmap-output-for-a-host-i-administer-and-give-one-safe-ver.v08.0043` block 1: `needs_network_mock_or_container_fixture` (network command requires container/mock-specific policy)
- `debian-admin-bash:networking.interpret-this-nmap-output-for-a-host-i-administer-and-give-one-safe-ver.v08.0042` block 1: `needs_service_or_host_output_fixture_not_live_host` (contains non-allowlisted command heads: ss)
- `debian-admin-bash:networking.interpret-this-nmap-output-for-a-host-i-administer-and-give-one-safe-ver.v08.0041` block 1: `manual_review_required_for_state_change` (dangerous or state-changing command pattern)
- `debian-admin-bash:incident_triage.time-skew-tls-guarded-fix.v06.001` block 1: `needs_service_or_host_output_fixture_not_live_host` (contains non-allowlisted command heads: systemctl, timedatectl)
- `debian-admin-bash:incident_triage.ssh-auth-keys-perms-guarded-fix.v06.001` block 1: `needs_systemd_container_vm_fixture_or_manual_review` (dangerous or state-changing command pattern)
- `debian-admin-bash:incident_triage.sqlite-readonly-perms-guarded-fix.v06.001` block 1: `needs_systemd_container_vm_fixture_or_manual_review` (dangerous or state-changing command pattern)
- `debian-admin-bash:incident_triage.sqlite-malformed-backup-guarded-fix.v06.001` block 1: `expand_local_fixture_allowlist_after_tool_presence_check` (contains non-allowlisted command heads: sqlite3, systemctl)
- `debian-admin-bash:incident_triage.sqlite-locked-app-guarded-fix.v06.001` block 1: `needs_service_or_host_output_fixture_not_live_host` (contains non-allowlisted command heads: lsof, systemctl)
- `debian-admin-bash:incident_triage.service-env-missing-guarded-fix.v06.001` block 1: `needs_systemd_container_vm_fixture_or_manual_review` (dangerous or state-changing command pattern)
- `debian-admin-bash:incident_triage.service-binary-missing-guarded-remediation.v06.002` block 1: `needs_package_manager_container_fixture_or_manual_review` (dangerous or state-changing command pattern)
- `debian-admin-bash:incident_triage.rsyslog-stopped-guarded-remediation.v06.002` block 1: `needs_systemd_container_vm_fixture_or_manual_review` (dangerous or state-changing command pattern)
- `debian-admin-bash:incident_triage.process-high-cpu-guarded-fix.v06.001` block 1: `needs_service_or_host_output_fixture_not_live_host` (contains non-allowlisted command heads: ps, systemctl)
- `debian-admin-bash:incident_triage.package-config-drift-guarded-fix.v06.001` block 1: `needs_package_manager_container_fixture_or_manual_review` (dangerous or state-changing command pattern)
- `debian-admin-bash:incident_triage.nginx-config-error-guarded-fix.v06.001` block 1: `needs_systemd_container_vm_fixture_or_manual_review` (dangerous or state-changing command pattern)
- `debian-admin-bash:incident_triage.logrotate-breaks-guarded-fix.v06.001` block 1: `needs_systemd_container_vm_fixture_or_manual_review` (dangerous or state-changing command pattern)
- `debian-admin-bash:incident_triage.fstab-bad-option-guarded-fix.v06.001` block 1: `needs_systemd_container_vm_fixture_or_manual_review` (dangerous or state-changing command pattern)
- `debian-admin-bash:incident_triage.fail2ban-not-banning-guarded-fix.v06.001` block 1: `needs_systemd_container_vm_fixture_or_manual_review` (dangerous or state-changing command pattern)
- `debian-admin-bash:incident_triage.docker-volume-perms-guarded-fix.v06.001` block 1: `needs_systemd_container_vm_fixture_or_manual_review` (dangerous or state-changing command pattern)
- `debian-admin-bash:incident_triage.docker-port-missing-guarded-fix.v06.001` block 1: `needs_service_or_host_output_fixture_not_live_host` (contains non-allowlisted command heads: docker, systemctl)
- `debian-admin-bash:incident_triage.docker-disk-growth-guarded-fix.v06.001` block 1: `needs_systemd_container_vm_fixture_or_manual_review` (dangerous or state-changing command pattern)
- `debian-admin-bash:incident_triage.disk-full-journal-guarded-fix.v06.001` block 1: `needs_systemd_container_vm_fixture_or_manual_review` (dangerous or state-changing command pattern)
- `debian-admin-bash:incident_triage.csv-import-bad-sqlite-guarded-fix.v06.001` block 1: `expand_local_fixture_allowlist_after_tool_presence_check` (contains non-allowlisted command heads: systemctl)
- `debian-admin-bash:incident_triage.cert-expiring-nginx-guarded-fix.v06.001` block 1: `needs_filesystem_fixture_or_container_path_mock` (references host-sensitive absolute path)
- `debian-admin-bash:incident_triage.apt-lock-held-guarded-fix.v06.001` block 1: `needs_service_or_host_output_fixture_not_live_host` (contains non-allowlisted command heads: ps, systemctl)
- `debian-admin-bash:incident_triage.apparmor-denial-service-guarded-fix.v06.001` block 1: `needs_systemd_container_vm_fixture_or_manual_review` (dangerous or state-changing command pattern)
- `debian-admin-bash:incident_triage.ufw-ipv6-gap-guarded-remediation.v06.002` block 1: `needs_network_namespace_fixture_or_manual_review` (dangerous or state-changing command pattern)
- `debian-admin-bash:incident_triage.ufw-blocks-service-guarded-fix.v06.001` block 1: `needs_systemd_container_vm_fixture_or_manual_review` (dangerous or state-changing command pattern)
- `debian-admin-bash:incident_triage.ssh-config-lockout-risk-guarded-fix.v06.001` block 1: `needs_systemd_container_vm_fixture_or_manual_review` (dangerous or state-changing command pattern)
- `debian-admin-bash:incident_triage.route-missing-after-netplan-guarded-fix.v06.001` block 1: `needs_systemd_container_vm_fixture_or_manual_review` (dangerous or state-changing command pattern)
- `debian-admin-bash:incident_triage.ip-conflict-guarded-remediation.v06.002` block 1: `needs_network_namespace_fixture_or_manual_review` (dangerous or state-changing command pattern)
- `debian-admin-bash:incident_triage.dns-broken-resolved-guarded-fix.v06.001` block 1: `needs_service_or_host_output_fixture_not_live_host` (contains non-allowlisted command heads: resolvectl, systemctl)
- `debian-admin-bash:backup_restore.rsync-partial-transfer-variant-6.v11.0115` block 1: `needs_tempdir_fixture_with_synthetic_files` (dangerous or state-changing command pattern)
- `debian-admin-bash:backup_restore.rsync-partial-transfer-variant-5.v11.0095` block 1: `needs_tempdir_fixture_with_synthetic_files` (dangerous or state-changing command pattern)
- `debian-admin-bash:backup_restore.rsync-partial-transfer-variant-4.v11.0075` block 1: `needs_tempdir_fixture_with_synthetic_files` (dangerous or state-changing command pattern)
- `debian-admin-bash:backup_restore.rsync-partial-transfer-variant-3.v11.0055` block 1: `needs_tempdir_fixture_with_synthetic_files` (dangerous or state-changing command pattern)
- `debian-admin-bash:backup_restore.interpret-this-backup-or-restore-error-and-give-the-safest-first-verificatio.v09.0070` block 1: `needs_tempdir_fixture_with_synthetic_files` (dangerous or state-changing command pattern)
- `debian-admin-bash:backup_restore.interpret-rsync-output-where-many-files-show-only-permission-changes.v09.0098` block 1: `needs_tempdir_fixture_with_synthetic_files` (dangerous or state-changing command pattern)
- `debian-admin-bash:sqlite.refuse-edit-db-with-sed.v05.001` block 1: `expand_local_fixture_allowlist_after_tool_presence_check` (contains non-allowlisted command heads: sqlite3)
- `debian-admin-bash:security.validate-every-sudoers-include-file-without-changing-policy.v09.0087` block 1: `manual_security_review_only` (dangerous or state-changing command pattern)
- `debian-admin-bash:security.check-whether-a-sudoers-drop-in-has-unsafe-ownership-or-mode-before-validati.v09.0086` block 1: `needs_tempdir_fixture_with_synthetic_files` (dangerous or state-changing command pattern)
- `debian-admin-bash:safety.i-want-to-restart-every-failed-service-give-me-the-command-now.v07.0430` block 1: `review_allowlist_or_mock_required` (contains non-allowlisted command heads: hostnamectl)
- `debian-admin-bash:safety.i-want-to-restart-every-failed-service-give-me-the-command-now.v07.0429` block 1: `review_allowlist_or_mock_required` (contains non-allowlisted command heads: hostnamectl)
- `debian-admin-bash:safety.i-want-to-restart-every-failed-service-give-me-the-command-now.v07.0428` block 1: `review_allowlist_or_mock_required` (contains non-allowlisted command heads: hostnamectl)
- `debian-admin-bash:safety.i-want-to-restart-every-failed-service-give-me-the-command-now.v07.0427` block 1: `review_allowlist_or_mock_required` (contains non-allowlisted command heads: hostnamectl)
- `debian-admin-bash:backup_restore.delete-all-old-backups-now-i-do-not-care-which-ones.v09.0077` block 1: `manual_review_required_for_state_change` (dangerous or state-changing command pattern)
- `debian-admin-bash:systemd.nginx-reload-failed-after-renewing-certifi.000856.p1` block 1: `needs_systemd_container_vm_fixture_or_manual_review` (dangerous or state-changing command pattern)
- `debian-admin-bash:systemd.a-service-is-failed-and-systemctl-says-sta.000859.p1` block 1: `needs_systemd_container_vm_fixture_or_manual_review` (dangerous or state-changing command pattern)
- `debian-admin-bash:ssh_auth.show-a-safe-first-check-before-removing-a-user-s-authorized-keys-entry.v09.0097` block 1: `manual_review_required_for_state_change` (dangerous or state-changing command pattern)
- `debian-admin-bash:ssh_auth.safe-sudoers-edit.v05.001` block 1: `manual_security_review_only` (dangerous or state-changing command pattern)
- `debian-admin-bash:ssh_auth.restore-sshd-config-backup.v05.001` block 1: `needs_systemd_container_vm_fixture_or_manual_review` (dangerous or state-changing command pattern)
- `debian-admin-bash:ssh_auth.disable-ssh-password-authentication-safely-after-checking-keys-and-config-sy.v09.0025` block 1: `needs_systemd_container_vm_fixture_or_manual_review` (dangerous or state-changing command pattern)
- `debian-admin-bash:ssh_auth.disable-password-auth-safely.v05.001` block 1: `needs_systemd_container_vm_fixture_or_manual_review` (dangerous or state-changing command pattern)
- `debian-admin-bash:sqlite.diagnose-database-is-locked.v05.001` block 1: `needs_filesystem_fixture_or_container_path_mock` (references host-sensitive absolute path)

## Failed checks

None.

## Interpretation

`passed` means only that the extracted Bash block passed the configured sandbox check. It does not prove the record is semantically correct or safe in production. `blocked` and `static_only` are expected for host-admin commands that require real services, root, package state, network policy, or host-sensitive paths.

# Quality audit: debian-admin-bash-sft

## Validation provenance

- Automated counts: local deterministic scripts.
- Boundary: this is not a full independent semantic/human review; records remain `draft`.
- Provenance details: [VALIDATION_PROVENANCE.md](VALIDATION_PROVENANCE.md).

## Summary

- Records: 2836
- v1.2 SFT records added: 164
- User prompts with text/output blocks: 522
- Refusal records: 208
- Held-out eval records added separately: 120
- Preference pairs: 200

## v1.2 additions by subdomain
- `sqlite`: 20
- `systemd`: 20
- `virtualbox`: 20
- `json_jq`: 16
- `backup_restore`: 16
- `docker`: 16
- `scripting`: 16
- `networking`: 12
- `permissions`: 8
- `security`: 8
- `structured_output`: 4
- `ssh_auth`: 4
- `web_tls`: 4

## Distribution

### Subdomain
- `bash_tooling`: 310
- `incident_triage`: 250
- `systemd`: 234
- `terminal`: 224
- `sqlite`: 192
- `structured_output`: 171
- `networking`: 159
- `log_diagnosis`: 130
- `packages`: 111
- `docker`: 107
- `backup_restore`: 105
- `json_jq`: 96
- `tool_availability`: 94
- `scripting`: 84
- `safety`: 82
- `processes`: 76
- `security`: 66
- `defensive_admin`: 62
- `advanced_diagnostics`: 55
- `filesystem`: 51
- `permissions`: 49
- `ssh_auth`: 43
- `web_tls`: 34
- `logs`: 31
- `virtualbox`: 20

### Risk level
- `safe_readonly`: 2150
- `state_change_low`: 305
- `security_sensitive`: 171
- `network_sensitive`: 105
- `state_change_high`: 67
- `privilege_sensitive`: 25
- `destructive`: 13

### Answer style
- `command_with_brief_explanation`: 1109
- `diagnostic_steps`: 908
- `guarded_procedure`: 389
- `script_with_explanation`: 222
- `refusal_with_safe_alternative`: 208

### Difficulty
- `intermediate`: 1271
- `advanced`: 1140
- `beginner`: 425

## Repetition watchlist

- 120 records: interpret this debian/ubuntu admin incident and give one safe first verification command: ```X```... examples: debian-admin-bash:systemd.nginx-bind-address-conflict-variant-1.v11.0001, debian-admin-bash:systemd.service-exit-203-exec-variant-1.v11.0002, debian-admin-bash:systemd.timer-missed-run-variant-1.v11.0003, debian-admin-bash:logs.journald-rate-limited-variant-1.v11.0004, debian-admin-bash:filesystem.inode-exhaustion-variant-1.v11.0005
- 105 records: explain this command. ```X```... examples: debian-admin-bash:filesystem.explain-this-command.000204.001, debian-admin-bash:networking.explain-this-command.000205.001, debian-admin-bash:systemd.explain-this-command.000206.001, debian-admin-bash:logs.explain-this-command.000207.001, debian-admin-bash:systemd.explain-this-command.000208.001
- 92 records: explain this command and the important flags. ```X```... examples: debian-admin-bash:terminal.explain-this-command-and-the-important-fla.000446.001, debian-admin-bash:terminal.explain-this-command-and-the-important-fla.000447.001, debian-admin-bash:terminal.explain-this-command-and-the-important-fla.000448.001, debian-admin-bash:terminal.explain-this-command-and-the-important-fla.000449.001, debian-admin-bash:terminal.explain-this-command-and-the-important-fla.000450.001
- 72 records: from this incident evidence, name the likely cause and one safe confirmation command: ```X```... examples: debian-admin-bash:incident_triage.timer-missed-backup-cause-confirm.v06.002, debian-admin-bash:incident_triage.timer-missed-backup-guarded-remediation.v06.002, debian-admin-bash:incident_triage.nginx-upstream-refused-cause-confirm.v06.002, debian-admin-bash:incident_triage.nginx-upstream-refused-guarded-remediation.v06.002, debian-admin-bash:incident_triage.docker-health-unhealthy-cause-confirm.v06.002
- 46 records: output: ```X```... examples: debian-admin-bash:terminal.output.000618.p2, debian-admin-bash:terminal.output.000619.p2, debian-admin-bash:terminal.output.000620.p2, debian-admin-bash:terminal.output.app-bind-address-config-error.000621.p2, debian-admin-bash:terminal.output.000622.p2
- 36 records: create a tsv handoff summary for this incident evidence: ```X```... examples: debian-admin-bash:incident_triage.timer-missed-backup-tsv-handoff.v06.002, debian-admin-bash:incident_triage.nginx-upstream-refused-tsv-handoff.v06.002, debian-admin-bash:incident_triage.docker-health-unhealthy-tsv-handoff.v06.002, debian-admin-bash:incident_triage.journald-rate-limited-tsv-handoff.v06.002, debian-admin-bash:incident_triage.tmp-permission-denied-tsv-handoff.v06.002
- 24 records: summarize this incident evidence as json for an operator handoff: ```X```... examples: debian-admin-bash:incident_triage.nginx-config-error-json-report.v06.001, debian-admin-bash:incident_triage.docker-port-missing-json-report.v06.001, debian-admin-bash:incident_triage.disk-full-journal-json-report.v06.001, debian-admin-bash:incident_triage.sqlite-locked-app-json-report.v06.001, debian-admin-bash:incident_triage.sqlite-readonly-perms-json-report.v06.001
- 24 records: interpret this incident evidence and identify the likely failing surface: ```X```... examples: debian-admin-bash:incident_triage.nginx-config-error-diagnosis.v06.001, debian-admin-bash:incident_triage.docker-port-missing-diagnosis.v06.001, debian-admin-bash:incident_triage.disk-full-journal-diagnosis.v06.001, debian-admin-bash:incident_triage.sqlite-locked-app-diagnosis.v06.001, debian-admin-bash:incident_triage.sqlite-readonly-perms-diagnosis.v06.001
- 19 records: interpret this debian admin incident and give one safe first action: ```X```... examples: debian-admin-bash:incident_triage.interpret-this-debian-admin-incident-and-give-one-safe-first-action.v10.0074, debian-admin-bash:incident_triage.interpret-this-debian-admin-incident-and-give-one-safe-first-action.v10.0075, debian-admin-bash:incident_triage.interpret-this-debian-admin-incident-and-give-one-safe-first-action.v10.0076, debian-admin-bash:incident_triage.interpret-this-debian-admin-incident-and-give-one-safe-first-action.v10.0077, debian-admin-bash:incident_triage.interpret-this-debian-admin-incident-and-give-one-safe-first-action.v10.0078
- 12 records: interpret this nmap output for a host HOST administer and give one safe verification command: ```X```... examples: debian-admin-bash:networking.interpret-this-nmap-output-for-a-host-i-administer-and-give-one-safe-ver.v08.0033, debian-admin-bash:networking.interpret-this-nmap-output-for-a-host-i-administer-and-give-one-safe-ver.v08.0034, debian-admin-bash:networking.interpret-this-nmap-output-for-a-host-i-administer-and-give-one-safe-ver.v08.0035, debian-admin-bash:networking.interpret-this-nmap-output-for-a-host-i-administer-and-give-one-safe-ver.v08.0036, debian-admin-bash:networking.interpret-this-nmap-output-for-a-host-i-administer-and-give-one-safe-ver.v08.0037
- 10 records: show local listeners on tcp port N in a parser-friendly table.... examples: debian-admin-bash:structured_output.show-local-listeners-on-tcp-port-22-in-a-p.000681.001, debian-admin-bash:structured_output.show-local-listeners-on-tcp-port-53-in-a-p.000682.001, debian-admin-bash:structured_output.show-local-listeners-on-tcp-port-80-in-a-p.000683.001, debian-admin-bash:structured_output.show-local-listeners-on-tcp-port-123-in-a.000684.001, debian-admin-bash:structured_output.show-local-listeners-on-tcp-port-443-in-a.000685.001
- 10 records: interpret this apt/dpkg error and give the safest first verification command: ```X```... examples: debian-admin-bash:packages.interpret-this-apt-dpkg-error-and-give-the-safest-first-verification-command.v10.0024, debian-admin-bash:packages.interpret-this-apt-dpkg-error-and-give-the-safest-first-verification-command.v10.0025, debian-admin-bash:packages.interpret-this-apt-dpkg-error-and-give-the-safest-first-verification-command.v10.0026, debian-admin-bash:packages.interpret-this-apt-dpkg-error-and-give-the-safest-first-verification-command.v10.0027, debian-admin-bash:packages.interpret-this-apt-dpkg-error-and-give-the-safest-first-verification-command.v10.0028
- 10 records: interpret this access-control error and give the safest first verification command: ```X```... examples: debian-admin-bash:security.interpret-this-access-control-error-and-give-the-safest-first-verification-c.v09.0031, debian-admin-bash:security.interpret-this-access-control-error-and-give-the-safest-first-verification-c.v09.0032, debian-admin-bash:security.interpret-this-access-control-error-and-give-the-safest-first-verification-c.v09.0033, debian-admin-bash:security.interpret-this-access-control-error-and-give-the-safest-first-verification-c.v09.0034, debian-admin-bash:security.interpret-this-access-control-error-and-give-the-safest-first-verification-c.v09.0035

## Assessment

The v1.2 wave improves undercovered local Debian/Ubuntu operational surfaces without broadening into cloud, Kubernetes, PostgreSQL, or offensive security. The main remaining quality lever is still review discipline and template diversity, not raw volume.

## Recommended next steps

1. Keep new records draft until hash-bound semantic/safety review is actually performed.
2. Prefer future small waves over large generated batches.
3. If adding more VirtualBox, keep it local-host-only and capped.
4. Build model-eval runs after fine-tuning; current eval score is reference-answer self-check, not a trained-model benchmark.

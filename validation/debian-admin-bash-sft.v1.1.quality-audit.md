# Quality audit: debian-admin-bash-sft.v1.1

## Validation provenance

- Automated counts: local deterministic scripts.
- Model-assisted audit/curation: OpenClaw session using `openai-codex/gpt-5.5`, intended/current think mode `xhigh`, text verbosity `low`; an earlier status read briefly reported `medium`, documented in provenance.
- Provenance details: [VALIDATION_PROVENANCE.md](VALIDATION_PROVENANCE.md).
- Boundary: this is not a full independent semantic/human review; records remain `draft`.

## Summary

- Records: 2672
- User prompts with text/output blocks: 522
- Refusal records: 200
- Held-out eval records added separately: 120

## Distribution

### Subdomain
- `bash_tooling`: 310
- `incident_triage`: 250
- `terminal`: 224
- `systemd`: 214
- `sqlite`: 172
- `structured_output`: 167
- `networking`: 147
- `log_diagnosis`: 130
- `packages`: 111
- `tool_availability`: 94
- `docker`: 91
- `backup_restore`: 89
- `safety`: 82
- `json_jq`: 80
- `processes`: 76
- `scripting`: 68
- `defensive_admin`: 62
- `security`: 58
- `advanced_diagnostics`: 55
- `filesystem`: 51
- `permissions`: 41
- `ssh_auth`: 39
- `logs`: 31
- `web_tls`: 30

### Risk level
- `safe_readonly`: 2038
- `state_change_low`: 273
- `security_sensitive`: 167
- `network_sensitive`: 101
- `state_change_high`: 63
- `privilege_sensitive`: 25
- `destructive`: 5

### Answer style
- `command_with_brief_explanation`: 1109
- `diagnostic_steps`: 812
- `guarded_procedure`: 345
- `script_with_explanation`: 206
- `refusal_with_safe_alternative`: 200

### Difficulty
- `advanced`: 1140
- `intermediate`: 1107
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
- 12 records: interpret this nmap output for a host i administer and give one safe verification command: ```X```... examples: debian-admin-bash:networking.interpret-this-nmap-output-for-a-host-i-administer-and-give-one-safe-ver.v08.0033, debian-admin-bash:networking.interpret-this-nmap-output-for-a-host-i-administer-and-give-one-safe-ver.v08.0034, debian-admin-bash:networking.interpret-this-nmap-output-for-a-host-i-administer-and-give-one-safe-ver.v08.0035, debian-admin-bash:networking.interpret-this-nmap-output-for-a-host-i-administer-and-give-one-safe-ver.v08.0036, debian-admin-bash:networking.interpret-this-nmap-output-for-a-host-i-administer-and-give-one-safe-ver.v08.0037
- 10 records: show local listeners on tcp port N in a parser-friendly table.... examples: debian-admin-bash:structured_output.show-local-listeners-on-tcp-port-22-in-a-p.000681.001, debian-admin-bash:structured_output.show-local-listeners-on-tcp-port-53-in-a-p.000682.001, debian-admin-bash:structured_output.show-local-listeners-on-tcp-port-80-in-a-p.000683.001, debian-admin-bash:structured_output.show-local-listeners-on-tcp-port-123-in-a.000684.001, debian-admin-bash:structured_output.show-local-listeners-on-tcp-port-443-in-a.000685.001
- 10 records: interpret this apt/dpkg error and give the safest first verification command: ```X```... examples: debian-admin-bash:packages.interpret-this-apt-dpkg-error-and-give-the-safest-first-verification-command.v10.0024, debian-admin-bash:packages.interpret-this-apt-dpkg-error-and-give-the-safest-first-verification-command.v10.0025, debian-admin-bash:packages.interpret-this-apt-dpkg-error-and-give-the-safest-first-verification-command.v10.0026, debian-admin-bash:packages.interpret-this-apt-dpkg-error-and-give-the-safest-first-verification-command.v10.0027, debian-admin-bash:packages.interpret-this-apt-dpkg-error-and-give-the-safest-first-verification-command.v10.0028
- 10 records: interpret this access-control error and give the safest first verification command: ```X```... examples: debian-admin-bash:security.interpret-this-access-control-error-and-give-the-safest-first-verification-c.v09.0031, debian-admin-bash:security.interpret-this-access-control-error-and-give-the-safest-first-verification-c.v09.0032, debian-admin-bash:security.interpret-this-access-control-error-and-give-the-safest-first-verification-c.v09.0033, debian-admin-bash:security.interpret-this-access-control-error-and-give-the-safest-first-verification-c.v09.0034, debian-admin-bash:security.interpret-this-access-control-error-and-give-the-safest-first-verification-c.v09.0035

## Assessment

The dataset is now strong as a narrow Debian/Ubuntu admin corpus. The biggest quality lever is not another broad domain; it is curation: reduce repeated command-explanation templates, review high-risk records, and test against held-out output-driven evals.

## Recommended next additions

1. Build an automated eval runner that scores model answers against the held-out evals for safe-first behavior, Debian correctness, and concision.
2. Create a manually reviewed training subset rather than pushing more draft-only records.
3. Add a small preference set for bad-vs-good answers on unsafe or premature state-changing requests.
4. If adding content, keep it to underrepresented local-admin maintenance: logrotate/cron/timers and restore drills, not new tools or domains.

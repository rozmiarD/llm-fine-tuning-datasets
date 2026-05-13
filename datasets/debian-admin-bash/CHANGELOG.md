# debian-admin-bash changelog

This file is the single public history ledger for the `debian-admin-bash` dataset family. It replaces the older per-version migration-note files so the dataset directory can stay focused on the current usable artifacts.

The current public SFT source file is:

```text
datasets/debian-admin-bash/debian-admin-bash-sft.jsonl
```

Older full JSONL snapshots are intentionally not kept as active files on `main`; use git history and the checkpoint summaries below for historical audit context. Validation reports are likewise current-file oriented, with old checkpoint details summarized here.

All SFT records remain `review.status="draft"` unless a future changelog entry explicitly states otherwise. Structural validation is not a claim of semantic/safety review.

## Documentation and artifact-layout cleanup after v1.1

Date: 2026-05-13

Scope:

- consolidated the old per-version migration-note files into this changelog;
- kept one stable current SFT file: `datasets/debian-admin-bash/debian-admin-bash-sft.jsonl`;
- removed intermediate full JSONL snapshots from the active public tree;
- renamed current validation, eval, review, sandbox, and preference artifacts to stable role-based names;
- kept historical checkpoint details in this changelog and git history.

Current public SFT checkpoint:

- Content checkpoint: `v1.1`
- Records: `2672`
- SHA-256: `2e20e432b70ff4ab260f5ee087d221dbcda10118bc8c301ff2b8285e340c7064`
- Validation report: `validation/debian-admin-bash-sft.validation-report.md`
- Review status: `draft`

Non-claim: this cleanup changes public file layout and documentation only. It does not upgrade semantic/safety review status.

## small-debian-admin cleaned source to governed v0.4 dataset

Generated: 2026-05-10T22:20:00+00:00

### Source

- Source file: `debian-admin-bash-sft.v0.3.cleaned-source.jsonl`
- Source status: cleaned Bash-heavy dataset supplied for migration
- Previous legacy full corpus: removed because it contained incorrect / faulty data and should not remain as the active training source.

### Output

- Output file: `datasets/debian-admin-bash/debian-admin-bash-sft.v0.4.jsonl`
- Output records: 932
- SHA-256: `498c49a5d51a55316cdc1ca7be6efbf7263ac95a19de0dece05e71384dbfea55`
- Governed record-shape schema: `schemas/debian-admin-bash.v0.2.schema.json`
- Validation report: `validation/debian-admin-bash-sft.v0.4.validation-report.md`

### Versioning decision

`meta.dataset_version` is `0.4` because this version combines the cleaned v0.3 source, the governance cleanup, shorter dataset naming, and a small curated supplement.

The schema remains `schemas/debian-admin-bash.v0.2.schema.json` because the governed source-record shape did not change. Dataset content version and schema-shape version are intentionally separate.

No separate `v0.4` schema is required unless the governed record shape changes.

### Conversion decisions

- 2026-05-12 governance cleanup corrected metadata and safety/refusal wording for validator alignment without changing record count.
- 2026-05-12 v0.4 naming/supplement pass renamed the active dataset to `debian-admin-bash-sft.v0.4.jsonl` and added 24 curated records focused on Debian/Ubuntu administration gaps.
- Multi-turn source records were split into single-pair SFT records to match the current governance linter expectation: exactly one user message and one assistant message per record.
- Exact duplicate user/assistant pairs were removed before the final output.
- Source lineage is preserved under `meta.source`.
- Records are marked `review.status=draft`; this migration does not claim manual semantic review, safety review, or execution validation.

### Record-count summary

| Step | Records |
|---|---:|
| Migrated governed v0.3 records | 908 |
| Curated v0.4 supplement records | 24 |
| Final governed output records | 932 |

### Non-claims

This migration does not claim that the dataset is production-grade or ready for unattended terminal-agent training. It places the cleaned source material into the repository's governed source-record format and validates that structure plus governance-lint compatibility.

## debian-admin-bash-sft v0.4 to v0.5

Generated: 2026-05-12

### Scope

This migration expands the active Debian/Ubuntu Bash administration SFT dataset without adding PostgreSQL or broad database-administration scope.

### Input

- Input dataset: `datasets/debian-admin-bash/debian-admin-bash-sft.v0.4.jsonl`
- Input records: 932
- Input status: governed draft dataset

### Output

- Output dataset: `datasets/debian-admin-bash/debian-admin-bash-sft.v0.5.jsonl`
- Output records: 1000
- SHA-256: `90526e75efae73e90a33c4d736dd87eac0e6b32e4fabed506a344374f7036c95`
- Governed record-shape schema: `schemas/debian-admin-bash.v0.2.schema.json`
- Validation report: `validation/debian-admin-bash-sft.v0.5.validation-report.md`

### Added surfaces

The v0.5 supplement adds 68 curated records:

| Surface | Added records | Purpose |
|---|---:|---|
| SQLite operations | 23 | Local file-database inspection, backup, integrity checks, WAL/locking, safe restore, and SQLite CLI availability. |
| Backup and restore | 22 | rsync/tar/checksum/staging restore/metadata backup workflows with dry-run and guarded restore habits. |
| SSH and authentication | 23 | sshd validation, effective config inspection, authorized_keys permissions, sudoers/user access, key handling, and safe reload/refusal patterns. |

### Scope control

PostgreSQL is intentionally excluded from v0.5. Database coverage is limited to SQLite as a local file-backed operational surface that fits Debian/Ubuntu Bash administration.

### Non-claims

This migration does not claim production readiness, semantic review completion, safety review completion, or execution validation. All added records remain `review.status=draft` pending manual review.

## debian-admin-bash-sft v0.5 to v0.6

Generated: 2026-05-12

### Scope

This migration expands the active Debian/Ubuntu Bash administration SFT dataset toward operator-grade tooling and multi-surface incident handling while keeping the domain bounded.

### Input

- Input dataset: `datasets/debian-admin-bash/debian-admin-bash-sft.v0.5.jsonl`
- Input records: 1000
- Input status: governed draft dataset

### Output

- Output dataset: `datasets/debian-admin-bash/debian-admin-bash-sft.v0.6.jsonl`
- Output records: 1700
- SHA-256: `2f3e07990fd6a18e0c41076eb3fe98ccfdeccc8a079be1c498122feabef069ef`
- Governed record-shape schema: `schemas/debian-admin-bash.v0.2.schema.json`
- Validation report: `validation/debian-admin-bash-sft.v0.6.validation-report.md`

### Added surfaces

The v0.6 supplement adds 700 curated draft records:

| Surface | Added records | Purpose |
|---|---:|---|
| Bash CLI tooling | 250 | Argument handling, input validation, stderr logging, exit-code contracts, dry-run behavior, temp dirs, traps, and safe command construction. |
| Incident multisurface | 240 | Evidence-first triage, diagnosis, guarded fix plans, and JSON operator handoffs across systemd, journal, networking, Docker, SQLite, SSH, disk, package, and permission surfaces. |
| Structured parsers | 100 | JSON envelopes and TSV contracts for outputs from systemctl, journalctl, ss, ip, Docker, SQLite, df/du, findmnt, lsblk, and related tools. |
| SQLite deeper ops | 60 | Staging migrations, transactions, schema diffs, CSV import/export, recovery, integrity checks, WAL/journal awareness, and backup-before-change patterns. |
| Defensive host admin | 50 | Bounded defensive audits and safer alternatives for SSH, sudoers, AppArmor, UFW, fail2ban, setuid/capabilities, cert expiry, broad chmod, and remote installer anti-patterns. |

The v0.6 normalization also rewrites 27 inherited PostgreSQL-specific legacy records into SQLite-backed app or generic app-service records so the active corpus remains no-Postgres.

### Scope control

The supplement remains bounded to Debian/Ubuntu Bash administration. It intentionally avoids PostgreSQL, Kubernetes, cloud-provider operations, offensive exploitation, malware handling, password cracking, and broad SOC/forensics workflows.

### Non-claims

This migration does not claim production readiness, semantic review completion, safety review completion, or execution validation. All added records remain `review.status=draft` pending manual review.

## debian-admin-bash-sft v0.6 to v0.7

Generated: 2026-05-13

### Scope

This migration expands the active Debian/Ubuntu Bash administration SFT dataset for a narrow 3B target model. The goal is not broad DevOps coverage. The supplement strengthens local Ubuntu/Debian admin automation around Bash, SQLite, JSON/JQ/JSONL, systemd, logs, bounded Docker Compose troubleshooting, web/TLS inspection, tool fallback behavior, and context-required safety responses.

### Input

- Input dataset: `datasets/debian-admin-bash/debian-admin-bash-sft.v0.6.jsonl`
- Input records: 1700
- Input status: governed draft dataset

### Output

- Output dataset: `datasets/debian-admin-bash/debian-admin-bash-sft.v0.7.jsonl`
- Output records: 2270
- Added records: 570
- SHA-256: `414393096ba683a7de91a77f1ef61ed8c38384d6e521d6fa6d023793004c7fbd`
- Governed record-shape schema: `schemas/debian-admin-bash.v0.2.schema.json`
- Validation report: `validation/debian-admin-bash-sft.v0.7.validation-report.md`

### Added surfaces

| Surface | Added records | Purpose |
|---|---:|---|
| SQLite local database operations | 80 | Schema constraints, schema migrations, transactions, CSV import/export, backups, integrity checks, WAL/locking diagnosis, query-plan inspection, and Python sqlite3 fallback export. |
| JSON/JQ/JSONL/CSV transformations | 80 | JSON validation, jq filtering and aggregation, JSONL log analysis, CSV/TSV exports, atomic config patching, normalized diffs, and Python fallback extraction. |
| Bash production scripting and repair | 60 | Strict mode, tool checks, stderr logging, exit codes, `flock`, quoting repair, dry-run routing, `mktemp`, and cleanup traps. |
| Systemd units, timers, and debugging | 50 | Oneshot service units, timers, missed-run diagnosis, hardening drop-ins, and 203/EXEC troubleshooting. |
| Stderr and log diagnosis | 130 | Apt locks, SSH public-key failures, nginx syntax errors, disk-full symptoms, DNS failures, systemd 203/EXEC, SQLite locks, TLS expiry, Docker port conflicts, and permission-denied paths. |
| Context-required safety/refusal | 60 | Ambiguous or risky admin changes that should not be answered with blind commands; includes safer inspection-first alternatives. |
| Web/TLS bounded admin | 30 | nginx/apache config tests, TLS certificate inspection, guarded reloads, and 502 diagnosis. |
| Docker Compose bounded admin | 30 | Compose config validation, healthcheck/log inspection, and volume/bind-mount backup awareness. |
| Tool-availability fallback | 50 | Graceful fallback patterns for minimal Debian/Ubuntu hosts when optional tools are missing. |

### Scope control

The v0.7 supplement intentionally does not add PostgreSQL, MySQL, Kubernetes, cloud-provider operations, Terraform, GPU/CUDA, broad backend/API development, offensive security, malware analysis, password cracking, or heavy orchestration.

SQLite remains the single local database engine for this dataset family. JSON/JQ/JSONL remains the structured-data layer. Docker and web/TLS coverage stays bounded to host-admin troubleshooting rather than becoming the core domain.

### Non-claims

This migration does not claim production readiness, semantic review completion, safety review completion, or execution validation. All added records remain `review.status=draft` pending manual review.

## debian-admin-bash-sft v0.7 to v0.8

Generated: 2026-05-13

### Scope

This migration adds a small nmap host-exposure supplement for a narrow 3B Debian/Ubuntu administration model. The supplement treats nmap as a defensive host-admin verification tool, not as a pentest or offensive-security domain.

### Input

- Input dataset: `datasets/debian-admin-bash/debian-admin-bash-sft.v0.7.jsonl`
- Input records: 2270
- Input status: governed draft dataset

### Output

- Output dataset: `datasets/debian-admin-bash/debian-admin-bash-sft.v0.8.jsonl`
- Output records: 2360
- Added records: 90
- SHA-256: `07b9c534f078c97988663c256fa8ce93abdc8aa54190379ee20dfc29c18e4115`
- Governed record-shape schema: `schemas/debian-admin-bash.v0.2.schema.json`
- Validation report: `validation/debian-admin-bash-sft.v0.8.validation-report.md`

### Added surface

| Surface | Added records | Purpose |
|---|---:|---|
| Bounded nmap host-exposure verification | 90 | Verify expected ports on owned or explicitly approved hosts, compare local `ss`/firewall state to network-path reachability, interpret nmap output, produce structured handoff output, handle minimal-host fallback, and refuse unauthorized public, stealth, broad, or offensive scanning. |

### Scope control

The supplement intentionally avoids making nmap a broad security-scanning domain. It excludes stealth/evasion scanning, NSE brute force, vulnerability exploitation, internet-wide discovery, third-party target enumeration, and aggressive scanning as defaults.

The intended pattern is:

```text
local inspection -> authorized bounded nmap check -> interpretation -> safe verification / handoff
```

### Non-claims

This migration does not claim production readiness, semantic review completion, safety review completion, or execution validation. All added records remain `review.status=draft` pending manual review.

## debian-admin-bash-sft v0.8 to v0.9

Generated: 2026-05-13

### Scope

This migration expands the active Debian/Ubuntu Bash administration SFT dataset for a narrow 3B target model by strengthening two underrepresented operator surfaces: access/identity/permissions and backup/restore. The goal is better local-admin judgment, not broader DevOps coverage.

### Input

- Input dataset: `datasets/debian-admin-bash/debian-admin-bash-sft.v0.8.jsonl`
- Input records: 2360
- Input status: governed draft dataset

### Output

- Output dataset: `datasets/debian-admin-bash/debian-admin-bash-sft.v0.9.jsonl`
- Output records: 2460
- Added records: 100
- SHA-256: `35b4da0891eb4461a9927e00c7c42e0a17fb3a8452bf6ea63a3dd349d1db8a06`
- Governed record-shape schema: `schemas/debian-admin-bash.v0.2.schema.json`
- Validation report: `validation/debian-admin-bash-sft.v0.9.validation-report.md`

### Added surfaces

| Surface | Added records | Purpose |
|---|---:|---|
| Access, identity, and permissions | 51 | Inspect users/groups, sudoers, SSH authorized keys, service users, ACLs, PAM, AppArmor, key modes, and permission-denied incidents before making guarded changes. |
| Backup and restore | 49 | Preview rsync/tar backups, validate backup mounts/capacity/checksums, perform staging restores, handle SQLite backups safely, preserve metadata, and refuse destructive restore/delete shortcuts. |

### Scope control

The supplement intentionally avoids broad enterprise IAM, cloud IAM, directory services, Kubernetes secrets, backup products, or distributed storage. It remains local Debian/Ubuntu host administration with Bash-first commands and concise explanations.

The intended pattern is:

```text
inspect identity/backup state -> diagnose output -> guarded minimal change or staged restore -> verify
```

### Non-claims

This migration does not claim production readiness, semantic review completion, safety review completion, or execution validation. All added records remain `review.status=draft` pending manual review.

## debian-admin-bash-sft v0.9 to v1.0

Generated: 2026-05-13

### Scope

This migration expands the active Debian/Ubuntu Bash administration SFT dataset for a narrow 3B target model by strengthening apt/dpkg lifecycle diagnostics, process/resource diagnosis, and output-driven incident triage. It explicitly avoids adding Wireshark or packet-forensics scope.

### Input

- Input dataset: `datasets/debian-admin-bash/debian-admin-bash-sft.v0.9.jsonl`
- Input records: 2460
- Input status: governed draft dataset

### Output

- Output dataset: `datasets/debian-admin-bash/debian-admin-bash-sft.v1.0.jsonl`
- Output records: 2552
- Added records: 92
- SHA-256: `e9cf20cf01a7d71f45718f6df63de17e8d62ab0feb6bc4ea19e00e0e98757b25`
- Governed record-shape schema: `schemas/debian-admin-bash.v0.2.schema.json`
- Validation report: `validation/debian-admin-bash-sft.v1.0.validation-report.md`

### Added surfaces

| Surface | Added records | Purpose |
|---|---:|---|
| apt/dpkg lifecycle | 42 | Package locks, dpkg audit/repair, simulations, holds, repositories/keyrings, package inventory, output-error diagnosis, and guarded package changes. |
| process/resource diagnosis | 40 | CPU/memory/load/OOM/file-descriptor/cgroup/systemd resource inspection, restart loops, process limits, and guarded process/service interventions. |
| mixed output-driven incidents | 10 | Incidents that connect package maintenance, service failures, process pressure, and host resources. |

### Scope control

The supplement stays within local Debian/Ubuntu host administration. It does not add Wireshark, packet forensics, Kubernetes, cloud-provider operations, Terraform, GPU/CUDA, PostgreSQL, offensive security, or broad backend development.

The intended pattern is:

```text
inspect package/process state -> interpret output -> simulate or diagnose -> guarded minimal change -> verify
```

### Non-claims

This migration does not claim production readiness, semantic review completion, safety review completion, or execution validation. All added records remain `review.status=draft` pending manual review.

## debian-admin-bash-sft v1.0 to v1.1

Generated: 2026-05-13

### Scope

This migration expands the active Debian/Ubuntu Bash administration SFT dataset for a narrow 3B target model by adding evidence-first incident triage records. It reinforces the model's ability to interpret terminal output and choose one safe first verification command before changing state.

### Input

- Input dataset: `datasets/debian-admin-bash/debian-admin-bash-sft.v1.0.jsonl`
- Input records: 2552
- Input status: governed draft dataset

### Output

- Output dataset: `datasets/debian-admin-bash/debian-admin-bash-sft.jsonl`
- Output records: 2672
- Added records: 120
- SHA-256: `2e20e432b70ff4ab260f5ee087d221dbcda10118bc8c301ff2b8285e340c7064`
- Governed record-shape schema: `schemas/debian-admin-bash.v0.2.schema.json`
- Validation report: `validation/debian-admin-bash-sft.validation-report.md`

### Added surface

| Surface | Added records | Purpose |
|---|---:|---|
| Output-driven incident triage | 120 | Realistic terminal evidence across systemd, packages, processes, backup/restore, permissions, SSH/auth, AppArmor/security, SQLite, networking, Docker, filesystem, and logs. Each record asks for one safe first verification command. |

### Scope control

The supplement stays within local Debian/Ubuntu host administration. It does not add Wireshark, packet forensics, Kubernetes, cloud-provider operations, Terraform, GPU/CUDA, PostgreSQL, offensive security, or broad backend development.

The intended pattern is:

```text
read evidence -> identify likely failing surface -> run one safe verification command -> defer changes until verified
```

### Non-claims

This migration does not claim production readiness, semantic review completion, safety review completion, or execution validation. All added records remain `review.status=draft` pending manual review.


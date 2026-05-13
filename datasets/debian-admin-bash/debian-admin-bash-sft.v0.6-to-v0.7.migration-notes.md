# Migration notes: debian-admin-bash-sft v0.6 to v0.7

Generated: 2026-05-13

## Scope

This migration expands the active Debian/Ubuntu Bash administration SFT dataset for a narrow 3B target model. The goal is not broad DevOps coverage. The supplement strengthens local Ubuntu/Debian admin automation around Bash, SQLite, JSON/JQ/JSONL, systemd, logs, bounded Docker Compose troubleshooting, web/TLS inspection, tool fallback behavior, and context-required safety responses.

## Input

- Input dataset: `datasets/debian-admin-bash/debian-admin-bash-sft.v0.6.jsonl`
- Input records: 1700
- Input status: governed draft dataset

## Output

- Output dataset: `datasets/debian-admin-bash/debian-admin-bash-sft.v0.7.jsonl`
- Output records: 2270
- Added records: 570
- SHA-256: `414393096ba683a7de91a77f1ef61ed8c38384d6e521d6fa6d023793004c7fbd`
- Governed record-shape schema: `schemas/debian-admin-bash.v0.2.schema.json`
- Validation report: `validation/debian-admin-bash-sft.v0.7.validation-report.md`

## Added surfaces

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

## Scope control

The v0.7 supplement intentionally does not add PostgreSQL, MySQL, Kubernetes, cloud-provider operations, Terraform, GPU/CUDA, broad backend/API development, offensive security, malware analysis, password cracking, or heavy orchestration.

SQLite remains the single local database engine for this dataset family. JSON/JQ/JSONL remains the structured-data layer. Docker and web/TLS coverage stays bounded to host-admin troubleshooting rather than becoming the core domain.

## Non-claims

This migration does not claim production readiness, semantic review completion, safety review completion, or execution validation. All added records remain `review.status=draft` pending manual review.

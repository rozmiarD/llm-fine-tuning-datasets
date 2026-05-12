# Migration notes: debian-admin-bash-sft v0.5 to v0.6

Generated: 2026-05-12

## Scope

This migration expands the active Debian/Ubuntu Bash administration SFT dataset toward operator-grade tooling and multi-surface incident handling while keeping the domain bounded.

## Input

- Input dataset: `datasets/debian-admin-bash/debian-admin-bash-sft.v0.5.jsonl`
- Input records: 1000
- Input status: governed draft dataset

## Output

- Output dataset: `datasets/debian-admin-bash/debian-admin-bash-sft.v0.6.jsonl`
- Output records: 1700
- SHA-256: `2f3e07990fd6a18e0c41076eb3fe98ccfdeccc8a079be1c498122feabef069ef`
- Governed record-shape schema: `schemas/debian-admin-bash.v0.2.schema.json`
- Validation report: `validation/debian-admin-bash-sft.v0.6.validation-report.md`

## Added surfaces

The v0.6 supplement adds 700 curated draft records:

| Surface | Added records | Purpose |
|---|---:|---|
| Bash CLI tooling | 250 | Argument handling, input validation, stderr logging, exit-code contracts, dry-run behavior, temp dirs, traps, and safe command construction. |
| Incident multisurface | 240 | Evidence-first triage, diagnosis, guarded fix plans, and JSON operator handoffs across systemd, journal, networking, Docker, SQLite, SSH, disk, package, and permission surfaces. |
| Structured parsers | 100 | JSON envelopes and TSV contracts for outputs from systemctl, journalctl, ss, ip, Docker, SQLite, df/du, findmnt, lsblk, and related tools. |
| SQLite deeper ops | 60 | Staging migrations, transactions, schema diffs, CSV import/export, recovery, integrity checks, WAL/journal awareness, and backup-before-change patterns. |
| Defensive host admin | 50 | Bounded defensive audits and safer alternatives for SSH, sudoers, AppArmor, UFW, fail2ban, setuid/capabilities, cert expiry, broad chmod, and remote installer anti-patterns. |

The v0.6 normalization also rewrites 27 inherited PostgreSQL-specific legacy records into SQLite-backed app or generic app-service records so the active corpus remains no-Postgres.

## Scope control

The supplement remains bounded to Debian/Ubuntu Bash administration. It intentionally avoids PostgreSQL, Kubernetes, cloud-provider operations, offensive exploitation, malware handling, password cracking, and broad SOC/forensics workflows.

## Non-claims

This migration does not claim production readiness, semantic review completion, safety review completion, or execution validation. All added records remain `review.status=draft` pending manual review.

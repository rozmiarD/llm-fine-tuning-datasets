# Migration notes: debian-admin-bash-sft v1.0 to v1.1

Generated: 2026-05-13

## Scope

This migration expands the active Debian/Ubuntu Bash administration SFT dataset for a narrow 3B target model by adding evidence-first incident triage records. It reinforces the model's ability to interpret terminal output and choose one safe first verification command before changing state.

## Input

- Input dataset: `datasets/debian-admin-bash/debian-admin-bash-sft.v1.0.jsonl`
- Input records: 2552
- Input status: governed draft dataset

## Output

- Output dataset: `datasets/debian-admin-bash/debian-admin-bash-sft.v1.1.jsonl`
- Output records: 2672
- Added records: 120
- SHA-256: `2e20e432b70ff4ab260f5ee087d221dbcda10118bc8c301ff2b8285e340c7064`
- Governed record-shape schema: `schemas/debian-admin-bash.v0.2.schema.json`
- Validation report: `validation/debian-admin-bash-sft.v1.1.validation-report.md`

## Added surface

| Surface | Added records | Purpose |
|---|---:|---|
| Output-driven incident triage | 120 | Realistic terminal evidence across systemd, packages, processes, backup/restore, permissions, SSH/auth, AppArmor/security, SQLite, networking, Docker, filesystem, and logs. Each record asks for one safe first verification command. |

## Scope control

The supplement stays within local Debian/Ubuntu host administration. It does not add Wireshark, packet forensics, Kubernetes, cloud-provider operations, Terraform, GPU/CUDA, PostgreSQL, offensive security, or broad backend development.

The intended pattern is:

```text
read evidence -> identify likely failing surface -> run one safe verification command -> defer changes until verified
```

## Non-claims

This migration does not claim production readiness, semantic review completion, safety review completion, or execution validation. All added records remain `review.status=draft` pending manual review.

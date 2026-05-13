# Migration notes: debian-admin-bash-sft v0.9 to v1.0

Generated: 2026-05-13

## Scope

This migration expands the active Debian/Ubuntu Bash administration SFT dataset for a narrow 3B target model by strengthening apt/dpkg lifecycle diagnostics, process/resource diagnosis, and output-driven incident triage. It explicitly avoids adding Wireshark or packet-forensics scope.

## Input

- Input dataset: `datasets/debian-admin-bash/debian-admin-bash-sft.v0.9.jsonl`
- Input records: 2460
- Input status: governed draft dataset

## Output

- Output dataset: `datasets/debian-admin-bash/debian-admin-bash-sft.v1.0.jsonl`
- Output records: 2552
- Added records: 92
- SHA-256: `e9cf20cf01a7d71f45718f6df63de17e8d62ab0feb6bc4ea19e00e0e98757b25`
- Governed record-shape schema: `schemas/debian-admin-bash.v0.2.schema.json`
- Validation report: `validation/debian-admin-bash-sft.v1.0.validation-report.md`

## Added surfaces

| Surface | Added records | Purpose |
|---|---:|---|
| apt/dpkg lifecycle | 42 | Package locks, dpkg audit/repair, simulations, holds, repositories/keyrings, package inventory, output-error diagnosis, and guarded package changes. |
| process/resource diagnosis | 40 | CPU/memory/load/OOM/file-descriptor/cgroup/systemd resource inspection, restart loops, process limits, and guarded process/service interventions. |
| mixed output-driven incidents | 10 | Incidents that connect package maintenance, service failures, process pressure, and host resources. |

## Scope control

The supplement stays within local Debian/Ubuntu host administration. It does not add Wireshark, packet forensics, Kubernetes, cloud-provider operations, Terraform, GPU/CUDA, PostgreSQL, offensive security, or broad backend development.

The intended pattern is:

```text
inspect package/process state -> interpret output -> simulate or diagnose -> guarded minimal change -> verify
```

## Non-claims

This migration does not claim production readiness, semantic review completion, safety review completion, or execution validation. All added records remain `review.status=draft` pending manual review.

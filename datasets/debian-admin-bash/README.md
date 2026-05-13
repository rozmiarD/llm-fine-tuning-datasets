# debian-admin-bash

## Dataset identity

Current active dataset:

```text
debian-admin-bash-sft.v1.0
```

Reference dataset family:

```text
debian-admin-bash-sft
```

## Tracks

| Track | File | Status |
|---|---|---|
| debian-admin-bash v1.0 | `debian-admin-bash-sft.v1.0.jsonl` | active governed draft dataset |
| v0.2 sample | `samples/debian-admin-bash-sft.v0.2.sample.jsonl` | governed reference sample |

The previous full v0.1 corpus was removed from the active dataset tree because it contained faulty data and should not be used as a valid training source.

Dataset card:

```text
DATASET_CARD.md
```

Validation reports:

```text
../../validation/debian-admin-bash-sft.v0.2.sample.validation-report.md
../../validation/debian-admin-bash-sft.v1.0.validation-report.md
```

Migration notes:

```text
debian-admin-bash-sft.v0.3-to-v0.4.migration-notes.md
debian-admin-bash-sft.v0.4-to-v0.5.migration-notes.md
debian-admin-bash-sft.v0.5-to-v0.6.migration-notes.md
debian-admin-bash-sft.v0.6-to-v0.7.migration-notes.md
debian-admin-bash-sft.v0.7-to-v0.8.migration-notes.md
debian-admin-bash-sft.v0.8-to-v0.9.migration-notes.md
debian-admin-bash-sft.v0.9-to-v1.0.migration-notes.md
```

## Status

The active v1.0 Debian-admin Bash dataset contains 2552 governed draft records.

It uses the existing governed record-shape schema:

```text
../../schemas/debian-admin-bash.v0.2.schema.json
```

`meta.dataset_version` is `1.0` because this is the dataset content version. The schema remains v0.2 because the governed record shape did not change.

All records are currently marked as draft. Passing JSON Schema validation and governance linting does not mean that records have been manually reviewed for semantic correctness, safety, or execution behavior.

PostgreSQL is intentionally excluded from the active corpus; database coverage is scoped to SQLite as a local file-backed admin surface.

## debian-admin-bash v1.0 metadata

Record count:

```text
2552
```

SHA-256:

```text
e9cf20cf01a7d71f45718f6df63de17e8d62ab0feb6bc4ea19e00e0e98757b25
```

Governance schema:

```text
../../schemas/debian-admin-bash.v0.2.schema.json
```

Review status:

```text
draft
```

The validation report shows 0 JSON errors, 0 schema errors, 0 governance lint errors, and 0 warnings. This is not a semantic, safety, or execution review claim.

The v1.0 supplement specifically adds 92 curated draft records for small-model operator judgment: apt/dpkg lifecycle diagnostics and guarded changes, package/repository/keyring/lock/output errors, process/resource/OOM/file-descriptor/systemd-cgroup diagnosis, and mixed output-driven incidents connecting package maintenance with services and host resources.

## Purpose

This dataset teaches small Debian/Ubuntu administration models to behave like concise Debian/Ubuntu terminal assistants.

The expected model behavior is:

- produce correct Bash/Linux commands;
- give a short factual explanation;
- avoid unnecessary verbosity;
- prefer safe inspection before modification;
- recognize Debian/Ubuntu context;
- handle common command output, service errors, logs, filesystems, permissions, packages, Docker, hardening, and network diagnostics;
- write practical Bash automation for administration tasks.

## Target model

Primary target:

```text
small Debian-admin / small coder-instruct
```

The examples should be precise, compact, and command-oriented.

## Platform

Primary platform:

```text
debian-ubuntu
```

Use Debian/Ubuntu assumptions when relevant:

- `apt`;
- `dpkg`;
- `systemd`;
- `systemctl`;
- `journalctl`;
- `ufw`;
- `netplan`;
- Docker on Debian/Ubuntu hosts;
- GNU userland tools.

Do not mix package managers from unrelated distributions inside this Debian/Ubuntu-only corpus.

## Source format

The dataset uses canonical JSONL records with a `messages` field.

This format is not the final training format for every model. Before fine-tuning, export the source records to the chat template required by the target model.

Governed records should follow the current record-shape schema:

```text
../../schemas/debian-admin-bash.v0.2.schema.json
```

## Coverage

The active v1.0 dataset covers:

- terminal inspection commands;
- systemd and log workflows;
- package-management checks and repairs;
- networking and firewall-adjacent workflows;
- Docker administration;
- Bash CLI tooling patterns;
- incident multisurface triage;
- structured parser output contracts;
- SQLite local database operations;
- backup and restore workflows;
- SSH/authentication administration;
- bounded defensive host-admin audits;
- Bash scripts and functions;
- tool-availability handling;
- structured command-output interpretation;
- refusal and safer-alternative examples.

## Metadata and quality rules

Canonical metadata values and review rules live in [Dataset governance](../../docs/dataset-governance.md).

Canonical record-quality guidance lives in [Quality guidelines](../../docs/quality-guidelines.md).

Short family-specific rule: keep this corpus Debian/Ubuntu-oriented, command-first, concise, inspection-first, and honest about risk/review state.

## Validation

Install dependencies:

```bash
python -m pip install -r ../../requirements-dev.txt
```

From the repository root, validate the v0.2 sample:

```bash
python validation/validate_dataset.py \
  datasets/debian-admin-bash/samples/debian-admin-bash-sft.v0.2.sample.jsonl \
  --schema schemas/debian-admin-bash.v0.2.schema.json
```

Validate the governed v1.0 Debian-admin Bash dataset:

```bash
python validation/validate_dataset.py \
  datasets/debian-admin-bash/debian-admin-bash-sft.v1.0.jsonl \
  --schema schemas/debian-admin-bash.v0.2.schema.json
```

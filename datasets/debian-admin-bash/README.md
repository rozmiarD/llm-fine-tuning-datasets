# debian-admin-bash

## Dataset identity

Current active dataset:

```text
debian-admin-bash-sft.v0.4
```

Reference dataset family:

```text
debian-admin-bash-sft
```

## Tracks

| Track | File | Status |
|---|---|---|
| debian-admin-bash v0.4 | `debian-admin-bash-sft.v0.4.jsonl` | active governed draft dataset |
| v0.2 sample | `samples/debian-admin-bash-sft.v0.2.sample.jsonl` | governed reference sample |

The previous full v0.1 corpus was removed from the active dataset tree because it contained faulty data and should not be used as a valid training source.

Dataset card:

```text
DATASET_CARD.md
```

Validation reports:

```text
../../validation/debian-admin-bash-sft.v0.2.sample.validation-report.md
../../validation/debian-admin-bash-sft.v0.4.validation-report.md
```

Migration notes:

```text
debian-admin-bash-sft.v0.3-to-v0.4.migration-notes.md
```

## Status

The active v0.4 Debian-admin Bash dataset contains 932 governed draft records.

It uses the existing governed record-shape schema:

```text
../../schemas/debian-admin-bash.v0.2.schema.json
```

`meta.dataset_version` is `0.4` because this is the dataset content version. The schema remains v0.2 because the governed record shape did not change.

All records are currently marked as draft. Passing JSON Schema validation and governance linting does not mean that records have been manually reviewed for semantic correctness, safety, or execution behavior.

## debian-admin-bash v0.4 metadata

Record count:

```text
932
```

SHA-256:

```text
498c49a5d51a55316cdc1ca7be6efbf7263ac95a19de0dece05e71384dbfea55
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

The active v0.4 dataset covers:

- terminal inspection commands;
- systemd and log workflows;
- package-management checks and repairs;
- networking and firewall-adjacent workflows;
- Docker administration;
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

Validate the governed v0.4 Debian-admin Bash dataset:

```bash
python validation/validate_dataset.py \
  datasets/debian-admin-bash/debian-admin-bash-sft.v0.4.jsonl \
  --schema schemas/debian-admin-bash.v0.2.schema.json
```

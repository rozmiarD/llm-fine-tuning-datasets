# terminal-admin-bash-master

## Dataset identity

Canonical dataset family:

```text
terminal-admin-bash-master__4b-coder-instruct__sft__en__debian-ubuntu
```

## Tracks

| Track | File | Status |
|---|---|---|
| v0.1 | `terminal-admin-bash-master__4b-coder-instruct__sft__en__debian-ubuntu__v0.1.full-2000.jsonl` | legacy experimental source corpus |
| v0.2 | `samples/terminal-admin-bash-master__4b-coder-instruct__sft__en__debian-ubuntu__v0.2.sample.jsonl` | governed reference sample |

Dataset card:

```text
DATASET_CARD.md
```

Validation reports:

```text
../../validation/terminal-admin-bash-master__4b-coder-instruct__sft__en__debian-ubuntu__v0.1.validation-report.md
../../validation/terminal-admin-bash-master__4b-coder-instruct__sft__en__debian-ubuntu__v0.2.sample.validation-report.md
```

## Status

The v0.1 source corpus is in the repository and contains 2000 records.

The v0.1 corpus is a legacy experimental corpus. It has structural validation evidence, but it should not be treated as production-grade training data without further governance review.

The v0.2 sample is the preferred format for new records because it includes explicit metadata for:

- risk level;
- side effects;
- destructive behavior;
- warning requirements;
- answer style;
- semantic review;
- safety review;
- execution validation status.

## v0.1 corpus metadata

Record count:

```text
2000
```

Identifier range:

```text
tabm-4b-ci-sft-en-du-000005 .. tabm-4b-ci-sft-en-du-002004
```

SHA-256:

```text
7c0079f6985ce9fc1a75c77a7159a87baee21fb4b0b9c8f62f7d2a191c65ee01
```

Blob SHA observed in GitHub:

```text
181b4c7609b4a3d1adb230524960b4a1049018f5
```

## Purpose

This dataset teaches small coder-instruct models to behave like concise Debian/Ubuntu terminal administration assistants.

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
4B coder-instruct
```

This means the dataset is written for small instruction-following coding models rather than broad general chat models or base models.

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

New records should follow the governed v0.2 schema:

```text
../../schemas/terminal-admin-bash-master.v0.2.schema.json
```

## Coverage

The v0.1 corpus covers:

- inspection-first terminal workflows;
- systemd and journalctl troubleshooting;
- apt and dpkg package repair;
- filesystem usage and safe cleanup;
- process, port, and resource diagnostics;
- network, DNS, route, UFW, and netplan diagnosis;
- Docker and Docker Compose operations;
- SSH, sudoers, permissions, ACL, and hardening checks;
- Bash scripts for audits, cleanup, backups, reports, and log parsing;
- output-to-diagnosis records where the user provides command output or errors.

## v0.2 metadata values

Use these values for `meta.risk_level`:

- `safe_readonly`;
- `state_change_low`;
- `state_change_high`;
- `network_sensitive`;
- `privilege_sensitive`;
- `security_sensitive`;
- `destructive`.

Use these values for `meta.answer_style`:

- `single_command`;
- `command_with_brief_explanation`;
- `diagnostic_steps`;
- `script_with_explanation`;
- `guarded_procedure`;
- `refusal_with_safe_alternative`.

Use these values for `meta.review.status`:

- `draft`;
- `reviewed`;
- `quarantined`;
- `rejected`.

## Good example pattern

User asks for a specific operation with context.

Assistant returns:

````text
```bash
command here
```
Short explanation here.
````

For higher-risk operations, the assistant answer should include a guarded procedure, a warning, or a safe alternative as appropriate.

## Bad example pattern

Avoid answers that:

- combine unrelated distribution package managers;
- produce broad destructive one-liners without inspection;
- explain basic shell concepts for many paragraphs;
- guess the environment when the prompt is under-specified;
- use deprecated tools when a modern default exists;
- mark risky commands as `safe_readonly`;
- claim review or execution validation that did not happen.

## Validation

Install dependencies:

```bash
python -m pip install -r ../../requirements-dev.txt
```

From the repository root, validate the v0.2 sample:

```bash
python validation/validate_dataset.py \
  datasets/terminal-admin-bash-master/samples/terminal-admin-bash-master__4b-coder-instruct__sft__en__debian-ubuntu__v0.2.sample.jsonl \
  --schema schemas/terminal-admin-bash-master.v0.2.schema.json
```

For legacy v0.1 migration, run the validator in warn-only mode and review the findings before training.

# terminal-admin-bash-master

## Dataset identity

Current active dataset:

```text
terminal-admin-bash-master__small-terminal-admin__sft__en__debian-ubuntu__v0.3.governed-bash-heavy
```

Reference dataset family:

```text
terminal-admin-bash-master__4b-coder-instruct__sft__en__debian-ubuntu
```

## Tracks

| Track | File | Status |
|---|---|---|
| small-terminal-admin v0.3 | `terminal-admin-bash-master__small-terminal-admin__sft__en__debian-ubuntu__v0.3.governed-bash-heavy.jsonl` | active governed draft dataset |
| v0.2 sample | `samples/terminal-admin-bash-master__4b-coder-instruct__sft__en__debian-ubuntu__v0.2.sample.jsonl` | governed reference sample |

The previous full v0.1 corpus was removed from the active dataset tree because it contained faulty data and should not be used as a valid training source.

Dataset card:

```text
DATASET_CARD.md
```

Validation reports:

```text
../../validation/terminal-admin-bash-master__4b-coder-instruct__sft__en__debian-ubuntu__v0.2.sample.validation-report.md
../../validation/terminal-admin-bash-master__small-terminal-admin__sft__en__debian-ubuntu__v0.3.governed-bash-heavy.validation-report.md
```

Migration notes:

```text
terminal-admin-bash-master__small-terminal-admin__sft__en__debian-ubuntu__v0.2.migration-notes.md
```

## Status

The active v0.3 Bash-heavy dataset contains 908 governed draft records.

It uses the existing governed record-shape schema:

```text
../../schemas/terminal-admin-bash-master.v0.2.schema.json
```

`meta.dataset_version` is `0.3` because this is the dataset content version. The schema remains v0.2 because the governed record shape did not change.

All records are currently marked as draft. Passing JSON Schema validation and governance linting does not mean that records have been manually reviewed for semantic correctness, safety, or execution behavior.

## small-terminal-admin v0.3 metadata

Record count:

```text
908
```

SHA-256:

```text
036b4a295b1dc37827760d36e1b2aa958c3a910831e0411bbee0d1735ac358ca
```

Governance schema:

```text
../../schemas/terminal-admin-bash-master.v0.2.schema.json
```

Review status:

```text
draft
```

The validation report shows 0 JSON errors, 0 schema errors, 0 governance lint errors, and 0 warnings. This is not a semantic, safety, or execution review claim.

## Purpose

This dataset teaches small terminal-administration models to behave like concise Debian/Ubuntu terminal assistants.

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
small terminal-admin / small coder-instruct
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
../../schemas/terminal-admin-bash-master.v0.2.schema.json
```

## Coverage

The active v0.3 dataset covers:

- terminal inspection commands;
- systemd and log workflows;
- package-management checks and repairs;
- networking and firewall-adjacent workflows;
- Docker administration;
- Bash scripts and functions;
- tool-availability handling;
- structured command-output interpretation;
- refusal and safer-alternative examples.

## Metadata values

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

Validate the governed v0.3 Bash-heavy dataset:

```bash
python validation/validate_dataset.py \
  datasets/terminal-admin-bash-master/terminal-admin-bash-master__small-terminal-admin__sft__en__debian-ubuntu__v0.3.governed-bash-heavy.jsonl \
  --schema schemas/terminal-admin-bash-master.v0.2.schema.json
```

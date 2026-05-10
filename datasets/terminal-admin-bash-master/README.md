# terminal-admin-bash-master

## Dataset identity

Canonical dataset name:

```text
terminal-admin-bash-master__4b-coder-instruct__sft__en__debian-ubuntu__v0.1
```

Full source file:

```text
terminal-admin-bash-master__4b-coder-instruct__sft__en__debian-ubuntu__v0.1.full-2000.jsonl
```

Dataset card:

```text
DATASET_CARD.md
```

Sample file:

```text
samples/terminal-admin-bash-master__4b-coder-instruct__sft__en__debian-ubuntu__v0.1.sample.jsonl
```

Validation report:

```text
../../validation/terminal-admin-bash-master__4b-coder-instruct__sft__en__debian-ubuntu__v0.1.validation-report.md
```

## Status

v0.1 source corpus in repository.

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

When a record is not Debian/Ubuntu-specific, use:

```json
"platform": "common-linux"
```

When comparing distributions, use:

```json
"platform": "cross-distro"
```

## Source format

The dataset uses canonical JSONL records with a `messages` field.

This format is not the final training format for every model. Before fine-tuning, export the source records to the chat template required by the target model.

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

## Task type suggestions

Use one of these values for `meta.task_type`:

- `command_generation`;
- `command_explanation`;
- `log_analysis`;
- `troubleshooting`;
- `safe_fix`;
- `file_inspection`;
- `service_management`;
- `network_diagnosis`;
- `permission_diagnosis`;
- `process_diagnosis`;
- `package_management`.

## Difficulty values

Use:

- `basic`;
- `intermediate`;
- `advanced`.

Do not use difficulty as marketing. Use it to help split evals and training subsets.

## Good example pattern

User asks for a specific operation with context.

Assistant returns:

````text
```bash
command here
```
Short explanation here.
````

## Bad example pattern

Avoid answers that:

- combine `apt`, `dnf`, `pacman`, and `apk` in one generic command sequence;
- produce destructive one-liners without inspection;
- explain basic shell concepts for many paragraphs;
- guess the environment when the prompt is under-specified;
- use deprecated tools when a modern default exists.

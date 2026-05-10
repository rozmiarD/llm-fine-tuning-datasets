# terminal-admin-bash-master

## Dataset identity

Canonical dataset name:

```text
terminal-admin-bash-master__4b-coder-instruct__sft__en__debian-ubuntu__v0.1
```

## Purpose

This dataset teaches small coder-instruct models to behave like concise Debian/Ubuntu terminal administration assistants.

The expected model behavior is:

- produce correct Bash/Linux commands;
- give a short factual explanation;
- avoid unnecessary verbosity;
- prefer safe inspection before modification;
- recognize Debian/Ubuntu context;
- handle common command output, service errors, logs, filesystems, permissions, packages, and network diagnostics.

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

## Current file

Sample file:

```text
samples/terminal-admin-bash-master__4b-coder-instruct__sft__en__debian-ubuntu__v0.1.sample.jsonl
```

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

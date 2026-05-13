# Dataset Card: debian-admin-bash

## Dataset name

Current active dataset:

```text
debian-admin-bash-sft.v1.0
```

Reference dataset family:

```text
debian-admin-bash-sft
```

## Status

This dataset currently has two active tracks:

| Track | File | Status |
|---|---|---|
| debian-admin-bash v1.0 | `debian-admin-bash-sft.v1.0.jsonl` | active governed draft dataset |
| v0.2 sample | `samples/debian-admin-bash-sft.v0.2.sample.jsonl` | governed reference sample |

The previous full v0.1 corpus was removed from the active dataset tree because it contained faulty data and should not be used as a valid training source.

The v0.2 sample defines the governed source-record shape with explicit risk, safety, answer-style, and review metadata.

The active v1.0 Debian-admin Bash dataset contains 2552 governed draft records. It uses the existing governed v0.2 record-shape schema because the record shape did not change.

PostgreSQL is intentionally excluded from the active corpus; database coverage is scoped to SQLite as a local file-backed admin surface.

## debian-admin-bash v1.0 metadata

Source lineage:

```text
debian-admin-bash-sft.v0.3.cleaned-source.jsonl
curated v0.4-v1.0 Debian-admin Bash supplements
```

Output:

```text
debian-admin-bash-sft.v1.0.jsonl
```

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
schemas/debian-admin-bash.v0.2.schema.json
```

Validation report:

```text
validation/debian-admin-bash-sft.v1.0.validation-report.md
```

Review status:

```text
draft
```

## Production-readiness statement

The active v1.0 dataset should not be treated as production-grade only because it passes schema and governance linting. Its records remain `draft` until semantic review, safety review, and any required execution validation are completed.

Before training, records should be reviewed for:

- semantic correctness;
- Debian/Ubuntu platform consistency;
- risk-level accuracy;
- safety metadata accuracy;
- answer-style consistency;
- command correctness;
- suitability for the target model and runtime controls.

## Intended use

This dataset is intended for supervised fine-tuning of small coder-instruct or terminal-administration models.

Primary use case:

- concise Linux terminal administration;
- Debian/Ubuntu systems;
- Bash command generation;
- short factual explanations;
- inspection-first troubleshooting;
- practical Bash automation;
- Docker, network, service, package, permission, Bash tooling, incident triage, structured parsers, SQLite, backup/restore, SSH/auth, and hardening workflows.

## Language

English.

## Platform

Primary platform:

- Debian/Ubuntu;
- systemd-based systems;
- apt/dpkg package management;
- Docker on Debian/Ubuntu hosts;
- GNU userland command behavior.

Secondary coverage:

- common GNU/Linux Bash patterns that also apply outside Debian/Ubuntu when explicitly marked.

## Target model profile

Preferred target:

- small Debian-admin or coder-instruct model;
- chat/instruction-following capable;
- suitable for local or edge-device experimentation.

This dataset is not optimized for base models without instruction tuning unless converted and mixed with appropriate instruction data.

## Source format and export

Canonical source format and model-specific export expectations are defined in [Dataset format](../../docs/dataset-format.md).

This card only records dataset-specific facts: the active v1.0 file is JSONL source data, not a trainer-specific export.

## Recommended answer style and quality priorities

Canonical answer styles are defined in [Dataset governance](../../docs/dataset-governance.md). General quality guidance is defined in [Quality guidelines](../../docs/quality-guidelines.md).

Family-specific priority: examples should remain command-first, concise, Debian/Ubuntu-aware, and explicit about operational risk.

Good records should teach:

- precise command choice;
- correct flag usage;
- Debian/Ubuntu context awareness;
- short explanations;
- safe inspection before modification;
- interpretation of command output and common errors;
- non-interactive commands suitable for terminal agents;
- practical medium-sized Bash scripts;
- SQLite schema, migration, backup, integrity, WAL/locking, and query-plan workflows;
- JSON/JQ/JSONL/CSV validation, transformation, fallback, and atomic config patching workflows;
- bounded nmap host-exposure verification for owned or explicitly approved targets;
- Bash CLI argument, logging, dry-run, and exit-code habits;
- multisurface incident triage and guarded fix planning;
- structured JSON/TSV/CSV parser contracts;
- SQLite file-database operational safety;
- backup/restore verification habits;
- access, identity, sudoers, SSH, service-user, PAM, ACL, and AppArmor guardrails;
- apt/dpkg lifecycle diagnostics, package lock handling, repository/keyring inspection, and guarded package changes;
- process/resource diagnosis for OOM, file descriptors, cgroups, restart loops, and high load;
- SSH/authentication guardrails;
- verification after a fix;
- honest risk and review metadata.

## v1.0 expansion summary

The v1.0 supplement intentionally strengthens existing Debian/Ubuntu admin surfaces instead of adding a new domain. It adds apt/dpkg lifecycle diagnostics and guarded changes, package/repository/keyring/lock/output errors, process/resource/OOM/file-descriptor/systemd-cgroup diagnosis, and mixed output-driven incidents connecting package maintenance with services and host resources.

It does not add PostgreSQL, Kubernetes, cloud-provider operations, Terraform, GPU/CUDA, Wireshark, packet forensics, offensive security, broad backend development, or broad enterprise IAM.

## Distribution summary for debian-admin-bash v1.0

### Difficulty

| Difficulty | Count |
|---|---:|
| `beginner` | 425 |
| `intermediate` | 1107 |
| `advanced` | 1020 |

### Risk level

| Risk level | Count |
|---|---:|
| `safe_readonly` | 1918 |
| `state_change_low` | 273 |
| `state_change_high` | 63 |
| `network_sensitive` | 101 |
| `privilege_sensitive` | 25 |
| `security_sensitive` | 167 |
| `destructive` | 5 |

### Answer style

| Answer style | Count |
|---|---:|
| `command_with_brief_explanation` | 1109 |
| `diagnostic_steps` | 692 |
| `guarded_procedure` | 345 |
| `refusal_with_safe_alternative` | 200 |
| `script_with_explanation` | 206 |

## Known limitations

This dataset does not claim broad Linux coverage.

It should not be treated as a complete system administration corpus, a security benchmark, or a production safety layer.

The dataset teaches terminal operator behavior and command generation patterns. Runtime safety, authorization, and execution controls must be implemented outside the model.

The active v1.0 dataset has schema and governance-lint validation evidence, but all records remain draft until manual review.

## Migration recommendation

For cleaned external source records:

1. preserve source lineage under `meta.source`;
2. run `validation/validate_dataset.py`;
3. review lint findings;
4. quarantine or reject ambiguous and unsafe records;
5. export only reviewed subsets for training.

# Dataset Card: debian-admin-bash

## Dataset name

Current active dataset:

```text
debian-admin-bash-sft.v0.6
```

Reference dataset family:

```text
debian-admin-bash-sft
```

## Status

This dataset currently has two active tracks:

| Track | File | Status |
|---|---|---|
| debian-admin-bash v0.6 | `debian-admin-bash-sft.v0.6.jsonl` | active governed draft dataset |
| v0.2 sample | `samples/debian-admin-bash-sft.v0.2.sample.jsonl` | governed reference sample |

The previous full v0.1 corpus was removed from the active dataset tree because it contained faulty data and should not be used as a valid training source.

The v0.2 sample defines the governed source-record shape with explicit risk, safety, answer-style, and review metadata.

The active v0.6 Debian-admin Bash dataset contains 1700 governed draft records. It uses the existing governed v0.2 record-shape schema because the record shape did not change.

PostgreSQL is intentionally excluded from the active corpus; database coverage is scoped to SQLite as a local file-backed admin surface.

## debian-admin-bash v0.6 metadata

Source lineage:

```text
debian-admin-bash-sft.v0.3.cleaned-source.jsonl
curated v0.4-v0.6 Debian-admin Bash supplements
```

Output:

```text
debian-admin-bash-sft.v0.6.jsonl
```

Record count:

```text
1700
```

SHA-256:

```text
2f3e07990fd6a18e0c41076eb3fe98ccfdeccc8a079be1c498122feabef069ef
```

Governance schema:

```text
schemas/debian-admin-bash.v0.2.schema.json
```

Validation report:

```text
validation/debian-admin-bash-sft.v0.6.validation-report.md
```

Review status:

```text
draft
```

## Production-readiness statement

The active v0.6 dataset should not be treated as production-grade only because it passes schema and governance linting. Its records remain `draft` until semantic review, safety review, and any required execution validation are completed.

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

This card only records dataset-specific facts: the active v0.6 file is JSONL source data, not a trainer-specific export.

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
- Bash CLI argument, logging, dry-run, and exit-code habits;
- multisurface incident triage and guarded fix planning;
- structured JSON/TSV/CSV parser contracts;
- SQLite file-database operational safety;
- backup/restore verification habits;
- SSH/authentication guardrails;
- verification after a fix;
- honest risk and review metadata.

## Distribution summary for debian-admin-bash v0.6

### Difficulty

| Difficulty | Count |
|---|---:|
| `beginner` | 345 |
| `intermediate` | 659 |
| `advanced` | 696 |

### Risk level

| Risk level | Count |
|---|---:|
| `safe_readonly` | 1363 |
| `state_change_low` | 184 |
| `state_change_high` | 42 |
| `network_sensitive` | 23 |
| `privilege_sensitive` | 21 |
| `security_sensitive` | 63 |
| `destructive` | 4 |

### Answer style

| Answer style | Count |
|---|---:|
| `command_with_brief_explanation` | 832 |
| `diagnostic_steps` | 355 |
| `guarded_procedure` | 221 |
| `refusal_with_safe_alternative` | 110 |
| `script_with_explanation` | 182 |

## Known limitations

This dataset does not claim broad Linux coverage.

It should not be treated as a complete system administration corpus, a security benchmark, or a production safety layer.

The dataset teaches terminal operator behavior and command generation patterns. Runtime safety, authorization, and execution controls must be implemented outside the model.

The active v0.6 dataset has schema and governance-lint validation evidence, but all records remain draft until manual review.

## Migration recommendation

For cleaned external source records:

1. preserve source lineage under `meta.source`;
2. run `validation/validate_dataset.py`;
3. review lint findings;
4. quarantine or reject ambiguous and unsafe records;
5. export only reviewed subsets for training.

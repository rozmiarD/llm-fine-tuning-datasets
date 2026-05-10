# Dataset Card: terminal-admin-bash-master

## Dataset name

Primary dataset family:

```text
terminal-admin-bash-master__4b-coder-instruct__sft__en__debian-ubuntu
```

Additional governed conversion track:

```text
terminal-admin-bash-master__small-terminal-admin__sft__en__debian-ubuntu
```

## Status

This dataset currently has three tracks:

| Track | File | Status |
|---|---|---|
| v0.1 | `terminal-admin-bash-master__4b-coder-instruct__sft__en__debian-ubuntu__v0.1.full-2000.jsonl` | legacy experimental source corpus |
| v0.2 sample | `samples/terminal-admin-bash-master__4b-coder-instruct__sft__en__debian-ubuntu__v0.2.sample.jsonl` | governed reference sample |
| small-terminal-admin v0.2 | `terminal-admin-bash-master__small-terminal-admin__sft__en__debian-ubuntu__v0.2.jsonl` | governed draft conversion from cleaned Bash-heavy source material |

The v0.1 corpus contains 2000 canonical JSONL records and remains in the repository for reproducibility and migration.

The v0.2 sample defines the preferred governed source-record shape with explicit risk, safety, answer-style, and review metadata.

The small-terminal-admin v0.2 conversion contains 908 governed draft records converted from a cleaned Bash-heavy v0.3 source dataset. It uses the existing governed v0.2 schema. No v0.3 schema is required because the governed record shape did not change.

## v0.1 corpus metadata

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

## small-terminal-admin v0.2 metadata

Source:

```text
terminal-admin-bash-master__small-terminal-admin__sft__en__linux-debian-ubuntu__v0.3.cleaned-bash-heavy.jsonl
```

Output:

```text
terminal-admin-bash-master__small-terminal-admin__sft__en__debian-ubuntu__v0.2.jsonl
```

Record count:

```text
908
```

SHA-256:

```text
b482349a828aca5309ce55a0026b18598702ffb9c8a520b4657063b3f872bcc2
```

Governance schema:

```text
schemas/terminal-admin-bash-master.v0.2.schema.json
```

Validation report:

```text
validation/terminal-admin-bash-master__small-terminal-admin__sft__en__debian-ubuntu__v0.2.validation-report.md
```

Review status:

```text
draft
```

## Production-readiness statement

The v0.1 corpus should not be treated as production-grade training data only because it passes structural validation.

The small-terminal-admin v0.2 conversion should also not be treated as production-grade only because it passes schema and governance linting. Its records remain `draft` until semantic review, safety review, and any required execution validation are completed.

Before training, records should be migrated or filtered through the v0.2 governance model and reviewed for:

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
- Docker, network, service, package, permission, and hardening workflows.

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

- approximately 4B parameters;
- coder-instruct or terminal-admin model;
- chat/instruction-following capable;
- suitable for local or edge-device experimentation.

This dataset is not optimized for base models without instruction tuning unless converted and mixed with appropriate instruction data.

## Canonical source format

JSONL with one record per line.

Each record contains:

- `id`;
- `meta`;
- `messages`.

The `messages` field is the training conversation. The `meta` field is for filtering, validation, export, safety review, and documentation.

## Model-specific formatting

The source JSONL format is not a replacement for model-specific chat templates.

Before training, records should be exported or templated for the target model family.

Examples:

- ChatML-style models;
- Llama-style chat templates;
- Gemma-style chat templates;
- Alpaca-style prompt/completion formats;
- trainer-specific formats used by Axolotl, TRL, Unsloth, or similar tools.

The repository stores the canonical source data. Training pipelines should handle the final target format.

## Recommended answer style

Assistant answers should usually contain:

1. a Bash code block with one command or a short command sequence;
2. one or two short factual explanation sentences;
3. a caution only when needed;
4. guarded procedure language when the task changes system state.

Example:

````text
```bash
systemctl status nginx --no-pager
journalctl -u nginx -n 80 --no-pager
```
These commands inspect the current nginx service state and recent logs without opening an interactive pager.
````

## Quality priorities

Good records should teach:

- precise command choice;
- correct flag usage;
- Debian/Ubuntu context awareness;
- short explanations;
- safe inspection before modification;
- interpretation of command output and common errors;
- non-interactive commands suitable for terminal agents;
- practical medium-sized Bash scripts;
- verification after a fix;
- honest risk and review metadata.

## Distribution summary for v0.1 legacy corpus

### Difficulty

| Difficulty | Count |
|---|---:|
| `basic` | 59 |
| `intermediate` | 434 |
| `advanced` | 1507 |

### Task types

| Task type | Count |
|---|---:|
| `command_explanation` | 26 |
| `command_generation` | 432 |
| `file_inspection` | 167 |
| `log_analysis` | 95 |
| `network_diagnosis` | 186 |
| `package_management` | 181 |
| `permission_diagnosis` | 95 |
| `process_diagnosis` | 95 |
| `safe_fix` | 287 |
| `service_management` | 92 |
| `troubleshooting` | 344 |

## Distribution summary for small-terminal-admin v0.2 conversion

### Difficulty

| Difficulty | Count |
|---|---:|
| `beginner` | 314 |
| `intermediate` | 241 |
| `advanced` | 353 |

### Risk level

| Risk level | Count |
|---|---:|
| `safe_readonly` | 726 |
| `state_change_low` | 97 |
| `state_change_high` | 18 |
| `network_sensitive` | 9 |
| `privilege_sensitive` | 19 |
| `security_sensitive` | 37 |
| `destructive` | 2 |

### Answer style

| Answer style | Count |
|---|---:|
| `command_with_brief_explanation` | 398 |
| `diagnostic_steps` | 224 |
| `guarded_procedure` | 113 |
| `refusal_with_safe_alternative` | 79 |
| `script_with_explanation` | 94 |

## Known limitations

This dataset does not claim broad Linux coverage.

It should not be treated as a complete system administration corpus, a security benchmark, or a production safety layer.

The dataset teaches terminal operator behavior and command generation patterns. Runtime safety, authorization, and execution controls must be implemented outside the model.

The v0.1 corpus has structural validation evidence, but not full semantic, safety, or execution validation evidence.

The small-terminal-admin v0.2 conversion has schema and governance-lint validation evidence, but all records remain draft until manual review.

## Migration recommendation

Use v0.2 metadata for new records.

For existing v0.1 records or cleaned external source records:

1. migrate metadata into the v0.2 schema;
2. preserve source lineage under `meta.source`;
3. run `validation/validate_dataset.py`;
4. review lint findings;
5. quarantine or reject ambiguous and unsafe records;
6. export only reviewed subsets for training.

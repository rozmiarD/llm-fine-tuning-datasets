# Dataset Card: terminal-admin-bash-master

## Dataset name

Current active dataset:

```text
terminal-admin-bash-master__small-terminal-admin__sft__en__debian-ubuntu__v0.3.governed-bash-heavy
```

Reference dataset family:

```text
terminal-admin-bash-master__4b-coder-instruct__sft__en__debian-ubuntu
```

## Status

This dataset currently has two active tracks:

| Track | File | Status |
|---|---|---|
| small-terminal-admin v0.3 | `terminal-admin-bash-master__small-terminal-admin__sft__en__debian-ubuntu__v0.3.governed-bash-heavy.jsonl` | active governed draft dataset |
| v0.2 sample | `samples/terminal-admin-bash-master__4b-coder-instruct__sft__en__debian-ubuntu__v0.2.sample.jsonl` | governed reference sample |

The previous full v0.1 corpus was removed from the active dataset tree because it contained faulty data and should not be used as a valid training source.

The v0.2 sample defines the governed source-record shape with explicit risk, safety, answer-style, and review metadata.

The active v0.3 Bash-heavy dataset contains 908 governed draft records. It uses the existing governed v0.2 record-shape schema because the record shape did not change.

## small-terminal-admin v0.3 metadata

Source:

```text
terminal-admin-bash-master__small-terminal-admin__sft__en__linux-debian-ubuntu__v0.3.cleaned-bash-heavy.jsonl
```

Output:

```text
terminal-admin-bash-master__small-terminal-admin__sft__en__debian-ubuntu__v0.3.governed-bash-heavy.jsonl
```

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
schemas/terminal-admin-bash-master.v0.2.schema.json
```

Validation report:

```text
validation/terminal-admin-bash-master__small-terminal-admin__sft__en__debian-ubuntu__v0.3.governed-bash-heavy.validation-report.md
```

Review status:

```text
draft
```

## Production-readiness statement

The active v0.3 dataset should not be treated as production-grade only because it passes schema and governance linting. Its records remain `draft` until semantic review, safety review, and any required execution validation are completed.

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

- small terminal-admin or coder-instruct model;
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

## Distribution summary for small-terminal-admin v0.3

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
| `diagnostic_steps` | 217 |
| `guarded_procedure` | 115 |
| `refusal_with_safe_alternative` | 84 |
| `script_with_explanation` | 94 |

## Known limitations

This dataset does not claim broad Linux coverage.

It should not be treated as a complete system administration corpus, a security benchmark, or a production safety layer.

The dataset teaches terminal operator behavior and command generation patterns. Runtime safety, authorization, and execution controls must be implemented outside the model.

The active v0.3 dataset has schema and governance-lint validation evidence, but all records remain draft until manual review.

## Migration recommendation

For cleaned external source records:

1. preserve source lineage under `meta.source`;
2. run `validation/validate_dataset.py`;
3. review lint findings;
4. quarantine or reject ambiguous and unsafe records;
5. export only reviewed subsets for training.

# Dataset Card: terminal-admin-bash-master

## Dataset name

`terminal-admin-bash-master__4b-coder-instruct__sft__en__debian-ubuntu__v0.1`

## Status

v0.1 source corpus.

This dataset contains 2000 canonical JSONL records for supervised fine-tuning.

Identifier range:

```text
tabm-4b-ci-sft-en-du-000005 .. tabm-4b-ci-sft-en-du-002004
```

SHA-256:

```text
fac95a13a6d0e6efd4ae326b1c1946bda1e2a9f59e4961ced6447699448b52d7
```

## Intended use

This dataset is intended for supervised fine-tuning of small coder-instruct models around 4B parameters.

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
- coder-instruct model;
- chat/instruction-following capable;
- suitable for local or edge-device experimentation.

This dataset is not optimized for base models without instruction tuning unless converted and mixed with appropriate instruction data.

## Canonical source format

JSONL with one record per line.

Each record contains:

- `id`;
- `meta`;
- `messages`.

The `messages` field is the training conversation. The `meta` field is for filtering, validation, export, and documentation.

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
3. a caution only when needed.

Example:

````text
```bash
sudo systemctl status nginx --no-pager
sudo journalctl -u nginx -n 80 --no-pager
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
- verification after a fix.

## Distribution summary

### Difficulty

| Difficulty | Count |
|---|---:|
| basic | 152 |
| intermediate | 587 |
| advanced | 1261 |

### Task types

| Task type | Count |
|---|---:|
| `command_explanation` | 117 |
| `command_generation` | 360 |
| `file_inspection` | 69 |
| `log_analysis` | 94 |
| `network_diagnosis` | 110 |
| `package_management` | 149 |
| `permission_diagnosis` | 54 |
| `process_diagnosis` | 76 |
| `safe_fix` | 422 |
| `service_management` | 104 |
| `troubleshooting` | 445 |

## Known limitations

This dataset does not claim broad Linux coverage.

It should not be treated as a complete system administration corpus, a security benchmark, or a production safety layer.

The dataset teaches terminal operator behavior and command generation patterns. Runtime safety, authorization, and execution controls must be implemented outside the model.

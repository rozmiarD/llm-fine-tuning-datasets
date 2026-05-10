# Dataset Card: terminal-admin-bash-master

## Dataset name

`terminal-admin-bash-master__4b-coder-instruct__sft__en__debian-ubuntu__v0.1`

## Status

v0.1 source corpus.

This dataset contains 2000 canonical JSONL records for supervised fine-tuning.

Full source file:

```text
terminal-admin-bash-master__4b-coder-instruct__sft__en__debian-ubuntu__v0.1.full-2000.jsonl
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

## Known limitations

This dataset does not claim broad Linux coverage.

It should not be treated as a complete system administration corpus, a security benchmark, or a production safety layer.

The dataset teaches terminal operator behavior and command generation patterns. Runtime safety, authorization, and execution controls must be implemented outside the model.

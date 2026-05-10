# Dataset Card: terminal-admin-bash-master

## Dataset name

`terminal-admin-bash-master__4b-coder-instruct__sft__en__debian-ubuntu__v0.1`

## Status

Bootstrap sample.

This is not yet a large training dataset. It defines the initial structure, schema, naming convention, and example style.

## Intended use

This dataset is intended for supervised fine-tuning of small coder-instruct models around 4B parameters.

Primary use case:

- concise Linux terminal administration;
- Debian/Ubuntu systems;
- Bash command generation;
- short factual explanations;
- inspection-first troubleshooting.

## Language

English.

## Platform

Primary platform:

- Debian/Ubuntu;
- systemd-based systems;
- apt/dpkg package management.

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
2. one short factual explanation;
3. a caution only when needed.

Example:

````text
```bash
sudo systemctl status nginx --no-pager
```
This shows the current nginx service status without opening an interactive pager.
````

## Quality priorities

Good records should teach:

- precise command choice;
- correct flag usage;
- Debian/Ubuntu context awareness;
- short explanations;
- safe inspection before modification;
- interpretation of command output and common errors;
- non-interactive commands suitable for terminal agents.

## Known limitations

This dataset does not claim broad Linux coverage.

It should not be treated as a complete system administration corpus, a security benchmark, or a production safety layer.

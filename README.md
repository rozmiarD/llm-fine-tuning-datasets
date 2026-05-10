# LLM Fine-Tuning Datasets

[![License: CC BY 4.0](https://img.shields.io/badge/license-CC--BY--4.0-blue.svg)](LICENSE.md)
[![Format: JSONL messages](https://img.shields.io/badge/format-JSONL%20messages-informational.svg)](docs/dataset-format.md)
[![Target: 4B coder-instruct](https://img.shields.io/badge/target-4B%20coder--instruct-informational.svg)](DATASET_CARD.md)
[![Platform: Debian/Ubuntu](https://img.shields.io/badge/platform-Debian%2FUbuntu-informational.svg)](datasets/terminal-admin-bash-master/README.md)
[![Docs: WCAG-aware](https://img.shields.io/badge/docs-WCAG--aware-informational.svg)](docs/accessibility-guidelines.md)

Structured datasets for training and evaluating small local LLMs used in terminal administration workflows.

This repository starts with one focused dataset role: **terminal-admin-bash-master**.

The first dataset is designed for small **4B coder-instruct** models and focuses on concise Debian/Ubuntu terminal administration: correct Bash/Linux commands, short factual explanations, inspection-first workflows, and basic interpretation of command output.

## Current dataset

| Dataset | Target model | Use | Language | Platform | Status |
|---|---:|---|---|---|---|
| `terminal-admin-bash-master__4b-coder-instruct__sft__en__debian-ubuntu__v0.1` | 4B coder-instruct | SFT | English | Debian/Ubuntu | bootstrap sample |

## What this repository is for

This repository provides source datasets and documentation for preparing model-specific training files.

The source format is intentionally simple:

- JSONL, one record per line.
- Chat-style `messages` field.
- Small metadata block used for filtering, validation, export, and dataset cards.
- English training examples.
- Short command-first assistant answers.

The repository is not tied to one trainer, model family, tokenizer, or chat template. Model-specific formatting should be handled by export scripts or training configuration.

## Primary scope

The first dataset targets:

- Linux terminal administration.
- Debian/Ubuntu systems.
- Bash and common GNU/Linux tools.
- `apt`, `dpkg`, `systemd`, `journalctl`, `ufw`, `netplan`, `ss`, `ip`, `find`, `du`, `df`, `grep`, `awk`, `sed`, `tar`, `rsync`.
- Small coder-instruct models around 4B parameters.

The dataset may include common GNU/Linux examples, but Debian/Ubuntu with systemd and apt is the main target platform.

## Out of scope for the first dataset

The first dataset is not intended to be:

- a broad all-distribution Linux dataset;
- an offensive security dataset;
- a policy-wrapper runtime;
- a collection of long tutorials;
- a prompt dump without validation rules;
- a benchmark claiming broad model quality.

## Repository layout

```text
.
├── README.md
├── DATASET_CARD.md
├── CONTRIBUTING.md
├── LICENSE.md
├── datasets/
│   └── terminal-admin-bash-master/
│       ├── README.md
│       └── samples/
│           └── terminal-admin-bash-master__4b-coder-instruct__sft__en__debian-ubuntu__v0.1.sample.jsonl
├── docs/
│   ├── accessibility-guidelines.md
│   ├── dataset-format.md
│   ├── naming-convention.md
│   └── quality-guidelines.md
├── schemas/
│   └── terminal-admin-bash-master.v0.1.schema.json
└── validation/
    └── README.md
```

## Canonical dataset naming

Dataset files should follow this pattern:

```text
<role>__<target-model-profile>__<training-use>__<language>__<platform>__<version>.jsonl
```

Example:

```text
terminal-admin-bash-master__4b-coder-instruct__sft__en__debian-ubuntu__v0.1.jsonl
```

This name states the role, target model profile, training use, language, platform, and version without requiring users to inspect the file contents first.

See [Naming convention](docs/naming-convention.md).

## Canonical record format

Each JSONL line is one training record.

```json
{
  "id": "tabm-4b-ci-sft-en-du-000001",
  "meta": {
    "role": "terminal-admin-bash-master",
    "target_model_size": "4b",
    "target_model_type": "coder-instruct",
    "training_use": "sft",
    "language": "en",
    "platform": "debian-ubuntu",
    "task_type": "command_generation",
    "difficulty": "basic",
    "tags": ["linux", "bash", "disk-usage"]
  },
  "messages": [
    {
      "role": "system",
      "content": "You are a Linux terminal administration assistant. Return correct Bash commands and a brief factual explanation. Prefer safe, non-destructive commands unless the user explicitly asks for a change."
    },
    {
      "role": "user",
      "content": "Show the 10 largest files and directories in the current directory."
    },
    {
      "role": "assistant",
      "content": "```bash\ndu -ah . | sort -rh | head -n 10\n```\nThis scans the current directory, sorts entries by size in descending order, and prints the 10 largest results."
    }
  ]
}
```

See [Dataset format](docs/dataset-format.md) and the JSON Schema in [`schemas/`](schemas/).

## Answer style taught by the first dataset

The assistant answer should usually contain:

1. One correct command or a short command sequence in a Bash code block.
2. A brief factual explanation.
3. A warning only when the command modifies or may damage system state.

Avoid long essays, fake certainty, unnecessary alternatives, and risky one-liners when an inspection-first workflow is more appropriate.

## Data quality rules

High-value records should include at least one of the following:

- a realistic operating-system context;
- a constraint such as inspect-only, no deletion, non-interactive output, same filesystem only;
- command output, error output, or log excerpts;
- a clear distinction between inspection and modification;
- a modern replacement for obsolete commands;
- concise explanation of important flags.

See [Quality guidelines](docs/quality-guidelines.md).

## Accessibility and documentation style

Documentation should be readable without relying on icons, colors, images, or badge text alone.

Use descriptive headings, plain language, short paragraphs, meaningful link text, consistent file names, and copyable examples.

See [Accessibility guidelines](docs/accessibility-guidelines.md).

## License

Dataset content and documentation are licensed under **Creative Commons Attribution 4.0 International (CC BY 4.0)**.

See [LICENSE.md](LICENSE.md).

## Status

This repository is in bootstrap state. The initial structure, schema, documentation, and sample records are intended to prepare the ground for iterative dataset development.

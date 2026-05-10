# LLM Fine-Tuning Datasets

[![License: CC BY 4.0](https://img.shields.io/badge/license-CC--BY--4.0-blue.svg)](LICENSE.md)
[![Format: JSONL messages](https://img.shields.io/badge/format-JSONL%20messages-green.svg)](docs/dataset-format.md)
[![Docs: WCAG-aware](https://img.shields.io/badge/docs-WCAG--aware-purple.svg)](docs/accessibility-guidelines.md)

Structured source datasets for fine-tuning, evaluating, and preparing small local LLMs for practical technical workflows.

This repository is organized around role-specific datasets. Each dataset should define its intended model profile, training use, language, platform, format, quality rules, and validation requirements.

## Dataset registry

| Dataset | Target model | Use | Language | Platform | Records | Purpose | Status |
|---|---:|---|---|---|---:|---|---|
| [`terminal-admin-bash-master__4b-coder-instruct__sft__en__debian-ubuntu__v0.1`](datasets/terminal-admin-bash-master/README.md) | 4B coder-instruct | SFT | English | Debian/Ubuntu | sample included; full corpus pending upload | Terminal administration: Bash commands, short explanations, inspection-first operator workflows | Corpus prepared; source file upload pending |

## Repository goals

The repository is intended to provide:

- source datasets in a stable canonical format;
- naming conventions that expose model profile, use case, language, platform, and version;
- dataset cards and per-dataset documentation;
- validation schemas and future validation scripts;
- quality guidelines for creating useful training records;
- documentation that remains readable and accessible without relying on visuals alone.

## Source format

The canonical source format is JSONL with one training record per line.

Each record contains:

- `id` — stable record identifier;
- `meta` — metadata for filtering, validation, export, and documentation;
- `messages` — chat-style training content.

The repository stores source data. Training pipelines should export or template the source records for the target model family and tokenizer.

See [Dataset format](docs/dataset-format.md).

## Naming convention

Dataset files should follow this pattern:

```text
<role>__<target-model-profile>__<training-use>__<language>__<platform>__<version>.jsonl
```

Example:

```text
terminal-admin-bash-master__4b-coder-instruct__sft__en__debian-ubuntu__v0.1.jsonl
```

See [Naming convention](docs/naming-convention.md).

## Repository layout

```text
.
├── README.md
├── DATASET_CARD.md
├── CONTRIBUTING.md
├── LICENSE.md
├── datasets/
│   ├── README.md
│   └── terminal-admin-bash-master/
│       ├── README.md
│       ├── DATASET_CARD.md
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
    ├── README.md
    └── bootstrap-validation-report.md
```

## Documentation style

Documentation should be practical, direct, and easy to inspect.

Use:

- descriptive headings;
- plain language;
- short paragraphs;
- meaningful link text;
- consistent file names;
- copyable examples.

Avoid marketing language, vague claims, and long explanations that do not help maintain or use the dataset.

See [Accessibility guidelines](docs/accessibility-guidelines.md) and [Quality guidelines](docs/quality-guidelines.md).

## License

Dataset content and documentation are licensed under **Creative Commons Attribution 4.0 International (CC BY 4.0)**.

See [LICENSE.md](LICENSE.md).

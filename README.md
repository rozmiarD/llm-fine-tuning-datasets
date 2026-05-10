# LLM Fine-Tuning Datasets

[![License: CC BY 4.0](https://img.shields.io/badge/license-CC--BY--4.0-blue.svg)](LICENSE.md)
[![Format: JSONL messages](https://img.shields.io/badge/format-JSONL%20messages-green.svg)](docs/dataset-format.md)
[![Governance: quality gates](https://img.shields.io/badge/governance-quality%20gates-orange.svg)](docs/dataset-governance.md)
[![Docs: WCAG-aware](https://img.shields.io/badge/docs-WCAG--aware-purple.svg)](docs/accessibility-guidelines.md)

Structured source datasets and dataset-governance tools for fine-tuning, evaluating, and preparing small local LLMs for practical technical workflows.

This repository is organized around role-specific datasets. Each dataset should define its intended model profile, training use, language, platform, source format, quality rules, risk metadata, validation requirements, and export assumptions.

## Important scope note

This repository stores source datasets. A valid JSONL file is not automatically a production-grade fine-tuning corpus.

Validation is layered:

```text
source JSONL
  -> JSON / schema validation
  -> dataset-governance linting
  -> semantic and safety review
  -> model-specific export
```

See [Dataset governance](docs/dataset-governance.md).

## Dataset registry

| Dataset | Target model | Use | Language | Platform | Records | Purpose | Status |
|---|---:|---|---|---|---:|---|---|
| [`terminal-admin-bash-master__4b-coder-instruct__sft__en__debian-ubuntu__v0.1`](datasets/terminal-admin-bash-master/README.md) | 4B coder-instruct | SFT | English | Debian/Ubuntu | 2000 | Terminal administration: Bash commands, short explanations, inspection-first operator workflows | legacy experimental corpus |
| [`terminal-admin-bash-master__4b-coder-instruct__sft__en__debian-ubuntu__v0.2`](datasets/terminal-admin-bash-master/README.md) | 4B coder-instruct | SFT | English | Debian/Ubuntu | sample only | Governed source-record format with risk metadata and quality gates | governed sample |

## Repository goals

The repository is intended to provide:

- source datasets in a stable canonical format;
- naming conventions that expose model profile, use case, language, platform, and version;
- dataset cards and per-dataset documentation;
- validation schemas and executable validation scripts;
- dataset-governance rules for safety, risk, answer style, and review status;
- quality guidelines for creating useful training records;
- documentation that remains readable and accessible without relying on visuals alone.

## Non-goals

This repository does not claim that:

- a structurally valid dataset is automatically ready for training;
- a fine-tuned terminal model is safe to run commands without runtime policy controls;
- the legacy v0.1 corpus has full semantic, safety, or execution validation;
- validation scripts can replace expert review.

## Source format

The canonical source format is JSONL with one training record per line.

Each record contains:

- `id` — stable record identifier;
- `meta` — metadata for filtering, validation, export, safety review, and documentation;
- `messages` — chat-style training content.

The repository stores source data. Training pipelines should export or template the source records for the target model family and tokenizer.

See [Dataset format](docs/dataset-format.md).

## Validation

Install development dependencies:

```bash
python -m pip install -r requirements-dev.txt
```

Validate the governed v0.2 sample:

```bash
python validation/validate_dataset.py \
  datasets/terminal-admin-bash-master/samples/terminal-admin-bash-master__4b-coder-instruct__sft__en__debian-ubuntu__v0.2.sample.jsonl \
  --schema schemas/terminal-admin-bash-master.v0.2.schema.json \
  --report validation/terminal-admin-bash-master__4b-coder-instruct__sft__en__debian-ubuntu__v0.2.sample.validation-report.md
```

For legacy corpora, use `--warn-only` while migrating metadata and reviewing records.

## Naming convention

Dataset files should follow this pattern:

```text
<role>__<target-model-profile>__<training-use>__<language>__<platform>__<version>.jsonl
```

The current full v0.1 corpus is stored with an explicit record-count suffix:

```text
terminal-admin-bash-master__4b-coder-instruct__sft__en__debian-ubuntu__v0.1.full-2000.jsonl
```

See [Naming convention](docs/naming-convention.md).

## Repository layout

```text
.
├── README.md
├── DATASET_CARD.md
├── CONTRIBUTING.md
├── LICENSE.md
├── requirements-dev.txt
├── datasets/
│   ├── README.md
│   └── terminal-admin-bash-master/
│       ├── README.md
│       ├── DATASET_CARD.md
│       ├── terminal-admin-bash-master__4b-coder-instruct__sft__en__debian-ubuntu__v0.1.full-2000.jsonl
│       └── samples/
│           ├── terminal-admin-bash-master__4b-coder-instruct__sft__en__debian-ubuntu__v0.1.sample.jsonl
│           └── terminal-admin-bash-master__4b-coder-instruct__sft__en__debian-ubuntu__v0.2.sample.jsonl
├── docs/
│   ├── accessibility-guidelines.md
│   ├── dataset-format.md
│   ├── dataset-governance.md
│   ├── naming-convention.md
│   └── quality-guidelines.md
├── schemas/
│   ├── terminal-admin-bash-master.v0.1.schema.json
│   └── terminal-admin-bash-master.v0.2.schema.json
└── validation/
    ├── README.md
    ├── validate_dataset.py
    ├── bootstrap-validation-report.md
    ├── terminal-admin-bash-master__4b-coder-instruct__sft__en__debian-ubuntu__v0.1.validation-report.md
    └── terminal-admin-bash-master__4b-coder-instruct__sft__en__debian-ubuntu__v0.2.sample.validation-report.md
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

See [Accessibility guidelines](docs/accessibility-guidelines.md), [Quality guidelines](docs/quality-guidelines.md), and [Dataset governance](docs/dataset-governance.md).

## License

Dataset content and documentation are licensed under **Creative Commons Attribution 4.0 International (CC BY 4.0)**.

See [LICENSE.md](LICENSE.md).

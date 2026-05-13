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

See [Dataset governance](docs/dataset-governance.md). The documentation map is in [docs/README.md](docs/README.md). Repository-specific publishing rules are in [Repository playbook](docs/repository-playbook.md).

## Dataset registry

| Dataset | Target model | Use | Language | Platform | Records | Purpose | Status |
|---|---:|---|---|---|---:|---|---|
| [`debian-admin-bash-sft.v1.1`](datasets/debian-admin-bash/README.md) | small Debian-admin | SFT | English | Debian/Ubuntu | 2672 | Debian/Ubuntu admin Bash SFT records with Bash tooling, incident triage, structured parsers, SQLite, defensive admin, risk metadata, and quality gates | governed draft dataset |
| [`debian-admin-bash-sft.v0.2`](datasets/debian-admin-bash/README.md) | 4B coder-instruct | SFT | English | Debian/Ubuntu | sample only | Governed source-record reference sample | governed sample |

## Deprecated / removed source material

The previous full `debian-admin-bash-sft.v0.1.full-2000.jsonl` corpus was removed from the active dataset tree because it contained faulty data and should not be treated as a valid training source.

Historical validation notes may remain for audit context, but active training work should use governed records and fresh validation reports.

## Repository goals

The repository is intended to provide:

- source datasets in a stable canonical format;
- naming conventions that expose model profile, use case, language, platform, and version;
- dataset cards and per-dataset documentation;
- validation schemas and executable validation scripts;
- dataset-governance rules for safety, risk, answer style, and review status;
- repository-specific publishing rules that keep draft waves local and push only official checkpoints;
- quality guidelines for creating useful training records;
- held-out eval and review artefacts for measuring quality separately from training data;
- documentation that remains readable and accessible without relying on visuals alone.

## Non-goals

This repository does not claim that:

- a structurally valid dataset is automatically ready for training;
- a fine-tuned terminal model is safe to run commands without runtime policy controls;
- validation scripts can replace expert review;
- draft migrated records are semantically reviewed only because they pass schema and governance linting.

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
  datasets/debian-admin-bash/samples/debian-admin-bash-sft.v0.2.sample.jsonl \
  --schema schemas/debian-admin-bash.v0.2.schema.json \
  --report validation/debian-admin-bash-sft.v0.2.sample.validation-report.md
```

Validate the governed v1.1 Debian-admin Bash dataset:

```bash
python validation/validate_dataset.py \
  datasets/debian-admin-bash/debian-admin-bash-sft.v1.1.jsonl \
  --schema schemas/debian-admin-bash.v0.2.schema.json \
  --report validation/debian-admin-bash-sft.v1.1.validation-report.md
```

## Naming convention

Dataset files should use short purpose-oriented names:

```text
<purpose>-<training-use>.<version>.jsonl
```

For this repo, the active purpose name is `debian-admin-bash`: Debian/Ubuntu administration through concise Bash-oriented assistant answers.

A dataset content version such as `v1.1` does not require a new schema when the governed source-record shape is unchanged. The current governed record-shape schema is:

```text
schemas/debian-admin-bash.v0.2.schema.json
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
│   └── debian-admin-bash/
│       ├── README.md
│       ├── DATASET_CARD.md
│       ├── debian-admin-bash-sft.v1.1.jsonl
│       ├── evals/
│       ├── preferences/
│       ├── review/
│       ├── debian-admin-bash-sft.v0.3-to-v0.4.migration-notes.md
│       ├── debian-admin-bash-sft.v0.4-to-v0.5.migration-notes.md
│       ├── debian-admin-bash-sft.v0.5-to-v0.6.migration-notes.md
│       ├── debian-admin-bash-sft.v0.6-to-v0.7.migration-notes.md
│       ├── debian-admin-bash-sft.v0.7-to-v0.8.migration-notes.md
│       ├── debian-admin-bash-sft.v0.8-to-v0.9.migration-notes.md
│       ├── debian-admin-bash-sft.v0.9-to-v1.0.migration-notes.md
│       ├── debian-admin-bash-sft.v1.0-to-v1.1.migration-notes.md
│       └── samples/
│           ├── debian-admin-bash-sft.v0.1.sample.jsonl
│           └── debian-admin-bash-sft.v0.2.sample.jsonl
├── docs/
│   ├── README.md
│   ├── accessibility-guidelines.md
│   ├── dataset-format.md
│   ├── dataset-governance.md
│   ├── naming-convention.md
│   ├── quality-guidelines.md
│   └── repository-playbook.md
├── schemas/
│   ├── debian-admin-bash.v0.1.schema.json
│   └── debian-admin-bash.v0.2.schema.json
├── scripts/
│   ├── build_quality_artifacts.py
│   ├── build_preference_set.py
│   ├── build_review_subset.py
│   ├── run_eval.py
│   └── run_sandbox_checks.py
└── validation/
    ├── README.md
    ├── VALIDATION_PROVENANCE.md
    ├── validate_dataset.py
    ├── validate_preference_dataset.py
    ├── bootstrap-validation-report.md
    ├── debian-admin-bash-sft.v0.1.historical.validation-report.md
    ├── debian-admin-bash-sft.v0.2.sample.validation-report.md
    ├── debian-admin-bash-sft.v1.1.validation-report.md
    ├── debian-admin-bash-sft.v1.1.quality-audit.md
    ├── debian-admin-bash-eval.v0.1.validation-report.md
    ├── debian-admin-bash-multiturn-eval.v0.1.validation-report.md
    ├── debian-admin-bash-eval.v0.1.heuristic-score.md
    ├── debian-admin-bash-sft.v1.1.sandbox-checks.md
    ├── debian-admin-bash-sft.v1.1.review-candidates.validation-report.md
    └── debian-admin-bash-preference.v0.1.validation-report.md
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

See [Documentation map](docs/README.md), [Accessibility guidelines](docs/accessibility-guidelines.md), [Quality guidelines](docs/quality-guidelines.md), and [Dataset governance](docs/dataset-governance.md).

## License

Dataset content and documentation are licensed under **Creative Commons Attribution 4.0 International (CC BY 4.0)**.

See [LICENSE.md](LICENSE.md).

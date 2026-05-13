# LLM Fine-Tuning Datasets

[![License: CC BY 4.0](https://img.shields.io/badge/license-CC--BY--4.0-blue.svg)](LICENSE.md)
[![Format: JSONL messages](https://img.shields.io/badge/format-JSONL%20messages-green.svg)](docs/dataset-format.md)
[![Governance: quality gates](https://img.shields.io/badge/governance-quality%20gates-orange.svg)](docs/dataset-governance.md)
[![Docs: WCAG-aware](https://img.shields.io/badge/docs-WCAG--aware-purple.svg)](docs/accessibility-guidelines.md)

Structured source datasets and dataset-governance tools for fine-tuning, evaluating, and preparing small local LLMs for practical technical workflows.

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

See [Dataset governance](docs/dataset-governance.md), [Quality guidelines](docs/quality-guidelines.md), and the repository-specific [Repository playbook](docs/repository-playbook.md).

## Dataset registry

| Dataset | Target model | Use | Language | Platform | Records | Status |
|---|---:|---|---|---|---:|---|
| [`debian-admin-bash-sft`](datasets/debian-admin-bash/README.md) | small Debian-admin | SFT | English | Debian/Ubuntu | 2836 | governed draft dataset |
| [`debian-admin-bash` eval/review artifacts](datasets/debian-admin-bash/README.md) | small Debian-admin | eval/review/preference | English | Debian/Ubuntu | 680 companion records | draft quality artifacts |

Current SFT file:

```text
datasets/debian-admin-bash/debian-admin-bash-sft.jsonl
```

The current content checkpoint is `v1.2`; the filename is stable so public `main` does not accumulate full JSONL snapshots for every checkpoint.

## Repository goals

This repository provides:

- source datasets in a stable JSONL message format;
- schemas and validators for dataset-governance metadata;
- concise dataset cards and README files focused on the current public state;
- a changelog for checkpoint history instead of many small per-version notes;
- held-out eval, review-candidate, sandbox, and preference artifacts;
- clear non-claims about review status and production readiness.

## Non-goals

This repository does not claim that:

- a structurally valid dataset is automatically ready for training;
- a fine-tuned terminal model is safe to run commands without runtime policy controls;
- validation scripts can replace expert semantic and safety review;
- draft migrated records are reviewed only because they pass schema and governance linting.

## Validate the current dataset

Install development dependencies:

```bash
python -m pip install -r requirements-dev.txt
```

Validate the current Debian-admin Bash SFT file:

```bash
python validation/validate_dataset.py \
  datasets/debian-admin-bash/debian-admin-bash-sft.jsonl \
  --schema schemas/debian-admin-bash.v0.2.schema.json \
  --report validation/debian-admin-bash-sft.validation-report.md
```

Run companion gates:

```bash
python validation/validate_dataset.py \
  datasets/debian-admin-bash/review/review-candidates.jsonl \
  --schema schemas/debian-admin-bash.v0.2.schema.json \
  --report validation/debian-admin-bash-review-candidates.validation-report.md

python validation/validate_preference_dataset.py \
  datasets/debian-admin-bash/preferences/preference.jsonl \
  --report validation/debian-admin-bash-preference.validation-report.md

python scripts/run_eval.py
python scripts/run_sandbox_checks.py
```

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
│       ├── CHANGELOG.md
│       ├── debian-admin-bash-sft.jsonl
│       ├── evals/
│       ├── preferences/
│       ├── review/
│       └── samples/
├── docs/
├── schemas/
├── scripts/
└── validation/
```

## Documentation map

- [docs/README.md](docs/README.md) — canonical documentation index.
- [datasets/debian-admin-bash/README.md](datasets/debian-admin-bash/README.md) — current dataset and companion artifacts.
- [datasets/debian-admin-bash/DATASET_CARD.md](datasets/debian-admin-bash/DATASET_CARD.md) — dataset card for current public state.
- [datasets/debian-admin-bash/CHANGELOG.md](datasets/debian-admin-bash/CHANGELOG.md) — checkpoint history.
- [validation/README.md](validation/README.md) — validation commands and report index.

## License

Dataset content and documentation are licensed under **Creative Commons Attribution 4.0 International (CC BY 4.0)**.

See [LICENSE.md](LICENSE.md).

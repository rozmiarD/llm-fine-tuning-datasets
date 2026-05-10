# Validation

This directory contains validation scripts, validation notes, and validation reports.

## Validation layers

Validation is layered.

```text
JSON parse
  -> JSON Schema
  -> governance lint
  -> semantic and safety review
```

The validator can catch many common dataset defects, but it does not prove that a record is correct or safe.

## Current schemas

| Schema | Scope |
|---|---|
| `schemas/terminal-admin-bash-master.v0.1.schema.json` | Legacy v0.1 source records. |
| `schemas/terminal-admin-bash-master.v0.2.schema.json` | Governed v0.2 source records with risk, safety, answer-style, and review metadata. |

## Validator

Executable validator:

```text
validation/validate_dataset.py
```

Install dependencies:

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

Validate a legacy corpus without failing the migration run:

```bash
python validation/validate_dataset.py \
  datasets/terminal-admin-bash-master/terminal-admin-bash-master__4b-coder-instruct__sft__en__debian-ubuntu__v0.1.full-2000.jsonl \
  --schema schemas/terminal-admin-bash-master.v0.1.schema.json \
  --warn-only
```

## What the validator checks

The validator checks:

- JSONL parseability;
- JSON Schema conformance when a schema is provided;
- duplicate IDs;
- exact duplicate user/assistant task pairs;
- one-user-message and one-assistant-message SFT shape;
- final assistant message position;
- Debian/Ubuntu package-manager drift;
- risky Bash/Linux patterns that require higher risk metadata;
- elevated-privilege mismatches;
- side-effect metadata mismatches;
- warning metadata for higher-risk examples;
- basic answer-style consistency;
- review-status honesty.

## What the validator does not prove

The validator does not prove that:

- the command is the best command;
- the command has been executed successfully;
- the answer is semantically correct;
- the dataset is production-grade;
- a trained model will behave safely without runtime controls.

## Reports

| Report | Scope | Status |
|---|---|---|
| [Bootstrap validation report](bootstrap-validation-report.md) | Initial repository structure and sample consistency | pass |
| [v0.1 validation report](terminal-admin-bash-master__4b-coder-instruct__sft__en__debian-ubuntu__v0.1.validation-report.md) | Legacy full corpus structural validation | legacy structural pass |
| [v0.2 sample validation report](terminal-admin-bash-master__4b-coder-instruct__sft__en__debian-ubuntu__v0.2.sample.validation-report.md) | Governed sample schema and governance validation | pass |

## Migration rule

Do not treat a legacy v0.1 pass as production readiness.

Before using records for training, migrate them to v0.2 metadata and run governance validation. High-risk or ambiguous records should be reviewed, quarantined, or rejected.

# Bootstrap Validation Report

## Scope

This historical report covers the initial repository structure and documentation consistency after the bootstrap cleanup. For current active dataset validation, see `debian-admin-bash-sft.v0.5.validation-report.md`.

Validated areas:

- root README is general repository documentation;
- dataset-specific documentation is placed under `datasets/debian-admin-bash/`;
- `datasets/README.md` exists to make the dataset directory explicit;
- dataset naming follows the documented convention;
- sample JSONL file name matches the dataset identity;
- sample JSONL records match the intended metadata pattern;
- JSON Schema exists for the current dataset family;
- root dataset card is an index, not a duplicated per-dataset card;
- per-dataset card exists next to the dataset README.

## Repository structure check

Expected structure:

```text
.
├── README.md
├── DATASET_CARD.md
├── CONTRIBUTING.md
├── LICENSE.md
├── datasets/
│   ├── README.md
│   └── debian-admin-bash/
│       ├── README.md
│       ├── DATASET_CARD.md
│       ├── debian-admin-bash-sft.v0.5.jsonl
│       └── samples/
│           ├── debian-admin-bash-sft.v0.1.sample.jsonl
│           └── debian-admin-bash-sft.v0.2.sample.jsonl
├── docs/
│   ├── README.md
│   ├── accessibility-guidelines.md
│   ├── dataset-format.md
│   ├── naming-convention.md
│   └── quality-guidelines.md
├── schemas/
│   ├── debian-admin-bash.v0.1.schema.json
│   └── debian-admin-bash.v0.2.schema.json
└── validation/
    ├── README.md
    └── bootstrap-validation-report.md
```

Status: pass.

## Naming check

Canonical dataset name:

```text
debian-admin-bash-sft.v0.1
```

Sample file:

```text
datasets/debian-admin-bash/samples/debian-admin-bash-sft.v0.1.sample.jsonl
```

Status: pass.

## Metadata check

Current sample records use:

```text
role: debian-admin-bash
target_model_size: 4b
target_model_type: coder-instruct
training_use: sft
language: en
platform: debian-ubuntu
```

Status: pass.

## Documentation separation check

Root README:

- describes repository-level goals;
- links to format, naming, quality, and accessibility docs;
- includes a dataset registry table with a Purpose column;
- avoids detailed dataset-specific implementation guidance.

Dataset README:

- describes the concrete dataset identity;
- states target model profile;
- states platform assumptions;
- states task types and answer style rules.

Status: pass.

## Accessibility-style check

Documentation uses:

- descriptive headings;
- plain language;
- copyable code blocks;
- meaningful link text;
- text equivalents for badge information.

Status: pass.

## Historical follow-up status

The original bootstrap follow-ups are complete enough for the current repository shape:

- JSONL/schema/governance validation now lives in `validation/validate_dataset.py`;
- the active governed dataset is `datasets/debian-admin-bash/debian-admin-bash-sft.v0.5.jsonl`;
- current validation reports live under `validation/`;
- future schema splits should still happen only when record shape or governance semantics change.

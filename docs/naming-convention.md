# Naming Convention

## Public artifact rule for this repository

For `llm-fine-tuning-datasets`, the current public full dataset file should use a stable purpose-oriented name:

```text
<purpose>-<training-use>.jsonl
```

Example:

```text
datasets/debian-admin-bash/debian-admin-bash-sft.jsonl
```

The dataset content version belongs in record metadata, validation reports, dataset cards, and the changelog, not necessarily in the active filename.

Current content checkpoint:

```text
meta.dataset_version = "1.2"
```

This avoids cluttering `main` with full JSONL snapshots for every checkpoint. Historical checkpoint summaries belong in `datasets/debian-admin-bash/CHANGELOG.md` and git history.

## Samples and companion artifacts

Samples may keep explicit version labels when they are retained as reference examples:

```text
<purpose>-<training-use>.<version>.sample.jsonl
```

Companion artifacts should use stable role names inside their directories:

```text
evals/single-turn.jsonl
evals/multiturn.jsonl
review/review-candidates.jsonl
preferences/preference.jsonl
```

## Field meanings

### purpose

The behavior or capability the dataset trains.

Example:

```text
debian-admin-bash
```

This name means the dataset is for Debian/Ubuntu administration through concise Bash-oriented assistant answers.

### training-use

The expected use of the file.

Allowed initial values:

- `sft`;
- `eval`;
- `preference`;
- `rag`;
- `tool-calling`.

The first dataset uses:

```text
sft
```

### metadata axes

Do not put every axis into the file name. Keep these in `meta` and dataset cards:

- language;
- platform;
- target model profile;
- review status;
- schema version;
- content version;
- detailed source lineage.

### content version

Use dataset content versioning in metadata and changelog entries:

```text
v1.2
```

Increase the content version when scope, source data, record quality rules, or intended training use changes significantly. A dataset content version does not require a new JSON Schema version when the governed record shape is unchanged.

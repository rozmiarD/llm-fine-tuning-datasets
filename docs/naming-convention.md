# Naming Convention

## Dataset file pattern

Use short purpose-oriented names:

```text
<purpose>-<training-use>.<version>.jsonl
```

For sample files:

```text
<purpose>-<training-use>.<version>.sample.jsonl
```

Current purpose names should describe what the data trains, not every metadata axis. Keep target model, language, platform, and review status in metadata and dataset cards.

## Current active datasets

Active governed draft dataset:

```text
debian-admin-bash-sft.v0.6.jsonl
```

Governed reference sample:

```text
debian-admin-bash-sft.v0.2.sample.jsonl
```

Historical v0.1 material is retained only as samples or validation context, not as an active full corpus.

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
- detailed source lineage.

### version

Use dataset content versioning:

```text
v0.6
```

Increase the version when scope, source data, record quality rules, or intended training use changes significantly. A dataset content version does not require a new JSON Schema version when the governed record shape is unchanged.

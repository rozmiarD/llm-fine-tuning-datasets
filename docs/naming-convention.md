# Naming Convention

## Dataset file pattern

Use this pattern:

```text
<role>__<target-model-profile>__<training-use>__<language>__<platform>__<version>.jsonl
```

For sample files:

```text
<role>__<target-model-profile>__<training-use>__<language>__<platform>__<version>.sample.jsonl
```

## Current active datasets

Active governed draft dataset:

```text
terminal-admin-bash-master__small-terminal-admin__sft__en__debian-ubuntu__v0.3.governed-bash-heavy.jsonl
```

Governed reference sample:

```text
terminal-admin-bash-master__4b-coder-instruct__sft__en__debian-ubuntu__v0.2.sample.jsonl
```

Historical v0.1 material is retained only as samples or validation context, not as an active full corpus.

## Field meanings

### role

The behavior or capability the dataset trains.

Example:

```text
terminal-admin-bash-master
```

### target-model-profile

The intended model size and type.

Example:

```text
4b-coder-instruct
```

This does not mean only one exact model can use the data. It states the optimization target.

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

### language

Use ISO-like short names.

Current value:

```text
en
```

### platform

The operating-system or runtime target.

Current value:

```text
debian-ubuntu
```

Other possible future values:

- `common-linux`;
- `cross-distro`;
- `rhel-fedora`;
- `alpine-busybox`;
- `arch-linux`;
- `raspberry-pi-os`.

### version

Use dataset content versioning:

```text
v0.3
```

Increase the version when scope, source data, record quality rules, or intended training use changes significantly. A dataset content version does not require a new JSON Schema version when the governed record shape is unchanged.

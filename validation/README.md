# Validation

This directory contains validation notes and validation reports.

## Current validation approach

The current structure includes a JSON Schema:

```text
schemas/terminal-admin-bash-master.v0.1.schema.json
```

Dataset records should be valid JSONL and each line should conform to that schema.

## Reports

| Report | Scope | Status |
|---|---|---|
| [Bootstrap validation report](bootstrap-validation-report.md) | Initial repository structure and sample consistency | pass |
| [terminal-admin-bash-master v0.1 validation report](terminal-admin-bash-master__4b-coder-instruct__sft__en__debian-ubuntu__v0.1.validation-report.md) | Expanded 2000-record canonical JSONL corpus | pass |

## Suggested future script

A future script may check:

- each line is valid JSON;
- required fields exist;
- `messages` contains valid roles;
- the last message is usually `assistant`;
- `meta.role` matches the dataset directory;
- `meta.language` matches the file name;
- `meta.platform` matches the file name;
- IDs are unique;
- tags are lowercase;
- assistant answer contains a Bash code block when task type requires commands.

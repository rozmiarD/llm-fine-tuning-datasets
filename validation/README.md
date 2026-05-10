# Validation

This directory is reserved for validation notes and future validation scripts.

## Current validation approach

The current bootstrap structure includes a JSON Schema:

```text
schemas/terminal-admin-bash-master.v0.1.schema.json
```

Dataset records should be valid JSONL and each line should conform to that schema.

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

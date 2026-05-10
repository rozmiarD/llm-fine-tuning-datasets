# Contributing

## Contribution goals

Contributions should improve the quality, consistency, or coverage of the dataset.

Good contributions include:

- realistic Debian/Ubuntu administration tasks;
- examples with actual command output or error output;
- concise command-first answers;
- corrections to inaccurate commands;
- improved metadata consistency;
- validation improvements;
- better migration notes and validation reports.

## Language

All dataset records should be written in English unless a future dataset explicitly declares another language in its file name and metadata.

## Style

Use direct, technical language.

Avoid:

- marketing claims;
- exaggerated AI language;
- long tutorial-style answers;
- vague prompts;
- dangerous commands without context;
- distro-mixed command sequences unless the task is explicitly cross-distro;
- claims that schema validation equals production readiness.

## Record requirements

New governed records should use the current governed source-record shape defined by:

```text
schemas/terminal-admin-bash-master.v0.2.schema.json
```

Every governed record must include:

- stable `id`;
- `meta.dataset_version`;
- `meta.task_type`;
- `meta.language`;
- `meta.domain`;
- `meta.subdomain`;
- `meta.target_os`;
- `meta.difficulty`;
- `meta.risk_level`;
- `meta.requires_root`;
- `meta.answer_style`;
- `meta.tags`;
- `meta.safety`;
- `meta.review`;
- `messages`.

The preferred SFT shape is:

```text
system -> user -> assistant
```

The final message should be an assistant answer.

For current governance linting, keep records to one user message and one assistant message. Split multi-turn source conversations into separate single-pair SFT records unless a future schema and validator explicitly support multi-turn training records.

## Metadata rules

Use `meta.dataset_version` for the dataset content version, for example `0.2` for the governed reference sample or `0.3` for the active cleaned Bash-heavy dataset.

Use the existing v0.2 schema when the governed record shape is unchanged. Do not create a new schema only because dataset content moved from `0.2` to `0.3`.

Preserve source lineage under `meta.source` when records were migrated from generated, cleaned, or external source material.

Create a new schema version only when the governed record shape changes, for example new required fields, changed enum meanings, or a materially different review/safety model.

## Risk and safety rules

Use the documented risk levels conservatively:

- `safe_readonly`;
- `state_change_low`;
- `state_change_high`;
- `network_sensitive`;
- `privilege_sensitive`;
- `security_sensitive`;
- `destructive`.

Set `meta.requires_root=true` when the assistant answer uses `sudo`, `doas`, `su -`, or otherwise requires elevated privileges.

Do not mark a record as `safe_readonly` when the assistant answer changes packages, services, firewall rules, routing, users, permissions, filesystems, disks, or other host state.

Use `meta.safety.has_side_effects=true` when the assistant answer intentionally changes host state.

Use `meta.safety.warning_required=true` and `meta.safety.warning_present=true` when the operation can disrupt services, networking, access, users, disks, or permissions.

## Review rules

Use review status honestly:

- `draft`: generated, migrated, or edited but not yet manually checked;
- `reviewed`: semantic and safety review completed;
- `quarantined`: likely problematic; keep for audit but do not train;
- `rejected`: do not use for training.

Do not mark records as `reviewed` just because they pass JSON Schema or governance linting.

Do not claim execution validation unless the command or procedure was actually executed or manually validated in the stated mode.

## Preferred assistant answer

````text
```bash
command here
```
Short factual explanation here.
````

For destructive or state-changing commands, prefer inspection first unless the user explicitly asks for the change.

For higher-risk operations, use guarded procedure language, a warning, a dry-run, a backup step, or a rollback note when appropriate.

For unsafe requests, use `refusal_with_safe_alternative` and provide a safer path.

## Review checklist

Before adding records, check:

- Is the command valid on Debian/Ubuntu?
- Is the explanation short and factual?
- Does the record avoid unnecessary alternatives?
- Is the platform correctly marked?
- Is the command destructive or state-changing?
- If destructive or state-changing, is the risk metadata correct?
- If elevated privileges are used, is `requires_root=true`?
- If a warning is required, is it present in the assistant answer?
- Are tags useful for filtering?
- Does the example teach something specific?
- Is review status honest?

## Validation before commit

Install development dependencies:

```bash
python -m pip install -r requirements-dev.txt
```

Validate a governed JSONL file:

```bash
python validation/validate_dataset.py \
  datasets/terminal-admin-bash-master/<dataset-file>.jsonl \
  --schema schemas/terminal-admin-bash-master.v0.2.schema.json \
  --report validation/<dataset-file>.validation-report.md
```

Use `--warn-only` only for legacy migration work where failures are expected and must be reviewed.

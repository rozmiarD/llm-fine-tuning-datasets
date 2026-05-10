# Dataset validation report

- Dataset: `datasets/terminal-admin-bash-master/terminal-admin-bash-master__small-terminal-admin__sft__en__debian-ubuntu__v0.3.governed-bash-heavy.jsonl`
- Schema: `schemas/terminal-admin-bash-master.v0.2.schema.json`
- Records: 908
- JSON errors: 0
- Schema errors: 0
- Governance lint errors: 0
- Warnings: 0
- Status: PASSED

## Distribution counters

### difficulty

- `advanced`: 353
- `beginner`: 314
- `intermediate`: 241

### risk_level

- `destructive`: 2
- `network_sensitive`: 7
- `privilege_sensitive`: 19
- `safe_readonly`: 728
- `security_sensitive`: 37
- `state_change_high`: 18
- `state_change_low`: 97

### answer_style

- `command_with_brief_explanation`: 387
- `diagnostic_steps`: 217
- `guarded_procedure`: 110
- `refusal_with_safe_alternative`: 100
- `script_with_explanation`: 94

### review_status

- `draft`: 908

### subdomain

- `advanced_diagnostics`: 55
- `docker`: 53
- `filesystem`: 44
- `logs`: 22
- `networking`: 69
- `packages`: 48
- `permissions`: 24
- `processes`: 16
- `safety`: 21
- `scripting`: 68
- `security`: 18
- `structured_output`: 66
- `systemd`: 145
- `terminal`: 224
- `tool_availability`: 35

## JSON errors

None.

## Schema errors

None.

## Governance lint errors

None.

## Warnings

None.

## Notes

- This report covers the governed v0.3 Bash-heavy dataset.
- The dataset uses `meta.dataset_version="0.3"` while validating against the existing governed record-shape schema: `schemas/terminal-admin-bash-master.v0.2.schema.json`.
- This does not create a new schema generation. The schema version describes the governed record shape; the dataset version describes the dataset content.
- All records remain `review.status=draft`; schema/lint pass is not a claim of semantic, safety, or execution review.

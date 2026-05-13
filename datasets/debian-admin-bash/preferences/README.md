# Debian-admin Bash preference set

This directory contains a small draft preference dataset for bad-vs-good Debian/Ubuntu terminal-admin behavior.

It is not SFT training data and does not use the governed `messages` shape. Each record contains:

- `prompt.system`;
- `prompt.user`;
- `chosen`;
- `rejected`;
- `rationale`.

## File

| File | Records | Purpose |
|---|---:|---|
| `debian-admin-bash-preference.v0.1.jsonl` | 60 | Preference examples for inspection-first, safe-first behavior. |

## Scope

The preference set targets common unsafe shortcuts:

- deleting package-manager locks;
- restarting services before validation;
- broad log deletion;
- `chmod 777` permission fixes;
- opening firewall ports before listener checks;
- restoring over live data without dry-run;
- disabling security controls;
- killing broad process names;
- copying live SQLite files unsafely;
- restarting Docker stacks before identifying the conflict.

## Review status

All preference records are draft. They are intended for review and preference-training experiments, not as a production-safety claim.

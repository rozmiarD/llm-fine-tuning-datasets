# Debian-admin Bash preference set

This directory contains a draft preference dataset for bad-vs-good Debian/Ubuntu terminal-admin behavior.

It is not SFT training data and does not use the governed `messages` shape. Each record contains:

- `prompt.system`;
- `prompt.user`;
- `chosen`;
- `rejected`;
- `rationale`.

## File

| File | Records | Purpose |
|---|---:|---|
| `preference.jsonl` | 200 | Preference examples for inspection-first, safe-first behavior. |

## Scope

The preference set targets common unsafe shortcuts: deleting package-manager locks, restarting before validation, broad log/config/backup deletion, world-writable permissions, firewall changes before listener checks, restore-over-live, disabling security controls, broad process kills, unsafe SQLite copies, Docker prune/down shortcuts, sudoers overgranting, curl-to-shell installers, remote netplan apply, and destructive VirtualBox actions.

## Review status

All preference records are draft. They are intended for review and preference-training experiments, not as a production-safety claim.

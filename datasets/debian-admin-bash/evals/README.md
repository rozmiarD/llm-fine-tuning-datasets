# Debian-admin Bash evals

This directory contains held-out evaluation records for the `debian-admin-bash` dataset family.

These files are not training data. They are intended to test whether a small Debian/Ubuntu admin model can interpret realistic terminal evidence, choose one safe first verification command, and avoid premature state changes.

## Files

| File | Records | Purpose |
|---|---:|---|
| `single-turn.jsonl` | 80 | Single-turn held-out evidence-to-command evaluation records. |
| `multiturn.jsonl` | 40 | Multi-turn continuation evals encoded as single user prompts so they remain compatible with the current governed record shape. |

## Format

Eval files use the same governed JSONL shape as source records and set `meta.task_type="eval"`.

The multi-turn eval file does not change the SFT schema. Previous turns are embedded in the user prompt and the assistant message is the expected next response.

## Non-claims

These evals are draft reference answers. Passing schema and governance validation does not prove model quality or production safety.

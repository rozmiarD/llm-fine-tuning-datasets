# Dataset Card: debian-admin-bash

## Summary

`debian-admin-bash` is a governed draft source dataset for concise Debian/Ubuntu terminal-administration assistants.

Current public SFT file:

```text
datasets/debian-admin-bash/debian-admin-bash-sft.jsonl
```

The current content checkpoint is `v1.2`, but the file name is stable on purpose. Historical full JSONL snapshots are tracked by git history and summarized in [CHANGELOG.md](CHANGELOG.md), not kept as active public files.

## Current metadata

| Field | Value |
|---|---|
| Dataset family | `debian-admin-bash-sft` |
| Current file | `debian-admin-bash-sft.jsonl` |
| Content checkpoint | `v1.2` |
| Records | `2836` |
| SHA-256 | `e021ee617322960579776f38cd71443ff5027df29b369c9e257ea0025e93aa2a` |
| Schema | `schemas/debian-admin-bash.v0.2.schema.json` |
| Review status | `draft` |
| Validation report | `validation/debian-admin-bash-sft.validation-report.md` |

## Intended use

Supervised fine-tuning and evaluation research for small coder-instruct or terminal-administration models.

The records emphasize:

- Debian/Ubuntu systems;
- Bash command generation;
- concise command-first answers;
- inspection before mutation;
- systemd, apt/dpkg, permissions, backup/restore, SSH/auth, Docker, bounded local VirtualBox administration, networking, logs, incident triage, Bash tooling, structured outputs, and SQLite workflows;
- refusals or safe alternatives for unsafe administrative shortcuts.

## Active companion artifacts

| Artifact | File | Purpose |
|---|---|---|
| Review candidates | `review/review-candidates.jsonl` | Candidate subset for manual semantic/safety review |
| Single-turn eval | `evals/single-turn.jsonl` | Held-out reference eval prompts |
| Multi-turn eval | `evals/multiturn.jsonl` | Held-out continuation-style eval prompts |
| Preference examples | `preferences/preference.jsonl` | Bad-vs-good safe-first examples |
| Governed sample | `samples/debian-admin-bash-sft.v0.2.sample.jsonl` | Small record-shape reference sample |

## Production-readiness statement

This dataset is **not production-ready by validation alone**.

All SFT records remain `review.status="draft"` until semantic review, safety review, and any required execution validation are complete. The validation tooling checks JSON, schema, governance metadata, and selected mechanical properties; it does not prove command correctness or runtime safety.

## Known limitations

- The dataset contains generated/curated draft records that need manual review before high-trust use.
- Some repeated templates remain and should be deduplicated or diversified during review.
- Sandbox triage intentionally blocks many host-admin commands rather than executing them.
- SQLite is the scoped database surface; PostgreSQL is intentionally excluded.
- VirtualBox coverage is bounded to local host VM administration, not broad cloud or enterprise virtualization.
- Training pipelines must still apply model-specific formatting, sampling, and runtime policy controls.

## Recommended next steps before training

1. Review high-risk records first: destructive, security-sensitive, privilege-sensitive, and state-changing records.
2. Prefer reviewed subsets over the full draft set for early training.
3. Use the held-out eval and preference files to check safe-first behavior.
4. Re-run validation and sandbox triage after any data edits.
5. Export only the reviewed subset or clearly label draft training experiments.

## License

Repository-level licensing applies. See `LICENSE.md`.

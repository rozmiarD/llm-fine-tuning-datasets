# Validation provenance

This file records who/what performed validation and review-related analysis for the current Debian-admin Bash dataset artefacts.

## Current validation wave

Date: 2026-05-13

Repository state: local draft commits ahead of `origin/main`; not pushed as an official remote checkpoint.

## Automated validators

The following checks are deterministic local tooling, not model judgment:

- `validation/validate_dataset.py`
  - JSONL parsing;
  - JSON Schema validation;
  - governance linting;
  - duplicate/task-pair checks;
  - metadata consistency checks.
- `validation/validate_preference_dataset.py`
  - preference JSONL structure;
  - chosen/rejected separation;
  - basic unsafe-shortcut detection.
- `scripts/run_eval.py`
  - heuristic safe-first eval scoring;
  - reference-answer self-check.
- `scripts/run_sandbox_checks.py`
  - Bash code-block extraction;
  - `bash -n` syntax checks;
  - conservative local/bwrap sandbox triage;
  - fixture-safe execution only for allowlisted commands;
  - blocked/static/manual-review classification for host-affecting commands.

## Model-assisted curation / audit

The dataset quality audit, review-candidate selection strategy, eval/preference design, and sandbox triage interpretation were produced with AI assistance in OpenClaw.

Model visible from OpenClaw session status at the time of this validation wave:

```text
model: openai-codex/gpt-5.5
fallback: openai-codex/gpt-5.4
reasoning / think mode: medium
text verbosity: low
execution mode: direct, elevated runtime available
```

Do not interpret this as a full independent semantic review by that model. The model helped design, generate, triage, and document artefacts; deterministic validators and sandbox checks produced the pass/fail counts.

## Review claim boundary

Current SFT records remain:

```text
review.status = draft
```

The following are not yet claimed:

- human semantic review of all records;
- human safety review of all records;
- execution validation of all records;
- production readiness;
- proof that a trained model will behave safely without runtime controls.

## How to upgrade provenance later

When a stronger review run happens, record:

- model/provider/version or human reviewer identity class;
- reasoning/effort mode, if applicable;
- prompt or rubric path;
- dataset file and SHA-256;
- exact commands run;
- container/image or sandbox backend;
- reviewed record IDs;
- pass/fail/quarantine counts;
- known limitations.

For example:

```text
semantic reviewer: GPT-5.5 high/xhigh or named human reviewer
rubric: datasets/debian-admin-bash/review/REVIEW_PLAN.md
input: datasets/debian-admin-bash/review/debian-admin-bash-sft.v1.1.review-candidates.jsonl
sandbox: bwrap + tempdir fixtures / container image <digest>
result: reviewed=<n>, quarantined=<n>, rejected=<n>
```

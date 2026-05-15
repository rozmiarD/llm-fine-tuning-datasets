# Validation

This directory contains validation scripts, validation provenance, and current validation reports.

## Validation provenance

The current validation/model provenance is recorded in [Validation provenance](VALIDATION_PROVENANCE.md).

Short version: deterministic scripts produce the validation, eval, and sandbox counts. Model-assisted curation and audit were performed in OpenClaw with `openai-codex/gpt-5.5`, intended/current think mode `xhigh`, text verbosity `low`; an earlier status read briefly reported `medium`, so provenance records that ambiguity. This is not a claim of full independent semantic/human review.

## Validation layers

```text
JSON parse
  -> JSON Schema
  -> governance lint
  -> mechanical eval/sandbox checks where applicable
  -> semantic and safety review
```

The validator can catch many common dataset defects, but it does not prove that a record is correct or safe.

## Current schemas

| Schema | Scope |
|---|---|
| `schemas/debian-admin-bash.v0.1.schema.json` | Legacy v0.1 source shape, retained only for historical context. |
| `schemas/debian-admin-bash.v0.2.schema.json` | Governed record-shape schema for Debian/Ubuntu admin Bash records with risk, safety, answer-style, and review metadata. |

The current Debian-admin Bash SFT file uses `meta.dataset_version="1.2"`, but it still validates against `schemas/debian-admin-bash.v0.2.schema.json` because the governed record shape did not change.

## Commands

Install dependencies:

```bash
python -m pip install -r requirements-dev.txt
```

Validate the current SFT dataset:

```bash
python validation/validate_dataset.py \
  datasets/debian-admin-bash/debian-admin-bash-sft.jsonl \
  --schema schemas/debian-admin-bash.v0.2.schema.json \
  --report validation/debian-admin-bash-sft.validation-report.md
```

Validate companion JSONL files:

```bash
python validation/validate_dataset.py \
  datasets/debian-admin-bash/evals/single-turn.jsonl \
  --schema schemas/debian-admin-bash.v0.2.schema.json \
  --report validation/debian-admin-bash-eval.validation-report.md

python validation/validate_dataset.py \
  datasets/debian-admin-bash/evals/multiturn.jsonl \
  --schema schemas/debian-admin-bash.v0.2.schema.json \
  --report validation/debian-admin-bash-multiturn-eval.validation-report.md

python validation/validate_dataset.py \
  datasets/debian-admin-bash/review/review-candidates.jsonl \
  --schema schemas/debian-admin-bash.v0.2.schema.json \
  --report validation/debian-admin-bash-review-candidates.validation-report.md
```

Validate preference examples:

```bash
python validation/validate_preference_dataset.py \
  datasets/debian-admin-bash/preferences/preference.jsonl \
  --report validation/debian-admin-bash-preference.validation-report.md
```

Generate and validate the LiteCoder-Terminal-SFT style export:

```bash
python scripts/convert_to_litecoder_terminal_sft.py \
  datasets/debian-admin-bash/debian-admin-bash-sft.jsonl \
  datasets/debian-admin-bash/debian-admin-bash-litecoder-terminal-sft.json

python validation/validate_litecoder_terminal_sft.py \
  datasets/debian-admin-bash/debian-admin-bash-litecoder-terminal-sft.json \
  --report validation/debian-admin-bash-litecoder-terminal-sft.validation-report.md
```

Run eval, sandbox, and review-state checks:

```bash
python scripts/run_eval.py \
  --report validation/debian-admin-bash-eval.heuristic-score.md

python scripts/run_sandbox_checks.py \
  --backend bwrap \
  --jsonl validation/debian-admin-bash-review-candidates.sandbox-checks.jsonl \
  --report validation/debian-admin-bash-review-candidates.sandbox-checks.md

python scripts/review_state.py status
```

The sandbox checker is conservative. It runs syntax checks for extracted Bash blocks, executes only allowlisted fixture-safe commands, and classifies host-admin commands as `static_only` or `blocked` with a suggested next review action.

The review-state checker is not a semantic reviewer. It computes canonical record hashes and detects stale `reviewed` markers so unchanged records and already-checked families do not consume review effort again.

## What the validator checks

- JSONL parseability;
- JSON Schema conformance when a schema is provided;
- duplicate IDs;
- exact duplicate user/assistant task pairs;
- one-user-message and one-assistant-message SFT shape;
- final assistant message position;
- Debian/Ubuntu package-manager drift;
- risky Bash/Linux patterns that require higher risk metadata;
- elevated-privilege mismatches through `requires_root`;
- side-effect metadata mismatches;
- warning metadata for higher-risk state-changing examples;
- basic answer-style consistency;
- review-status honesty;
- stale hash-bound review markers when `scripts/review_state.py status` is run.

## What validation does not prove

Validation does not prove that:

- the command is the best command;
- the command has been executed successfully;
- the answer is semantically correct;
- the dataset is production-grade;
- a trained model will behave safely without runtime controls.

## Current reports

| Report | Scope | Status |
|---|---|---|
| [Validation provenance](VALIDATION_PROVENANCE.md) | Validator/tool/model provenance and review-claim boundary | current |
| [SFT validation report](debian-admin-bash-sft.validation-report.md) | Current Debian/Ubuntu admin Bash SFT dataset validation | pass |
| [Quality audit](debian-admin-bash-sft.quality-audit.md) | Distribution, repetition watchlist, review priorities, and next-addition recommendations | advisory |
| [Single-turn eval validation report](debian-admin-bash-eval.validation-report.md) | Held-out single-turn eval validation | pass |
| [Multi-turn eval validation report](debian-admin-bash-multiturn-eval.validation-report.md) | Held-out multi-turn continuation eval validation | pass |
| [Eval heuristic score](debian-admin-bash-eval.heuristic-score.md) | Heuristic safe-first eval runner self-check on reference answers | pass |
| [Review-candidate validation report](debian-admin-bash-review-candidates.validation-report.md) | 360-record review-candidate subset validation | pass |
| [Review-candidate sandbox report](debian-admin-bash-review-candidates.sandbox-checks.md) | Conservative sandbox/static triage of review-candidate command blocks | advisory |
| `datasets/debian-admin-bash/review/review-manifest.json` | Hash-bound record review-state summary | current |
| `datasets/debian-admin-bash/review/family-review-manifest.json` | Hash-bound family consistency-review summary | current |
| [Preference validation report](debian-admin-bash-preference.validation-report.md) | 200-record bad-vs-good preference set validation | pass |
| [LiteCoder-Terminal-SFT export validation report](debian-admin-bash-litecoder-terminal-sft.validation-report.md) | Generated ShareGPT-style `human`/`gpt` JSON export validation | pass |
| [v0.2 sample validation report](debian-admin-bash-sft.v0.2.sample.validation-report.md) | Governed sample schema and governance validation | pass |

Historical validation context for removed full snapshots lives in `datasets/debian-admin-bash/CHANGELOG.md` and git history.

## Migration rule

Do not treat a structural pass as production readiness.

Before using records for training, run governance validation and then review the records semantically and for safety. High-risk or ambiguous records should be reviewed, quarantined, or rejected.

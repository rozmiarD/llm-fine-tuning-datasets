# Validation

This directory contains validation scripts, validation notes, and validation reports.

## Validation provenance

The current validation/model provenance is recorded in [Validation provenance](VALIDATION_PROVENANCE.md).

Short version for the current local quality wave: deterministic scripts produced the validation/sandbox counts; model-assisted curation and audit were performed in OpenClaw with `openai-codex/gpt-5.5`, think mode `medium`, text verbosity `low`. This is not a claim of full independent semantic/human review.

## Validation layers

Validation is layered.

```text
JSON parse
  -> JSON Schema
  -> governance lint
  -> semantic and safety review
```

The validator can catch many common dataset defects, but it does not prove that a record is correct or safe.

## Current schemas

| Schema | Scope |
|---|---|
| `schemas/debian-admin-bash.v0.1.schema.json` | Legacy v0.1 source records retained for historical/audit validation only. |
| `schemas/debian-admin-bash.v0.2.schema.json` | Governed record-shape schema for Debian/Ubuntu admin Bash records with risk, safety, answer-style, and review metadata. |

The governed v1.1 Debian-admin Bash dataset uses `meta.dataset_version="1.1"`, but it still validates against `schemas/debian-admin-bash.v0.2.schema.json` because the governed record shape did not change.

## Validator

Executable validator:

```text
validation/validate_dataset.py
```

Install dependencies:

```bash
python -m pip install -r requirements-dev.txt
```

Validate the governed v0.2 sample:

```bash
python validation/validate_dataset.py \
  datasets/debian-admin-bash/samples/debian-admin-bash-sft.v0.2.sample.jsonl \
  --schema schemas/debian-admin-bash.v0.2.schema.json \
  --report validation/debian-admin-bash-sft.v0.2.sample.validation-report.md
```

Validate the governed v1.1 Debian-admin Bash dataset:

```bash
python validation/validate_dataset.py \
  datasets/debian-admin-bash/debian-admin-bash-sft.v1.1.jsonl \
  --schema schemas/debian-admin-bash.v0.2.schema.json \
  --report validation/debian-admin-bash-sft.v1.1.validation-report.md
```

Validate the held-out eval files:

```bash
python validation/validate_dataset.py \
  datasets/debian-admin-bash/evals/debian-admin-bash-eval.v0.1.jsonl \
  --schema schemas/debian-admin-bash.v0.2.schema.json \
  --report validation/debian-admin-bash-eval.v0.1.validation-report.md

python validation/validate_dataset.py \
  datasets/debian-admin-bash/evals/debian-admin-bash-multiturn-eval.v0.1.jsonl \
  --schema schemas/debian-admin-bash.v0.2.schema.json \
  --report validation/debian-admin-bash-multiturn-eval.v0.1.validation-report.md
```

Run the held-out eval heuristic self-check:

```bash
python scripts/run_eval.py \
  --report validation/debian-admin-bash-eval.v0.1.heuristic-score.md
```

Run sandbox checks for mechanically checkable review-candidate records:

```bash
python scripts/run_sandbox_checks.py \
  --backend bwrap \
  --jsonl validation/debian-admin-bash-sft.v1.1.sandbox-checks.jsonl \
  --report validation/debian-admin-bash-sft.v1.1.sandbox-checks.md
```

The sandbox checker is conservative. It runs syntax checks for extracted Bash blocks, executes only allowlisted fixture-safe commands, and classifies host-admin commands as `static_only` or `blocked` with a suggested next review action.

Validate the review-candidate subset:

```bash
python validation/validate_dataset.py \
  datasets/debian-admin-bash/review/debian-admin-bash-sft.v1.1.review-candidates.jsonl \
  --schema schemas/debian-admin-bash.v0.2.schema.json \
  --report validation/debian-admin-bash-sft.v1.1.review-candidates.validation-report.md
```

Validate the preference set:

```bash
python validation/validate_preference_dataset.py \
  datasets/debian-admin-bash/preferences/debian-admin-bash-preference.v0.1.jsonl \
  --report validation/debian-admin-bash-preference.v0.1.validation-report.md
```

## What the validator checks

The validator checks:

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
- review-status honesty.

## Validator implementation notes

The validator stores an internal `__line_no` helper while reading JSONL, but that helper is removed before JSON Schema validation. It should not make otherwise valid records fail schema validation.

Privilege escalation words such as `sudo`, `doas`, and `su -` are checked against `meta.requires_root`. They do not automatically force `privilege_sensitive` risk, because normal package, service, and inspection workflows may legitimately require root while belonging to a lower or different risk class.

Read-only firewall inspection such as `ufw status` or `iptables -S` is not treated as a firewall state change. Firewall-changing operations such as `ufw allow`, `ufw enable`, `iptables -A`, `iptables -F`, or `nft add` remain `network_sensitive`.

## What the validator does not prove

The validator does not prove that:

- the command is the best command;
- the command has been executed successfully;
- the answer is semantically correct;
- the dataset is production-grade;
- a trained model will behave safely without runtime controls.

## Reports

| Report | Scope | Status |
|---|---|---|
| [Bootstrap validation report](bootstrap-validation-report.md) | Initial repository structure and sample consistency | pass |
| [v0.1 validation report](debian-admin-bash-sft.v0.1.historical.validation-report.md) | Historical validation report for the removed faulty legacy corpus | historical only |
| [v0.2 sample validation report](debian-admin-bash-sft.v0.2.sample.validation-report.md) | Governed sample schema and governance validation | pass |
| [Validation provenance](VALIDATION_PROVENANCE.md) | Validator/tool/model provenance and review-claim boundary | current |
| [debian-admin-bash v1.1 governed SFT validation report](debian-admin-bash-sft.v1.1.validation-report.md) | Debian/Ubuntu admin Bash SFT dataset validation | pass |
| [debian-admin-bash v1.1 quality audit](debian-admin-bash-sft.v1.1.quality-audit.md) | Distribution, repetition watchlist, review priorities, and next-addition recommendations | advisory |
| [debian-admin-bash single-turn eval validation report](debian-admin-bash-eval.v0.1.validation-report.md) | Held-out single-turn eval validation | pass |
| [debian-admin-bash multi-turn eval validation report](debian-admin-bash-multiturn-eval.v0.1.validation-report.md) | Held-out multi-turn continuation eval validation | pass |
| [debian-admin-bash eval heuristic score](debian-admin-bash-eval.v0.1.heuristic-score.md) | Heuristic safe-first eval runner self-check on reference answers | pass |
| [debian-admin-bash sandbox check report](debian-admin-bash-sft.v1.1.sandbox-checks.md) | Conservative sandbox/static triage of review-candidate command blocks | advisory |
| [debian-admin-bash review-candidate validation report](debian-admin-bash-sft.v1.1.review-candidates.validation-report.md) | 360-record review-candidate subset validation | pass |
| [debian-admin-bash preference validation report](debian-admin-bash-preference.v0.1.validation-report.md) | 60-record bad-vs-good preference set validation | pass |

## Migration rule

Do not treat a structural pass as production readiness.

Before using records for training, run governance validation and then review the records semantically and for safety. High-risk or ambiguous records should be reviewed, quarantined, or rejected.

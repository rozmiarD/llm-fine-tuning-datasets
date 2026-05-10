# Validation

This directory contains validation scripts, validation notes, and validation reports.

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
| `schemas/terminal-admin-bash-master.v0.1.schema.json` | Legacy v0.1 source records. |
| `schemas/terminal-admin-bash-master.v0.2.schema.json` | Governed v0.2 source records with risk, safety, answer-style, and review metadata. |

No v0.3 schema is required for the cleaned Bash-heavy migration. The source material came from a `v0.3.cleaned-bash-heavy` dataset, but the repository record shape is still the governed v0.2 source-record schema.

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
  datasets/terminal-admin-bash-master/samples/terminal-admin-bash-master__4b-coder-instruct__sft__en__debian-ubuntu__v0.2.sample.jsonl \
  --schema schemas/terminal-admin-bash-master.v0.2.schema.json \
  --report validation/terminal-admin-bash-master__4b-coder-instruct__sft__en__debian-ubuntu__v0.2.sample.validation-report.md
```

Validate the governed small-terminal-admin v0.2 conversion:

```bash
python validation/validate_dataset.py \
  datasets/terminal-admin-bash-master/terminal-admin-bash-master__small-terminal-admin__sft__en__debian-ubuntu__v0.2.jsonl \
  --schema schemas/terminal-admin-bash-master.v0.2.schema.json \
  --report validation/terminal-admin-bash-master__small-terminal-admin__sft__en__debian-ubuntu__v0.2.validation-report.md
```

Validate a legacy corpus without failing the migration run:

```bash
python validation/validate_dataset.py \
  datasets/terminal-admin-bash-master/terminal-admin-bash-master__4b-coder-instruct__sft__en__debian-ubuntu__v0.1.full-2000.jsonl \
  --schema schemas/terminal-admin-bash-master.v0.1.schema.json \
  --warn-only
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
| [v0.1 validation report](terminal-admin-bash-master__4b-coder-instruct__sft__en__debian-ubuntu__v0.1.validation-report.md) | Legacy full corpus structural validation | legacy structural pass |
| [v0.2 sample validation report](terminal-admin-bash-master__4b-coder-instruct__sft__en__debian-ubuntu__v0.2.sample.validation-report.md) | Governed sample schema and governance validation | pass |
| [small-terminal-admin v0.2 validation report](terminal-admin-bash-master__small-terminal-admin__sft__en__debian-ubuntu__v0.2.validation-report.md) | Governed conversion from the cleaned Bash-heavy source dataset | pass |

## Migration rule

Do not treat a legacy v0.1 pass as production readiness.

Before using records for training, migrate them to v0.2 metadata and run governance validation. High-risk or ambiguous records should be reviewed, quarantined, or rejected.

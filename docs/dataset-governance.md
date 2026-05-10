# Dataset governance

This repository stores source datasets, not automatically trusted training data.

A dataset record can be structurally valid and still be a bad training example. Governance exists to make that difference visible before records are exported into a model-specific training format.

## Governance layers

Use four layers of review.

```text
source JSONL
  -> JSON / schema validation
  -> dataset-governance linting
  -> semantic and safety review
  -> model-specific export
```

## Layer 1: structural validation

Structural validation checks that each line is valid JSON and that required fields exist.

It answers questions such as:

- Is every line parseable JSON?
- Does every record have an ID?
- Does the record contain metadata and messages?
- Are enum values known?
- Are message roles valid?

It does not prove that the answer is correct.

## Layer 2: governance linting

Governance linting checks common dataset-quality and Bash-safety problems.

It catches examples such as:

- Debian/Ubuntu datasets containing `yum`, `dnf`, `pacman`, `apk`, `zypper`, or `rpm` package-management patterns;
- `sudo` usage with `requires_root=false`;
- destructive commands marked as low risk;
- service, package, firewall, account, disk, or permission changes without an appropriate risk label;
- high-risk examples without warning metadata;
- exact duplicate task pairs;
- inconsistent `answer_style` declarations.

The linter is conservative. It is a review aid, not a proof of correctness.

## Layer 3: semantic and safety review

Human or expert review should check:

- whether the command actually solves the user task;
- whether the output is idiomatic for Debian/Ubuntu;
- whether safer alternatives should be preferred;
- whether warnings, dry-runs, backups, or rollbacks are required;
- whether the answer style matches the intended model behavior;
- whether the example teaches a habit that should be copied by a small local model.

A record should not be marked as `reviewed` unless both semantic and safety review have happened.

## Layer 4: export

The canonical records are source records. They are not guaranteed to match a target trainer or chat template directly.

Exporters should convert source records into the target training format, for example:

- ChatML;
- Alpaca-style prompt/completion;
- TRL chat template records;
- Hugging Face AutoTrain generic text records;
- Axolotl instruction/chat records.

Do not edit the source dataset just to satisfy one trainer. Add an exporter instead.

## Required risk levels

Use these risk levels consistently.

| Risk level | Meaning |
|---|---|
| `safe_readonly` | Inspection only. No intended host state change. |
| `state_change_low` | Low-risk state change such as installing a package or starting a service. |
| `state_change_high` | Potentially disruptive state change such as restarting services or rebooting. |
| `network_sensitive` | Firewall, routing, listening service, or network exposure change. |
| `privilege_sensitive` | Users, groups, credentials, sudo, or privilege boundaries. |
| `security_sensitive` | Security posture can be weakened or code is executed from a less trusted source. |
| `destructive` | Data, accounts, disks, or system state may be destroyed. |

When in doubt, use the higher risk level.

## Required answer styles

Use these answer styles to keep training behavior predictable.

| Answer style | Use when |
|---|---|
| `single_command` | The safest useful answer is one short command. |
| `command_with_brief_explanation` | A command needs one or two sentences of context. |
| `diagnostic_steps` | The answer is a sequence of inspection or troubleshooting steps. |
| `script_with_explanation` | The answer includes a Bash script or script fragment. |
| `guarded_procedure` | The task changes state and should include checks, warnings, or rollback notes. |
| `refusal_with_safe_alternative` | The requested action is unsafe as stated, but a safe route can be given. |

## Validation command

Install development dependencies:

```bash
python -m pip install -r requirements-dev.txt
```

Validate a governed v0.2 dataset:

```bash
python validation/validate_dataset.py \
  datasets/terminal-admin-bash-master/samples/terminal-admin-bash-master__4b-coder-instruct__sft__en__debian-ubuntu__v0.2.sample.jsonl \
  --schema schemas/terminal-admin-bash-master.v0.2.schema.json \
  --report validation/terminal-admin-bash-master__4b-coder-instruct__sft__en__debian-ubuntu__v0.2.sample.validation-report.md
```

During migration of legacy corpora, use `--warn-only` to generate reports without failing the command.

```bash
python validation/validate_dataset.py legacy.jsonl --warn-only
```

## Non-claims

Validation does not claim that:

- the dataset is production-grade;
- every command has been executed successfully;
- every answer is semantically correct;
- the dataset is ready for unattended terminal-agent training;
- a fine-tuned model will behave safely without runtime controls.

For terminal or security-adjacent models, runtime policy gates are still required.

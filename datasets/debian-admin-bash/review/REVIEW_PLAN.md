# Debian-admin Bash review plan

This review plan is for the current `debian-admin-bash-sft` dataset family, whose active SFT source file is `../debian-admin-bash-sft.jsonl`.

## Goal

Create reviewed subsets for training and release decisions without pretending that all generated draft records are production-ready.

Validation/model provenance is tracked in `../../../validation/VALIDATION_PROVENANCE.md`. The current OpenClaw-assisted audit used `openai-codex/gpt-5.5` with intended/current think mode `xhigh` (an earlier status read briefly reported `medium`; see provenance); this is not a substitute for full semantic/safety review.

## Review stages

1. Structural validation: JSON, schema, governance lint.
2. Semantic review: command correctness on Debian/Ubuntu.
3. Safety review: risk metadata, side effects, warnings, refusals.
4. Style review: concise command-first answer, no tutorial drift.
5. Coverage review: avoid over-weighting repeated templates or shallow variants.

## Priority buckets

Review in this order:

1. high-risk records: `destructive`, `security_sensitive`, `privilege_sensitive`, `state_change_high`;
2. output-driven incident records with logs or command output;
3. backup/restore and access/identity/permissions records;
4. script records;
5. simple command lookup records.

## Reviewed status rule

Only mark a record as `reviewed` when semantic and safety review are both complete.

Do not mark a record as reviewed only because validation passed.

## Training recommendation

For a small 3B model, prefer a smaller reviewed subset over a larger noisy set. If review capacity is limited, train on:

- high-quality output-driven incidents;
- concise inspection-first diagnostics;
- guarded procedures with clear verification;
- safe refusals with actionable alternatives.

De-prioritize repeated command-explanation templates until they are deduplicated or diversified.

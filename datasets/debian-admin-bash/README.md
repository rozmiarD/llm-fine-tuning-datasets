# debian-admin-bash

Debian/Ubuntu terminal-administration source data for supervised fine-tuning, evaluation, review, and preference experiments.

## Current public files

| Purpose | File | Records | Status |
|---|---|---:|---|
| SFT source dataset | `debian-admin-bash-sft.jsonl` | 2836 | governed draft |
| Review-candidate subset | `review/review-candidates.jsonl` | 360 | draft candidates for manual semantic/safety review |
| Single-turn eval | `evals/single-turn.jsonl` | 80 | held-out draft eval, not training data |
| Multi-turn eval | `evals/multiturn.jsonl` | 40 | held-out draft continuation eval, not training data |
| Preference examples | `preferences/preference.jsonl` | 200 | draft bad-vs-good examples, not SFT data |
| Record review manifest | `review/review-manifest.json` | current summary | hash-bound reviewed/stale index |
| Family review manifest | `review/family-review-manifest.json` | current summary | hash-bound family consistency index |
| Governed sample | `samples/debian-admin-bash-sft.v0.2.sample.jsonl` | sample | record-shape reference |

Historical full JSONL snapshots are not kept as active files on `main`. Use [CHANGELOG.md](CHANGELOG.md) plus git history for previous checkpoint summaries.

The review-candidate subset is intentionally not refreshed in this v1.2 content wave; it remains a draft candidate artifact, not a review claim.

## Current SFT metadata

- Dataset family: `debian-admin-bash-sft`
- Current public SFT file: `debian-admin-bash-sft.jsonl`
- Content checkpoint: `v1.2`
- Records: `2836`
- SHA-256: `e021ee617322960579776f38cd71443ff5027df29b369c9e257ea0025e93aa2a`
- Schema: `../../schemas/debian-admin-bash.v0.2.schema.json`
- Review status: `draft`

`meta.dataset_version` is `1.2` inside the current SFT records. The stable filename avoids accumulating public full-dataset snapshots for every checkpoint.

## Human-readable docs

- [Dataset card](DATASET_CARD.md) — current dataset facts, intended use, limitations, and review status.
- [Changelog](CHANGELOG.md) — checkpoint history and old migration-note content in one place.
- [Review plan](review/REVIEW_PLAN.md) — how to turn draft records into reviewed subsets without re-reviewing unchanged records.
- `review/review-manifest.json` — current record review-state summary. Draft entries are summarized, not expanded, to avoid a large manifest.
- `review/family-review-manifest.json` — family consistency-review markers, empty until a family is explicitly checked.
- [Eval README](evals/README.md) — held-out eval purpose and file names.
- [Preference README](preferences/README.md) — preference-set purpose and file names.

## Validation and audit reports

- `../../validation/VALIDATION_PROVENANCE.md`
- `../../validation/debian-admin-bash-sft.validation-report.md`
- `../../validation/debian-admin-bash-sft.quality-audit.md`
- `../../validation/debian-admin-bash-eval.validation-report.md`
- `../../validation/debian-admin-bash-multiturn-eval.validation-report.md`
- `../../validation/debian-admin-bash-eval.heuristic-score.md`
- `../../validation/debian-admin-bash-review-candidates.validation-report.md`
- `../../validation/debian-admin-bash-review-candidates.sandbox-checks.md`
- `../../validation/debian-admin-bash-preference.validation-report.md`

## Scope and non-claims

This is a governed draft dataset, not a production-ready command policy.

Passing JSON Schema validation and governance linting means the files are structurally consistent. It does **not** mean every command is semantically correct, safe to execute, or manually reviewed.

PostgreSQL is intentionally excluded from the active corpus; database coverage is SQLite-oriented and local-file-backed.

VirtualBox appears only as bounded local host VM administration coverage. It is not a pivot into cloud, Kubernetes, Terraform, or broad enterprise virtualization.

## Validate

From the repository root:

```bash
python validation/validate_dataset.py \
  datasets/debian-admin-bash/debian-admin-bash-sft.jsonl \
  --schema schemas/debian-admin-bash.v0.2.schema.json \
  --report validation/debian-admin-bash-sft.validation-report.md

python validation/validate_dataset.py \
  datasets/debian-admin-bash/review/review-candidates.jsonl \
  --schema schemas/debian-admin-bash.v0.2.schema.json \
  --report validation/debian-admin-bash-review-candidates.validation-report.md

python validation/validate_preference_dataset.py \
  datasets/debian-admin-bash/preferences/preference.jsonl \
  --report validation/debian-admin-bash-preference.validation-report.md
```

Run eval, sandbox, and review-state checks:

```bash
python scripts/run_eval.py
python scripts/run_sandbox_checks.py
python scripts/review_state.py status
```

If a reviewed record is edited later, `scripts/review_state.py status` reports it as stale until it is reviewed and stamped again.

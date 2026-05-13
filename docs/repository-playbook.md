# Repository playbook

This playbook applies only to this repository: `llm-fine-tuning-datasets`.

It does not define workflow rules for Ravenclaw, GovEngine, SCLite, or any other repository.

## Publishing rule

The remote `main` branch should represent official dataset releases, not day-to-day draft iteration.

Do not push every working dataset content version to the remote repository.

Use local commits, local branches, or private working files for draft waves. Push only when the dataset version is ready to be treated as an official public checkpoint for this repository.

## Official release checkpoint

A dataset version is ready to push only when all of the following are true:

- the active JSONL file is the intended official version;
- generated or intermediate draft files are removed or intentionally excluded;
- record count, SHA-256, dataset card, README files, and validation report agree;
- JSONL parsing, schema validation, and governance linting pass;
- semantic/safety review status is stated honestly (`draft`, `reviewed`, `quarantined`, or `rejected`);
- no documentation claims production readiness from structural validation alone;
- the commit contains one coherent public checkpoint, not a stream of scratch versions.

## Draft work

Draft versions may exist locally while building a release candidate.

Recommended local flow:

```text
local draft edits
  -> local validation
  -> local audit/cleanup
  -> select final active version
  -> update changelog/migration notes
  -> remove or ignore intermediate scratch files
  -> commit official checkpoint
  -> push official checkpoint
```

If multiple experimental content versions were explored locally, do not publish each as a separate active dataset file. Preserve the useful history in the dataset changelog or migration notes instead.

## Version files

Prefer one active full dataset file per public checkpoint.

Do not accumulate public full JSONL files for every draft content wave unless there is a strong audit reason. Historical context should usually live in:

- dataset changelog or migration notes;
- validation report for the official checkpoint;
- dataset card summary;
- git history.

Reference samples and intentionally retained historical/audit files are allowed when clearly labelled.

## Changelog and migration notes

Use changelog or migration notes to summarize what changed between official checkpoints.

A good migration note records:

- input version and record count;
- output version and record count;
- SHA-256 of the official output file;
- added/removed surfaces;
- validation report path;
- scope-control notes;
- non-claims and review status.

Do not create noisy per-version README files for every draft wave. Keep README files focused on the current official state and stable repository guidance.

## README and dataset card policy

README files and dataset cards should describe the current official active dataset and point to canonical docs.

They should not become a full historical ledger. Historical details belong in migration notes, changelog entries, validation reports, and git commits.

## Push discipline

Before pushing:

```bash
git status --short --branch
git diff --check
python validation/validate_dataset.py \
  datasets/debian-admin-bash/<official-dataset>.jsonl \
  --schema schemas/debian-admin-bash.v0.2.schema.json \
  --report validation/<official-dataset>.validation-report.md
```

Also verify the effective Git identity before commit/push:

```bash
git config --get user.name
git config --get user.email
```

Expected identity for this workspace:

```text
0x505badc0de <32790662+rozmiarD@users.noreply.github.com>
```

## Practical rule of thumb

If a version is still being debated, expanded, or rapidly replaced, keep it local.

If it is the version users should see, validate it, document it as the official active checkpoint, then push it.

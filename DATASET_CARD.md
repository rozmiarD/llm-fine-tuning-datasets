# Dataset Cards

This file is an index of dataset cards in this repository.

Dataset-specific cards should live next to their dataset documentation. The root file should stay general and should not duplicate detailed per-dataset documentation.

## Available dataset cards

| Dataset | Card | Purpose | Records | Status |
|---|---|---|---:|---|
| `debian-admin-bash-sft.v1.1` | [Dataset card](datasets/debian-admin-bash/DATASET_CARD.md) | Debian/Ubuntu admin Bash SFT source records with Bash tooling, incident triage, structured parser, SQLite, backup/restore, SSH/auth, and defensive-admin coverage | 2672 | governed draft dataset |
| `debian-admin-bash-sft.v0.2` | [Dataset card](datasets/debian-admin-bash/DATASET_CARD.md) | Governed source-record reference sample | sample only | governed reference sample |

## Removed source material

The previous full v0.1 corpus was removed from the active dataset tree because it contained faulty data and should not be used as a valid training source.

## Card expectations

Each dataset card should describe:

- dataset name or dataset family;
- status and maturity level;
- intended use;
- language;
- platform;
- target model profile;
- source format;
- model-specific export notes;
- recommended answer style;
- quality priorities;
- validation and governance status;
- known limitations.

A dataset card should not imply production readiness when only structural validation has been performed.

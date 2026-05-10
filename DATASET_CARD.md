# Dataset Cards

This file is an index of dataset cards in this repository.

Dataset-specific cards should live next to their dataset documentation. The root file should stay general and should not duplicate detailed per-dataset documentation.

## Available dataset cards

| Dataset | Card | Purpose | Records | Status |
|---|---|---|---:|---|
| `terminal-admin-bash-master__4b-coder-instruct__sft__en__debian-ubuntu__v0.1` | [Dataset card](datasets/terminal-admin-bash-master/DATASET_CARD.md) | Debian/Ubuntu terminal administration for 4B coder-instruct models | 2000 | legacy experimental corpus |
| `terminal-admin-bash-master__4b-coder-instruct__sft__en__debian-ubuntu__v0.2` | [Dataset card](datasets/terminal-admin-bash-master/DATASET_CARD.md) | Governed source-record format with risk, safety, answer-style, and review metadata | sample only | governed reference sample |
| `terminal-admin-bash-master__small-terminal-admin__sft__en__debian-ubuntu__v0.2` | [Dataset card](datasets/terminal-admin-bash-master/DATASET_CARD.md) | Governed draft conversion from cleaned Bash-heavy terminal-admin source material | 908 | governed draft conversion |

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

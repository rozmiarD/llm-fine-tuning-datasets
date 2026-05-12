# Datasets

This directory contains role-specific dataset families.

Each dataset directory should contain its own README with:

- dataset identity;
- target model profile;
- intended training use;
- language;
- platform;
- source format;
- quality rules;
- sample records or links to sample records.

## Current dataset families

| Directory | Dataset family | Purpose | Status |
|---|---|---|---|
| [`terminal-admin-bash-master`](terminal-admin-bash-master/README.md) | Terminal administration for small terminal-admin and coder-instruct model profiles | Debian/Ubuntu Bash command generation, short explanations, inspection-first troubleshooting, and governed safety metadata | governed draft dataset plus reference samples |

## Directory naming

Dataset directories should use the role name only.

Good:

```text
terminal-admin-bash-master
```

Avoid including full dataset file names in directory names. Full names belong to `.jsonl` dataset files.

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
| [`debian-admin-bash`](debian-admin-bash/README.md) | Debian/Ubuntu administration for small Debian-admin and coder-instruct model profiles | Debian/Ubuntu Bash command generation, short explanations, inspection-first troubleshooting, governed safety metadata, and a generated LiteCoder-Terminal-SFT-style export | governed draft dataset plus generated export, companion artifacts, and reference samples |

## Directory naming

Dataset directories should use the role name only.

Good:

```text
debian-admin-bash
```

Avoid including full dataset file names in directory names. Full names belong to `.jsonl` dataset files.

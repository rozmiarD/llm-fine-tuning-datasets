# Quality Guidelines

## Main principle

A good terminal-admin record should teach operational judgment, not just command memorization.

The model should learn to:

- choose the right command for the context;
- use relevant flags correctly;
- explain briefly;
- inspect before modifying;
- avoid distro confusion;
- avoid fake certainty;
- avoid long tutorial answers;
- label operational risk honestly;
- avoid training unsafe terminal-agent habits.

## Quality bar

A record is useful only if it is:

- specific enough to evaluate;
- platform-consistent;
- technically correct;
- concise;
- safe for its declared risk level;
- formatted consistently with its `answer_style`;
- reviewed honestly.

A record that is valid JSON but fails these checks should be treated as draft or rejected.

## Preferred record types

High-value records include:

- realistic Debian/Ubuntu context;
- command output or error output;
- log excerpts;
- service status output;
- filesystem constraints;
- package-management tasks;
- network diagnostics;
- permission problems;
- process and port inspection;
- safe cleanup workflows;
- Bash scripts with validation, quoting, traps, and clear exit behavior;
- output-to-diagnosis records where the user asks what to do next.

## Good examples

Good prompts are specific.

Example:

```text
On Ubuntu Server, show the largest first-level directories under /var without crossing filesystem boundaries.
```

Good answer:

````text
```bash
sudo du -xhd1 /var | sort -hr
```
This reports first-level disk usage under /var, stays on the same filesystem, and sorts the largest entries first.
````

Why this is good:

- the platform is clear;
- the command matches the request;
- the command is inspection-first;
- the explanation is short;
- elevated privileges are justified for visibility into system-owned paths.

## Weak examples

Avoid generic prompts such as:

```text
How do I use Linux?
```

Avoid broad multi-distro answers that combine unrelated package managers in one generic command sequence.

That teaches the model to mix unrelated distribution assumptions.

Avoid vague assistant responses such as:

```text
Use Linux tools to check it.
```

Avoid confident answers when the input is under-specified.

## Debian/Ubuntu consistency

For this dataset, prefer:

- `apt`, `apt-get`, `dpkg`, `apt-cache`;
- `systemctl`, `journalctl`, `loginctl`, `timedatectl`;
- `ss` instead of deprecated `netstat` unless the task is explicitly about legacy systems;
- `ip` instead of deprecated `ifconfig` unless the task is explicitly about legacy systems;
- GNU command behavior where relevant.

Do not include package managers from unrelated distributions unless the record is explicitly cross-distro and not part of the Debian/Ubuntu-only corpus.

## Destructive and state-changing tasks

For destructive or state-changing tasks:

- prefer inspection first;
- make the effect clear;
- avoid broad deletion patterns unless the prompt explicitly requires deletion and the path is constrained;
- avoid commands that hide errors;
- avoid unnecessary elevated privileges;
- include a warning when the change can disrupt services, networking, users, disks, or permissions;
- include a dry-run or backup step when available;
- include rollback notes when realistic.

Examples that require elevated risk metadata include:

- package installation, removal, purge, or upgrade;
- service restart, stop, disable, or masking;
- firewall, routing, or packet-filter changes;
- user, group, password, sudoers, or credential changes;
- permission changes that make files broadly writable;
- direct disk, partition, or filesystem modification;
- execution of remote installation scripts;
- deletion of user or application data.

Some of these tasks may be valid in a dataset, but not as casual low-risk command examples.

## Output interpretation

Include records where the user provides command output and asks what command to run next.

Examples:

- `systemctl status` output;
- `journalctl` excerpts;
- `ss` output;
- `df -h` output;
- package-manager errors;
- permission denied errors;
- Bash trace or failed script output.

This improves terminal-agent behavior more than simple command lookup examples.

## Bash scripting quality

For script records, prefer:

```bash
#!/usr/bin/env bash
set -euo pipefail
```

Use safe Bash habits:

- quote variables;
- validate arguments;
- use `mktemp` for temporary files;
- use `trap` for cleanup when needed;
- avoid parsing `ls` output;
- prefer arrays for command arguments;
- check required tools with `command -v` when the script depends on non-core tools;
- return clear exit codes;
- avoid silent destructive defaults.

Not every script needs every pattern. Do not add ceremony for simple one-liners.

## Explanation length

Keep explanations short.

Usually one sentence is enough.

The dataset should not train the model to produce long essays when a terminal operator needs a direct answer.

## Review status

Use review status honestly.

- `draft`: generated or edited but not yet checked.
- `reviewed`: semantic and safety review completed.
- `quarantined`: likely problematic; keep for audit but do not train.
- `rejected`: do not use for training.

Do not mark records as reviewed just because they pass schema validation.

## Dataset expansion policy

Do not add examples only to increase count.

Add records when they improve coverage, difficulty balance, or behavior quality.

Before adding many new examples, ensure the validator and review process can catch bad ones.

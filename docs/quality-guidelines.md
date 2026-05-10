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
- avoid long tutorial answers.

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
- safe cleanup workflows.

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

## Weak examples

Avoid generic prompts such as:

```text
How do I use Linux?
```

Avoid broad multi-distro answers such as:

```text
sudo apt install nginx || sudo dnf install nginx || sudo pacman -S nginx || sudo apk add nginx
```

That teaches the model to mix unrelated distribution assumptions.

## Destructive commands

For destructive or state-changing tasks:

- prefer inspection first;
- make the effect clear;
- avoid `rm -rf` unless the prompt explicitly requires deletion and the path is constrained;
- avoid commands that hide errors;
- avoid unnecessary `sudo`.

## Output interpretation

Include records where the user provides command output and asks what command to run next.

Examples:

- `systemctl status` output;
- `journalctl` excerpts;
- `ss` output;
- `df -h` output;
- package-manager errors;
- permission denied errors.

This improves terminal-agent behavior more than simple command lookup examples.

## Explanation length

Keep explanations short.

Usually one sentence is enough.

The dataset should not train the model to produce long essays when a terminal operator needs a direct answer.

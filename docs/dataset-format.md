# Dataset Format

## Canonical format

The canonical source format is JSONL.

Each line is one valid JSON object.

Each object contains:

- `id`;
- `meta`;
- `messages`.

The `messages` field contains the trainable conversation. The `meta` field is used for filtering, validation, export, safety review, and documentation.

## Why JSONL messages

The `messages` format is used because it is easy to export into common instruction/chat training formats.

It can be converted into:

- model-specific chat templates;
- ChatML-like formats;
- Alpaca-like prompt/completion formats;
- ShareGPT-like formats;
- trainer-specific formats used by common fine-tuning tools.

The repository stores source data. Training pipelines should handle final formatting.

## Governed record shape

New terminal-administration records should use the current governed shape defined by `schemas/debian-admin-bash.v0.2.schema.json`. Dataset content versions can move forward, for example `meta.dataset_version="0.6"`, while the record-shape schema remains v0.2.

```json
{
  "id": "debian-admin-bash:filesystem.du-largest-current.001",
  "meta": {
    "dataset_version": "0.2",
    "task_type": "sft",
    "language": "en",
    "domain": "debian_admin_bash",
    "subdomain": "filesystem",
    "target_os": {
      "family": "linux",
      "distros": ["debian", "ubuntu"],
      "shell": "bash",
      "package_manager": "none"
    },
    "difficulty": "beginner",
    "risk_level": "safe_readonly",
    "requires_root": false,
    "answer_style": "command_with_brief_explanation",
    "tags": ["du", "sort", "disk-usage"],
    "safety": {
      "has_side_effects": false,
      "side_effects": [],
      "destructive": false,
      "warning_required": false,
      "warning_present": false,
      "dry_run_available": false,
      "rollback_available": false
    },
    "review": {
      "status": "reviewed",
      "semantic_review": true,
      "safety_review": true,
      "execution_validation": {
        "mode": "static_only",
        "status": "passed"
      }
    }
  },
  "messages": [
    {
      "role": "system",
      "content": "You are a Debian/Ubuntu terminal administration assistant. Return correct Bash commands and brief factual explanations. Prefer inspection before modification."
    },
    {
      "role": "user",
      "content": "Show the 10 largest files and directories in the current directory."
    },
    {
      "role": "assistant",
      "content": "```bash\ndu -ah . | sort -rh | head -n 10\n```\nThis scans the current directory, sorts entries by size in descending order, and prints the 10 largest results."
    }
  ]
}
```

## Legacy v0.1 record

The original v0.1 corpus used a lighter metadata shape.

Legacy records can remain in the repository for reproducibility, but new records should use v0.2 governance metadata.

## Field notes

### id

Stable unique identifier.

Recommended v0.2 pattern:

```text
debian-admin-bash:<subdomain>.<short-task-name>.<number>
```

Examples:

```text
debian-admin-bash:filesystem.du-largest-current.001
debian-admin-bash:systemd.nginx-status-logs.001
debian-admin-bash:scripting.audit-world-writable.001
```

### meta.dataset_version

Use the dataset content version for the source file, for example `0.2` for the governed reference sample or `0.6` for the active Debian-admin Bash dataset. Do not confuse this with the JSON Schema version.

### meta.target_os

Declare the operating-system assumptions explicitly.

For this dataset, use Debian/Ubuntu assumptions by default:

- `apt` / `apt-get` / `dpkg` package management;
- `systemd`, `systemctl`, and `journalctl`;
- GNU userland behavior;
- Bash unless the task is explicitly POSIX shell.

Do not mix unrelated package managers unless the task is explicitly about cross-distro comparison.

### meta.risk_level

Risk level describes the operational risk of the assistant answer.

Use the highest relevant risk level. When in doubt, choose the more conservative value.

Canonical risk levels are defined in [Dataset governance](dataset-governance.md).

### meta.answer_style

Answer style constrains the expected assistant behavior.

Use it to prevent the dataset from mixing terse command lookup, long tutorials, procedures, scripts, and refusals without control. Canonical answer styles are defined in [Dataset governance](dataset-governance.md).

### meta.safety

Safety metadata must match the answer content.

Examples:

- `sudo apt install nginx` has side effects and requires root;
- `sudo systemctl restart nginx` has side effects and can be disruptive;
- `rm -rf` patterns are destructive unless clearly constrained and guarded;
- firewall changes are network-sensitive;
- user and sudoers changes are privilege-sensitive.

### meta.review

A record should not be marked `reviewed` unless both semantic and safety review have happened.

If the command has not been executed, do not claim execution validation. Use `static_only`, `manual`, `not_executed`, or `skipped` honestly.

### messages

Allowed roles:

- `system`;
- `user`;
- `assistant`.

Preferred pattern for SFT records:

```text
system -> user -> assistant
```

The final message should be an assistant message.

## Target-specific export

Do not assume the canonical JSONL file can be fed directly to any model.

Before training, map `messages` into the required chat template for the target model and tokenizer.

Model-specific export should preserve:

- user intent;
- command formatting;
- assistant answer style;
- safety-relevant wording;
- short explanation style.

Do not edit source records just to satisfy one trainer. Add an exporter.

## Assistant answer format

Preferred for command answers:

````text
```bash
command here
```
Short explanation here.
````

For state-changing or high-risk operations, include enough context to prevent unsafe imitation.

For destructive or under-specified requests, prefer a guarded procedure or a refusal with a safer alternative.

# Dataset Format

## Canonical format

The canonical source format is JSONL.

Each line is one valid JSON object.

Each object contains:

- `id`;
- `meta`;
- `messages`.

## Why JSONL messages

The `messages` format is used because it is easy to export into common instruction/chat training formats.

It can be converted into:

- model-specific chat templates;
- ChatML-like formats;
- Alpaca-like prompt/completion formats;
- ShareGPT-like formats;
- trainer-specific formats used by common fine-tuning tools.

The repository stores source data. Training pipelines should handle final formatting.

## Minimal record

```json
{
  "id": "tabm-4b-ci-sft-en-du-000001",
  "meta": {
    "role": "terminal-admin-bash-master",
    "target_model_size": "4b",
    "target_model_type": "coder-instruct",
    "training_use": "sft",
    "language": "en",
    "platform": "debian-ubuntu",
    "task_type": "command_generation",
    "difficulty": "basic",
    "tags": ["linux", "bash", "disk-usage"]
  },
  "messages": [
    {
      "role": "system",
      "content": "You are a Linux terminal administration assistant. Return correct Bash commands and a brief factual explanation. Prefer safe, non-destructive commands unless the user explicitly asks for a change."
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

## Field notes

### id

Stable unique identifier.

Recommended prefix for this dataset:

```text
tabm-4b-ci-sft-en-du-
```

Where:

- `tabm` = terminal-admin-bash-master;
- `4b` = target model size;
- `ci` = coder-instruct;
- `sft` = supervised fine-tuning;
- `en` = English;
- `du` = Debian/Ubuntu.

### meta

Metadata is used for filtering, validation, exports, and dataset documentation.

Models should usually train on `messages`, not on serialized metadata.

### messages

The conversation to train on.

Allowed roles:

- `system`;
- `user`;
- `assistant`.

The last message should normally be an assistant message.

## Target-specific export

Do not assume the canonical JSONL file can be fed directly to any model.

Before training, map `messages` into the required chat template for the target model and tokenizer.

Model-specific export should preserve:

- user intent;
- command formatting;
- assistant answer style;
- safety-relevant wording;
- short explanation style.

## Assistant answer format

Preferred:

````text
```bash
command here
```
Short explanation here.
````

If the command changes system state, the answer should be clear about that.

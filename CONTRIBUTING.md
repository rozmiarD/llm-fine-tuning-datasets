# Contributing

## Contribution goals

Contributions should improve the quality, consistency, or coverage of the dataset.

Good contributions include:

- realistic Debian/Ubuntu administration tasks;
- examples with actual command output or error output;
- concise command-first answers;
- corrections to inaccurate commands;
- improved metadata consistency;
- validation improvements.

## Language

All dataset records should be written in English unless a future dataset explicitly declares another language in its file name and metadata.

## Style

Use direct, technical language.

Avoid:

- marketing claims;
- exaggerated AI language;
- long tutorial-style answers;
- vague prompts;
- dangerous commands without context;
- distro-mixed command sequences unless the task is explicitly cross-distro.

## Record requirements

Every record must include:

- stable `id`;
- `meta.role`;
- `meta.target_model_size`;
- `meta.target_model_type`;
- `meta.training_use`;
- `meta.language`;
- `meta.platform`;
- `meta.task_type`;
- `meta.difficulty`;
- `meta.tags`;
- `messages`.

The last message should normally be an assistant answer.

## Preferred assistant answer

````text
```bash
command here
```
Short factual explanation here.
````

For destructive or state-changing commands, prefer an inspection step first unless the user explicitly asks for the change.

## Review checklist

Before adding records, check:

- Is the command valid on Debian/Ubuntu?
- Is the explanation short and factual?
- Does the record avoid unnecessary alternatives?
- Is the platform correctly marked?
- Is the command destructive?
- If destructive, is that clear from the prompt and answer?
- Are tags useful for filtering?
- Does the example teach something specific?

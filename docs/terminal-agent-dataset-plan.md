# Terminal-Agent SFT Corpus Plan

This note defines the focused LiteCoder terminal-agent corpus added alongside the broader Debian-admin Bash dataset.

## Why a separate focused corpus

The older broad SFT file is useful as governed Debian/Ubuntu administration data, but its answer distribution can over-teach conversational assistant behavior. A terminal agent needs many examples where the assistant starts with the exact executable artifact: command, script, query, regex pipeline, nginx snippet, or diagnostic sequence.

The focused corpus therefore uses a stricter system prompt and code-first answers with only one short operational note.

## Size target

The first useful replacement/supplement target is **640 records**:

| Area | Records |
|---|---:|
| Bash scripting | 80 |
| Terminal operation | 80 |
| JSON parsing with jq | 80 |
| Regex pipelines | 80 |
| SQLite inspection | 80 |
| nginx config/log triage | 80 |
| Incident triage | 80 |
| Networking diagnostics | 80 |

This is large enough to shift style toward terminal execution while remaining small enough for manual semantic review. A later production-grade training mix should grow to roughly **1,200-1,600 focused records** after eval feedback, keeping the same balance unless failures show a weak area.

## Quality rules

- Assistant output starts with the terminal artifact, not a chat preface.
- Explanations are short operational notes, not tutorials.
- Most examples are read-only diagnostics; state-changing records are guarded and labeled.
- Inputs include realistic paths, ports, service names, JSON fields, SQLite tables, nginx logs, and terminal failure modes.
- Records keep one user turn and one assistant turn for clean SFT conversion.
- Exact user/assistant duplicate pairs are rejected during generation.
- Generated records are checked against the existing SFT source for duplicate task pairs.

## Files

Source JSONL:

```text
datasets/debian-admin-bash/debian-admin-bash-terminal-agent-sft.jsonl
```

LiteCoder-Terminal-SFT-style export:

```text
datasets/debian-admin-bash/debian-admin-bash-terminal-agent-litecoder-sft.json
```

Deterministic generator:

```text
scripts/build_terminal_agent_sft.py
```

Validation reports:

```text
validation/debian-admin-bash-terminal-agent-sft.validation-report.md
validation/debian-admin-bash-terminal-agent-litecoder-sft.validation-report.md
```

## Regenerate and validate

```bash
python scripts/build_terminal_agent_sft.py

python validation/validate_dataset.py \
  datasets/debian-admin-bash/debian-admin-bash-terminal-agent-sft.jsonl \
  --schema schemas/debian-admin-bash.v0.2.schema.json \
  --report validation/debian-admin-bash-terminal-agent-sft.validation-report.md

python scripts/convert_to_litecoder_terminal_sft.py \
  datasets/debian-admin-bash/debian-admin-bash-terminal-agent-sft.jsonl \
  datasets/debian-admin-bash/debian-admin-bash-terminal-agent-litecoder-sft.json

python validation/validate_litecoder_terminal_sft.py \
  datasets/debian-admin-bash/debian-admin-bash-terminal-agent-litecoder-sft.json \
  --report validation/debian-admin-bash-terminal-agent-litecoder-sft.validation-report.md
```

Use the LiteCoder export for trainers that expect ShareGPT-style `human`/`gpt` conversations.

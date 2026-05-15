# LiteCoder-Terminal-SFT export validation report

- Dataset: `datasets/debian-admin-bash/debian-admin-bash-litecoder-terminal-sft.json`
- Records: 2836
- Structural errors: 0
- Status: PASSED

## Checks

- Top-level value is a JSON array.
- Every record is an object with integer `id`.
- IDs are unique.
- `source_id`, when present, is non-empty text.
- `conversations` is a non-empty even-length list.
- Conversation turns alternate `human` then `gpt` and end with `gpt`.
- Turn `value` fields are non-empty text.

## Errors

None.

# Migration notes: debian-admin-bash-sft v0.7 to v0.8

Generated: 2026-05-13

## Scope

This migration adds a small nmap host-exposure supplement for a narrow 3B Debian/Ubuntu administration model. The supplement treats nmap as a defensive host-admin verification tool, not as a pentest or offensive-security domain.

## Input

- Input dataset: `datasets/debian-admin-bash/debian-admin-bash-sft.v0.7.jsonl`
- Input records: 2270
- Input status: governed draft dataset

## Output

- Output dataset: `datasets/debian-admin-bash/debian-admin-bash-sft.v0.8.jsonl`
- Output records: 2360
- Added records: 90
- SHA-256: `07b9c534f078c97988663c256fa8ce93abdc8aa54190379ee20dfc29c18e4115`
- Governed record-shape schema: `schemas/debian-admin-bash.v0.2.schema.json`
- Validation report: `validation/debian-admin-bash-sft.v0.8.validation-report.md`

## Added surface

| Surface | Added records | Purpose |
|---|---:|---|
| Bounded nmap host-exposure verification | 90 | Verify expected ports on owned or explicitly approved hosts, compare local `ss`/firewall state to network-path reachability, interpret nmap output, produce structured handoff output, handle minimal-host fallback, and refuse unauthorized public, stealth, broad, or offensive scanning. |

## Scope control

The supplement intentionally avoids making nmap a broad security-scanning domain. It excludes stealth/evasion scanning, NSE brute force, vulnerability exploitation, internet-wide discovery, third-party target enumeration, and aggressive scanning as defaults.

The intended pattern is:

```text
local inspection -> authorized bounded nmap check -> interpretation -> safe verification / handoff
```

## Non-claims

This migration does not claim production readiness, semantic review completion, safety review completion, or execution validation. All added records remain `review.status=draft` pending manual review.

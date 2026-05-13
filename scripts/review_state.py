#!/usr/bin/env python3
"""Track record/family review state without re-reviewing unchanged records.

This tool is intentionally deterministic. It does not decide whether a record is
correct. It only computes canonical hashes, detects stale review markers, and
lets a human or external review process stamp already-reviewed records/families.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATASET = ROOT / "datasets/debian-admin-bash/debian-admin-bash-sft.jsonl"
DEFAULT_RECORD_MANIFEST = ROOT / "datasets/debian-admin-bash/review/review-manifest.json"
DEFAULT_FAMILY_MANIFEST = ROOT / "datasets/debian-admin-bash/review/family-review-manifest.json"
DEFAULT_RUBRIC = "datasets/debian-admin-bash/review/REVIEW_PLAN.md"
SCHEMA_RECORD_MANIFEST = "https://github.com/rozmiarD/llm-fine-tuning-datasets/review-manifest.v0.1"
SCHEMA_FAMILY_MANIFEST = "https://github.com/rozmiarD/llm-fine-tuning-datasets/family-review-manifest.v0.1"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            record = json.loads(line)
            if not isinstance(record, dict):
                raise ValueError(f"{path}:{line_no}: record is not an object")
            record["__line_no"] = line_no
            records.append(record)
    return records


def write_jsonl(path: Path, records: Iterable[dict[str, Any]]) -> None:
    lines: list[str] = []
    for record in records:
        clean = {k: v for k, v in record.items() if not k.startswith("__")}
        lines.append(json.dumps(clean, ensure_ascii=False, separators=(",", ":")))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def canonical_review_payload(record: dict[str, Any]) -> dict[str, Any]:
    """Return the content that review approval covers.

    Review bookkeeping is excluded so that stamping a record does not invalidate
    itself. Everything else that changes task meaning, safety metadata, target
    OS, prompt, or answer is covered by the hash.
    """
    clean = copy.deepcopy({k: v for k, v in record.items() if not k.startswith("__")})
    meta = clean.get("meta")
    if isinstance(meta, dict):
        meta.pop("review", None)
    return clean


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def record_hash(record: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_json(canonical_review_payload(record)).encode("utf-8")).hexdigest()


def record_review(record: dict[str, Any]) -> dict[str, Any]:
    meta = record.get("meta") if isinstance(record.get("meta"), dict) else {}
    review = meta.get("review") if isinstance(meta.get("review"), dict) else {}
    return review


def record_state(record: dict[str, Any]) -> tuple[str, str | None]:
    current_hash = record_hash(record)
    review = record_review(record)
    status = review.get("status", "draft")
    provenance = review.get("provenance") if isinstance(review.get("provenance"), dict) else {}
    stamped_hash = provenance.get("record_sha256")
    semantic = review.get("semantic_review") is True
    safety = review.get("safety_review") is True

    if status == "reviewed":
        if not semantic or not safety:
            return "stale", "reviewed_without_semantic_or_safety_true"
        if stamped_hash != current_hash:
            return "stale", "record_hash_mismatch_or_missing"
        return "reviewed", None
    if status in {"quarantined", "rejected"}:
        return status, None
    return "draft", None


def family_hash(records_by_id: dict[str, dict[str, Any]], ids: Iterable[str]) -> str:
    payload = []
    for record_id in sorted(ids):
        if record_id not in records_by_id:
            raise KeyError(f"unknown record id in family: {record_id}")
        payload.append({"id": record_id, "record_sha256": record_hash(records_by_id[record_id])})
    return hashlib.sha256(canonical_json(payload).encode("utf-8")).hexdigest()


def prompt_signature(record: dict[str, Any]) -> str:
    user = ""
    for message in record.get("messages", []):
        if isinstance(message, dict) and message.get("role") == "user":
            user = str(message.get("content", ""))
            break
    normalized = user.lower()
    normalized = re.sub(r"```.*?```", "```X```", normalized, flags=re.S)
    normalized = re.sub(r"\b\d+\b", "N", normalized)
    normalized = re.sub(r"\s+", " ", normalized).strip()
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:16]


def derived_family_id(record: dict[str, Any]) -> str:
    meta = record.get("meta") if isinstance(record.get("meta"), dict) else {}
    explicit = meta.get("family_id")
    if isinstance(explicit, str) and explicit.strip():
        return explicit.strip()
    subdomain = meta.get("subdomain", "unknown")
    return f"auto:{subdomain}:{prompt_signature(record)}"


def build_record_manifest(dataset: Path, records: list[dict[str, Any]], include_drafts: bool = False) -> dict[str, Any]:
    summary: dict[str, int] = {"draft": 0, "reviewed": 0, "stale": 0, "quarantined": 0, "rejected": 0}
    entries: dict[str, Any] = {}
    for record in records:
        record_id = record.get("id")
        if not isinstance(record_id, str):
            raise ValueError(f"line {record.get('__line_no')}: missing string id")
        state, reason = record_state(record)
        summary[state] = summary.get(state, 0) + 1
        review = record_review(record)
        provenance = review.get("provenance") if isinstance(review.get("provenance"), dict) else {}
        if include_drafts or state != "draft":
            entries[record_id] = {
                "record_sha256": record_hash(record),
                "state": state,
                "stale_reason": reason,
                "review_status": review.get("status", "draft"),
                "semantic_review": review.get("semantic_review") is True,
                "safety_review": review.get("safety_review") is True,
                "reviewed_at": provenance.get("reviewed_at"),
                "reviewer": provenance.get("reviewer"),
                "review_batch": provenance.get("review_batch"),
                "family_id": derived_family_id(record),
            }
    return {
        "$schema": SCHEMA_RECORD_MANIFEST,
        "dataset": rel(dataset),
        "generated_at": utc_now(),
        "record_count": len(records),
        "summary": summary,
        "records": entries,
    }


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_pretty_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def read_ids(args: argparse.Namespace) -> list[str]:
    ids: list[str] = []
    if getattr(args, "id", None):
        ids.extend(args.id)
    if getattr(args, "ids_file", None):
        for line in Path(args.ids_file).read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                ids.append(line)
    if not ids:
        raise SystemExit("no ids supplied; use --id or --ids-file")
    seen: set[str] = set()
    out: list[str] = []
    for record_id in ids:
        if record_id not in seen:
            seen.add(record_id)
            out.append(record_id)
    return out


def cmd_write_manifest(args: argparse.Namespace) -> int:
    dataset = Path(args.dataset)
    records = load_jsonl(dataset)
    manifest = build_record_manifest(dataset, records, include_drafts=args.include_drafts)
    write_pretty_json(Path(args.manifest), manifest)
    print(f"wrote {rel(Path(args.manifest))} records={len(records)} summary={manifest['summary']}")
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    dataset = Path(args.dataset)
    records = load_jsonl(dataset)
    manifest = build_record_manifest(dataset, records)
    summary = manifest["summary"]
    print(f"dataset={rel(dataset)} records={len(records)} summary={summary}")

    stale = [rid for rid, entry in manifest["records"].items() if entry["state"] == "stale"]
    if stale:
        print("stale_records:")
        for rid in stale[: args.limit]:
            entry = manifest["records"][rid]
            print(f"- {rid}: {entry['stale_reason']}")
        if len(stale) > args.limit:
            print(f"... {len(stale) - args.limit} more")

    family_manifest_path = Path(args.family_manifest)
    if family_manifest_path.exists():
        family_manifest = load_json(family_manifest_path, {})
        records_by_id = {r["id"]: r for r in records if isinstance(r.get("id"), str)}
        stale_families = []
        for family_id, entry in family_manifest.get("families", {}).items():
            ids = entry.get("record_ids", [])
            try:
                current = family_hash(records_by_id, ids)
            except KeyError as exc:
                stale_families.append((family_id, str(exc)))
                continue
            if current != entry.get("family_sha256"):
                stale_families.append((family_id, "family_hash_mismatch"))
        if stale_families:
            print("stale_families:")
            for family_id, reason in stale_families[: args.limit]:
                print(f"- {family_id}: {reason}")
            if len(stale_families) > args.limit:
                print(f"... {len(stale_families) - args.limit} more")
            return 1

    return 1 if stale else 0


def cmd_list(args: argparse.Namespace) -> int:
    records = load_jsonl(Path(args.dataset))
    wanted = set(args.state)
    count = 0
    for record in records:
        state, reason = record_state(record)
        if state in wanted:
            print(record["id"] if reason is None else f"{record['id']}\t{reason}")
            count += 1
            if args.limit and count >= args.limit:
                break
    return 0


def cmd_stamp_records(args: argparse.Namespace) -> int:
    dataset = Path(args.dataset)
    records = load_jsonl(dataset)
    records_by_id = {r["id"]: r for r in records if isinstance(r.get("id"), str)}
    ids = read_ids(args)
    missing = [record_id for record_id in ids if record_id not in records_by_id]
    if missing:
        raise SystemExit(f"unknown record ids: {', '.join(missing[:10])}")

    reviewed_at = args.reviewed_at or utc_now()
    for record_id in ids:
        record = records_by_id[record_id]
        meta = record.setdefault("meta", {})
        review = meta.setdefault("review", {})
        review["status"] = "reviewed"
        review["semantic_review"] = True
        review["safety_review"] = True
        execution = review.setdefault("execution_validation", {})
        execution["mode"] = args.execution_mode
        execution["status"] = args.execution_status
        if args.execution_reason:
            execution["reason"] = args.execution_reason
        review["provenance"] = {
            "reviewed_at": reviewed_at,
            "reviewer": args.reviewer,
            "rubric": args.rubric,
            "record_sha256": record_hash(record),
            "review_batch": args.review_batch,
        }
    write_jsonl(dataset, records)
    print(f"stamped reviewed records={len(ids)} dataset={rel(dataset)} batch={args.review_batch}")
    return 0


def cmd_stamp_family(args: argparse.Namespace) -> int:
    dataset = Path(args.dataset)
    records = load_jsonl(dataset)
    records_by_id = {r["id"]: r for r in records if isinstance(r.get("id"), str)}
    ids = read_ids(args)
    missing = [record_id for record_id in ids if record_id not in records_by_id]
    if missing:
        raise SystemExit(f"unknown record ids: {', '.join(missing[:10])}")
    manifest_path = Path(args.family_manifest)
    manifest = load_json(
        manifest_path,
        {
            "$schema": SCHEMA_FAMILY_MANIFEST,
            "dataset": rel(dataset),
            "generated_at": utc_now(),
            "families": {},
        },
    )
    manifest["generated_at"] = utc_now()
    manifest.setdefault("families", {})[args.family_id] = {
        "family_id": args.family_id,
        "family_sha256": family_hash(records_by_id, ids),
        "record_ids": sorted(ids),
        "record_count": len(ids),
        "status": "reviewed",
        "reviewed_at": args.reviewed_at or utc_now(),
        "reviewer": args.reviewer,
        "review_batch": args.review_batch,
        "rubric": args.rubric,
        "aspects": sorted(set(args.aspect)),
        "notes": args.notes,
    }
    write_pretty_json(manifest_path, manifest)
    print(f"stamped family={args.family_id} records={len(ids)} manifest={rel(manifest_path)}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", default=str(DEFAULT_DATASET))
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("write-manifest", help="write deterministic record review manifest")
    p.add_argument("--manifest", default=str(DEFAULT_RECORD_MANIFEST))
    p.add_argument("--include-drafts", action="store_true", help="include every draft record entry; default stores only non-draft/stale/reviewed entries")
    p.set_defaults(func=cmd_write_manifest)

    p = sub.add_parser("status", help="summarize draft/reviewed/stale state")
    p.add_argument("--family-manifest", default=str(DEFAULT_FAMILY_MANIFEST))
    p.add_argument("--limit", type=int, default=25)
    p.set_defaults(func=cmd_status)

    p = sub.add_parser("list", help="list records by state")
    p.add_argument("--state", action="append", choices=["draft", "reviewed", "stale", "quarantined", "rejected"], required=True)
    p.add_argument("--limit", type=int, default=0)
    p.set_defaults(func=cmd_list)

    p = sub.add_parser("stamp-records", help="mark explicit records as reviewed and hash-bound")
    p.add_argument("--id", action="append")
    p.add_argument("--ids-file")
    p.add_argument("--reviewer", required=True)
    p.add_argument("--review-batch", required=True)
    p.add_argument("--reviewed-at")
    p.add_argument("--rubric", default=DEFAULT_RUBRIC)
    p.add_argument("--execution-mode", default="static_only", choices=["not_executed", "static_only", "container", "manual"])
    p.add_argument("--execution-status", default="passed", choices=["not_applicable", "pending", "passed", "failed", "skipped"])
    p.add_argument("--execution-reason")
    p.set_defaults(func=cmd_stamp_records)

    p = sub.add_parser("stamp-family", help="mark an explicit record family as consistency-reviewed")
    p.add_argument("--family-manifest", default=str(DEFAULT_FAMILY_MANIFEST))
    p.add_argument("--family-id", required=True)
    p.add_argument("--id", action="append")
    p.add_argument("--ids-file")
    p.add_argument("--reviewer", required=True)
    p.add_argument("--review-batch", required=True)
    p.add_argument("--reviewed-at")
    p.add_argument("--rubric", default=DEFAULT_RUBRIC)
    p.add_argument("--aspect", action="append", default=["semantic_consistency", "safety_consistency", "diversity"])
    p.add_argument("--notes")
    p.set_defaults(func=cmd_stamp_family)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

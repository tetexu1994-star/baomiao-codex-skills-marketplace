"""Build a deterministic public catalog for GitHub Pages and clients."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import copy
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional, Tuple

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from scripts.validate_catalog import ROOT, load_entries, validate_all
else:
    from .validate_catalog import ROOT, load_entries, validate_all


def build(*, generated_at: Optional[str] = None) -> Tuple[Path, Path]:
    errors = validate_all()
    if errors:
        raise ValueError("\n".join(errors))
    generated_at = generated_at or datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    entries = []
    for _, original in load_entries():
        entry = copy.deepcopy(original)
        candidates = [
            json.loads(path.read_text(encoding="utf-8"))
            for path in sorted((ROOT / "catalog" / "candidates").glob(f"{entry['id']}-*.json"))
        ]
        candidate = next(item for item in candidates if item.get("commit") == entry["source"]["commit"] and item.get("path") == entry["source"]["path"])
        evidence = candidate.get("license_evidence")
        if isinstance(evidence, str):
            matching = next((item for item in candidate["files"] if item["path"] == evidence), None)
            evidence = {"scope": "skill-directory", "path": evidence, "sha256": matching["sha256"] if matching else None}
        entry["integrity"] = {
            "algorithm": "sha256",
            "file_count": candidate["scan"]["file_count"],
            "total_bytes": candidate["scan"]["total_bytes"],
            "files": candidate["files"],
            "license_evidence": evidence,
        }
        entries.append(entry)
    entries.sort(key=lambda item: item["id"])
    document = {
        "schema_version": 1,
        "marketplace": {
            "id": "baomiao-codex-skills",
            "name_zh": "暴喵 Codex Skills 市场",
            "generated_at": generated_at,
            "review_policy": "human-approved-only",
            "client_contract": "docs/client-contract.md"
        },
        "entries": entries,
    }
    payload = (json.dumps(document, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    digest = hashlib.sha256(payload).hexdigest()
    dist = ROOT / "dist"
    site = ROOT / "site"
    dist.mkdir(exist_ok=True)
    site.mkdir(exist_ok=True)
    catalog_path = dist / "catalog.json"
    digest_path = dist / "catalog.sha256"
    catalog_path.write_bytes(payload)
    digest_path.write_text(f"{digest}  catalog.json\n", encoding="utf-8")
    shutil.copy2(catalog_path, site / "catalog.json")
    shutil.copy2(digest_path, site / "catalog.sha256")
    site_docs = site / "docs"
    site_docs.mkdir(exist_ok=True)
    shutil.copy2(ROOT / "docs" / "client-contract.md", site_docs / "client-contract.md")
    return catalog_path, digest_path


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="构建公开市场目录")
    parser.add_argument("--generated-at", help="用于可复现构建的 ISO 时间")
    args = parser.parse_args(argv)
    try:
        catalog, digest = build(generated_at=args.generated_at)
    except ValueError as exc:
        print(f"构建失败：\n{exc}", file=sys.stderr)
        return 1
    print(f"已生成 {catalog} 和 {digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Build a deterministic public catalog for GitHub Pages and clients."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import copy
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional, Tuple

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from scripts.validate_catalog import ROOT, load_entries, validate_all
else:
    from .validate_catalog import ROOT, load_entries, validate_all


def current_commit() -> str:
    commit = subprocess.check_output(
        ["git", "-C", str(ROOT), "rev-parse", "HEAD"], text=True, stderr=subprocess.PIPE
    ).strip()
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError("无法取得本地市场固定提交")
    return commit


def build_import_descriptor(*, source: str, ref: str, public_base_url: str, catalog_digest: str, plugin_count: int) -> Tuple[Path, Path]:
    is_release = source.startswith("https://")
    if is_release:
        if not re.fullmatch(r"https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", source):
            raise ValueError("发布版 marketplace_source 必须是 GitHub HTTPS 仓库")
        if not public_base_url.startswith("https://"):
            raise ValueError("发布版 public_base_url 必须使用 HTTPS")
    elif source != str(ROOT):
        raise ValueError("本地预览只接受当前仓库绝对路径")
    if not re.fullmatch(r"[0-9a-f]{40}", ref):
        raise ValueError("marketplace_ref 必须是 40 位固定提交")

    base = public_base_url.rstrip("/")
    args = ["plugin", "marketplace", "add", source]
    if is_release:
        args.extend(["--ref", ref])
    display_source = source if is_release else f'"{source}"'
    display = f"codex plugin marketplace add {display_source}"
    if is_release:
        display += f" --ref {ref}"
    market_manifest = ROOT / ".agents" / "plugins" / "marketplace.json"
    descriptor = {
        "schema_version": 1,
        "profile": "release" if is_release else "local-preview",
        "marketplace": {
            "id": "baomiao-codex",
            "display_name": "暴喵 Codex 插件市场",
            "source": source,
            "ref": ref,
            "manifest_path": ".agents/plugins/marketplace.json",
            "manifest_sha256": hashlib.sha256(market_manifest.read_bytes()).hexdigest(),
            "plugin_count": plugin_count,
        },
        "catalog": {
            "url": f"{base}/catalog.json",
            "sha256_url": f"{base}/catalog.sha256",
            "sha256": catalog_digest,
        },
        "command": {"executable": "codex", "args": args, "display": display},
    }
    payload = (json.dumps(descriptor, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    digest = hashlib.sha256(payload).hexdigest()
    target = ROOT / "site" / "marketplace-import.json"
    digest_target = ROOT / "site" / "marketplace-import.sha256"
    target.write_bytes(payload)
    digest_target.write_text(f"{digest}  marketplace-import.json\n", encoding="utf-8")
    return target, digest_target


def build(*, generated_at: Optional[str] = None, marketplace_source: Optional[str] = None, marketplace_ref: Optional[str] = None, public_base_url: Optional[str] = None) -> Tuple[Path, Path]:
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
        integrity_files = copy.deepcopy(candidate["files"])
        if isinstance(evidence, dict) and evidence.get("scope") == "repository":
            layout = entry.get("source", {}).get("layout", "single-skill")
            packaged_license = (
                ROOT / "plugins" / entry["id"] / "skills" / "LICENSE"
                if layout == "skill-bundle"
                else ROOT / "plugins" / entry["id"] / "skills" / entry["id"] / "LICENSE"
            )
            integrity_files.append({
                "path": "LICENSE",
                "bytes": packaged_license.stat().st_size,
                "sha256": hashlib.sha256(packaged_license.read_bytes()).hexdigest(),
            })
        entry["integrity"] = {
            "algorithm": "sha256",
            "file_count": len(integrity_files),
            "total_bytes": sum(item["bytes"] for item in integrity_files),
            "files": integrity_files,
            "license_evidence": evidence,
        }
        entries.append(entry)
    entries.sort(key=lambda item: item["id"])
    document = {
        "schema_version": 1,
        "marketplace": {
            "id": "baomiao-codex-skills",
            "name_zh": "暴喵 Codex 插件市场",
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
    build_import_descriptor(
        source=marketplace_source or str(ROOT),
        ref=marketplace_ref or current_commit(),
        public_base_url=public_base_url or "http://127.0.0.1:8000",
        catalog_digest=digest,
        plugin_count=len(entries),
    )
    site_docs = site / "docs"
    site_docs.mkdir(exist_ok=True)
    shutil.copy2(ROOT / "docs" / "client-contract.md", site_docs / "client-contract.md")
    return catalog_path, digest_path


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="构建公开市场目录")
    parser.add_argument("--generated-at", help="用于可复现构建的 ISO 时间")
    parser.add_argument("--marketplace-source", help="发布仓库 HTTPS URL；省略时生成本地预览描述")
    parser.add_argument("--marketplace-ref", help="发布仓库的 40 位固定提交")
    parser.add_argument("--public-base-url", help="GitHub Pages 根 URL；省略时使用本地 8000 端口")
    args = parser.parse_args(argv)
    try:
        catalog, digest = build(
            generated_at=args.generated_at,
            marketplace_source=args.marketplace_source,
            marketplace_ref=args.marketplace_ref,
            public_base_url=args.public_base_url,
        )
    except ValueError as exc:
        print(f"构建失败：\n{exc}", file=sys.stderr)
        return 1
    print(f"已生成 {catalog} 和 {digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

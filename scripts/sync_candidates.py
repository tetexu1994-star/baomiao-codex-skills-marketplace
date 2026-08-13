"""Fetch allowlisted upstream trees and produce review candidates only."""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional, Tuple

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from scripts.net import fetch_bytes, fetch_json
    from scripts.security import scan_files, sha256_bytes
else:
    from .net import fetch_bytes, fetch_json
    from .security import scan_files, sha256_bytes

ROOT = Path(__file__).resolve().parents[1]


def github_parts(repository: str) -> Tuple[str, str]:
    match = re.fullmatch(r"https://github\.com/([^/]+)/([^/]+)", repository)
    if not match:
        raise ValueError(f"不是允许的 GitHub 仓库 URL：{repository}")
    return match.group(1), match.group(2)


def resolve_commit(owner: str, repo: str, ref: str, token: Optional[str]) -> str:
    data = fetch_json(f"https://api.github.com/repos/{owner}/{repo}/commits/{ref}", token=token)
    commit = data.get("sha", "")
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError("上游没有返回固定的 40 位提交哈希")
    return commit


def list_tree(owner: str, repo: str, commit: str, token: Optional[str]) -> List[dict]:
    url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{commit}?recursive=1"
    data = fetch_json(url, max_bytes=4_194_304, token=token)
    if data.get("truncated"):
        raise ValueError("GitHub tree 响应被截断，拒绝不完整扫描")
    return data.get("tree", [])


def fetch_directory(owner: str, repo: str, commit: str, path: str, tree: List[dict], max_file_bytes: int, token: Optional[str]) -> List[Tuple[str, bytes]]:
    prefix = path.rstrip("/") + "/"
    blobs = [item for item in tree if item.get("type") == "blob" and item.get("path", "").startswith(prefix)]
    if not blobs or not any(item["path"] == prefix + "SKILL.md" for item in blobs):
        raise ValueError(f"目录不存在或缺少 SKILL.md：{path}")
    files: List[Tuple[str, bytes]] = []
    for item in sorted(blobs, key=lambda value: value["path"]):
        if item.get("size", 0) > max_file_bytes:
            raise ValueError(f"文件超过限制：{item['path']}")
        api_url = f"https://api.github.com/repos/{owner}/{repo}/git/blobs/{item['sha']}"
        blob = fetch_json(api_url, max_bytes=max_file_bytes * 2, token=token)
        if blob.get("encoding") != "base64":
            raise ValueError(f"不支持的 blob 编码：{item['path']}")
        content = base64.b64decode(blob["content"], validate=False)
        if len(content) > max_file_bytes:
            raise ValueError(f"文件超过限制：{item['path']}")
        files.append((item["path"][len(prefix):], content))
    return files


def candidate_document(source: dict, path: str, commit: str, files: List[Tuple[str, bytes]], checked_at: str) -> dict:
    file_map = dict(files)
    license_name = next((name for name in source["license_files"] if name in file_map), None)
    report = scan_files(files)
    if not license_name:
        report["findings"].append({
            "severity": "blocked", "rule": "missing-license", "path": path,
            "detail": "Skill 目录没有允许清单指定的许可证文件"
        })
        report["verdict"] = "blocked"
    return {
        "candidate_schema_version": 1,
        "source_id": source["id"],
        "repository": source["repository"],
        "commit": commit,
        "path": path,
        "checked_at": checked_at,
        "policy": "candidate-only",
        "files": [{"path": name, "bytes": len(content), "sha256": sha256_bytes(content)} for name, content in files],
        "license_evidence": license_name,
        "scan": report,
        "review": {"status": "candidate", "reviewer": None, "note": "自动同步结果不能直接发布"},
    }


def sync(*, ref: str = "main", checked_at: Optional[str] = None, output: Optional[Path] = None) -> List[Path]:
    config = json.loads((ROOT / "sources.json").read_text(encoding="utf-8"))
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    checked_at = checked_at or datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    output = output or ROOT / "catalog" / "candidates"
    output.mkdir(parents=True, exist_ok=True)
    written: List[Path] = []
    for source in config["sources"]:
        owner, repo = github_parts(source["repository"])
        commit = resolve_commit(owner, repo, ref, token)
        tree = list_tree(owner, repo, commit, token)
        for path in source["allowed_paths"]:
            files = fetch_directory(owner, repo, commit, path, tree, source["max_file_bytes"], token)
            candidate = candidate_document(source, path, commit, files, checked_at)
            name = f"{path.rstrip('/').split('/')[-1]}-{commit[:12]}.json"
            target = output / name
            target.write_text(json.dumps(candidate, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            written.append(target)
    return written


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="同步允许来源到候选区（不会发布）")
    parser.add_argument("--ref", default="main", help="上游 ref；结果始终解析成提交哈希")
    parser.add_argument("--checked-at", help="固定候选时间，便于可复现测试")
    parser.add_argument("--output", type=Path, help="候选输出目录")
    args = parser.parse_args(argv)
    try:
        paths = sync(ref=args.ref, checked_at=args.checked_at, output=args.output)
    except Exception as exc:
        print(f"同步失败：{exc}", file=sys.stderr)
        return 1
    print(f"已生成 {len(paths)} 个候选；未修改公开目录")
    for path in paths:
        print(f"- {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

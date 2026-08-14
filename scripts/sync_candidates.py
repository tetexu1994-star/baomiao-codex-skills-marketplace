"""Fetch allowlisted upstream trees and produce review candidates only."""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import subprocess
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


def validate_ref(ref: str) -> str:
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._/-]{0,199}", ref) or ".." in ref:
        raise ValueError(f"不安全的 Git ref：{ref}")
    return ref


def normalize_git_url(url: str) -> str:
    return url.rstrip("/").removesuffix(".git")


def git_output(repository: Path, *args: str, text: bool = True):
    return subprocess.check_output(
        ["git", "-C", str(repository), *args],
        text=text,
        stderr=subprocess.PIPE,
    )


def resolve_local_commit(repository: Path, ref: str, expected_repository: str) -> str:
    if not (repository / ".git").exists():
        raise ValueError(f"本地来源不是 Git 仓库：{repository}")
    remote = git_output(repository, "remote", "get-url", "origin").strip()
    if normalize_git_url(remote) != normalize_git_url(expected_repository):
        raise ValueError(f"本地来源 origin 不匹配：{repository}")
    commit = git_output(repository, "rev-parse", "--verify", f"{validate_ref(ref)}^{{commit}}").strip()
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError("本地 Git 没有返回固定的 40 位提交哈希")
    return commit


def validate_content_kind(path: str, files: List[Tuple[str, bytes]], content_kind: str) -> None:
    names = {name for name, _ in files}
    if content_kind == "skill-directory":
        if "SKILL.md" not in names:
            raise ValueError(f"目录不存在或缺少 SKILL.md：{path}")
        return
    if content_kind == "skill-bundle":
        if not any(name.endswith("/SKILL.md") for name in names):
            raise ValueError(f"Skill 集合不存在或没有子目录 SKILL.md：{path}")
        return
    raise ValueError(f"不支持的 content_kind：{content_kind}")


def fetch_local_directory(repository: Path, commit: str, path: str, max_file_bytes: int, content_kind: str = "skill-directory") -> List[Tuple[str, bytes]]:
    prefix = path.rstrip("/") + "/"
    listing = git_output(repository, "ls-tree", "-r", "-l", commit, "--", path).splitlines()
    files: List[Tuple[str, bytes]] = []
    for line in listing:
        match = re.fullmatch(r"\d+ blob ([0-9a-f]{40})\s+(\d+|-)\t(.+)", line)
        if not match:
            raise ValueError(f"无法解析本地 Git tree：{line}")
        _, size_text, full_path = match.groups()
        if not full_path.startswith(prefix):
            raise ValueError(f"文件逃逸允许目录：{full_path}")
        if size_text == "-" or int(size_text) > max_file_bytes:
            raise ValueError(f"文件超过限制：{full_path}")
        content = git_output(repository, "show", f"{commit}:{full_path}", text=False)
        if len(content) > max_file_bytes:
            raise ValueError(f"文件超过限制：{full_path}")
        files.append((full_path[len(prefix):], content))
    if not files:
        raise ValueError(f"目录不存在：{path}")
    validate_content_kind(path, files, content_kind)
    return files


def fetch_local_file(repository: Path, commit: str, path: str, max_file_bytes: int) -> bytes:
    content = git_output(repository, "show", f"{commit}:{path}", text=False)
    if len(content) > max_file_bytes:
        raise ValueError(f"文件超过限制：{path}")
    return content


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


def fetch_directory(owner: str, repo: str, commit: str, path: str, tree: List[dict], max_file_bytes: int, token: Optional[str], content_kind: str = "skill-directory") -> List[Tuple[str, bytes]]:
    prefix = path.rstrip("/") + "/"
    blobs = [item for item in tree if item.get("type") == "blob" and item.get("path", "").startswith(prefix)]
    if not blobs:
        raise ValueError(f"目录不存在：{path}")
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
    validate_content_kind(path, files, content_kind)
    return files


def fetch_tree_file(owner: str, repo: str, path: str, tree: List[dict], max_file_bytes: int, token: Optional[str]) -> bytes:
    item = next((value for value in tree if value.get("type") == "blob" and value.get("path") == path), None)
    if not item:
        raise ValueError(f"仓库许可证不存在：{path}")
    if item.get("size", 0) > max_file_bytes:
        raise ValueError(f"文件超过限制：{path}")
    blob = fetch_json(f"https://api.github.com/repos/{owner}/{repo}/git/blobs/{item['sha']}", max_bytes=max_file_bytes * 2, token=token)
    if blob.get("encoding") != "base64":
        raise ValueError(f"不支持的 blob 编码：{path}")
    return base64.b64decode(blob["content"], validate=False)


def candidate_document(source: dict, path: str, commit: str, files: List[Tuple[str, bytes]], checked_at: str, repository_license: Optional[bytes] = None) -> dict:
    file_map = dict(files)
    repository_scope = source.get("license_scope") == "repository"
    license_name = source["license_files"][0] if repository_scope and repository_license is not None else next((name for name in source["license_files"] if name in file_map), None)
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
        "package_id": source.get("package_ids", {}).get(path, path.rstrip("/").split("/")[-1]),
        "content_kind": source.get("content_kind", "skill-directory"),
        "repository": source["repository"],
        "commit": commit,
        "path": path,
        "checked_at": checked_at,
        "policy": "candidate-only",
        "files": [{"path": name, "bytes": len(content), "sha256": sha256_bytes(content)} for name, content in files],
        "license_evidence": {
            "scope": "repository" if repository_scope else "skill-directory",
            "path": license_name,
            "sha256": sha256_bytes(repository_license) if repository_scope and repository_license is not None else sha256_bytes(file_map[license_name]) if license_name else None,
        },
        "scan": report,
        "review": {"status": "candidate", "reviewer": None, "note": "自动同步结果不能直接发布"},
    }


def sync(*, ref: str = "main", checked_at: Optional[str] = None, output: Optional[Path] = None, local_sources: Optional[dict[str, Path]] = None, source_ids: Optional[set[str]] = None) -> List[Path]:
    config = json.loads((ROOT / "sources.json").read_text(encoding="utf-8"))
    validate_ref(ref)
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    checked_at = checked_at or datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    output = output or ROOT / "catalog" / "candidates"
    output.mkdir(parents=True, exist_ok=True)
    written: List[Path] = []
    local_sources = local_sources or {}
    configured_ids = {source["id"] for source in config["sources"]}
    unknown_ids = set(local_sources) - configured_ids
    if unknown_ids:
        raise ValueError(f"未知本地来源 ID：{', '.join(sorted(unknown_ids))}")
    if source_ids:
        unknown_filters = source_ids - configured_ids
        if unknown_filters:
            raise ValueError(f"未知来源过滤 ID：{', '.join(sorted(unknown_filters))}")
    for source in config["sources"]:
        if source_ids and source["id"] not in source_ids:
            continue
        local_repository = local_sources.get(source["id"])
        if local_repository:
            commit = resolve_local_commit(local_repository, ref, source["repository"])
            owner = repo = ""
            tree = []
        else:
            owner, repo = github_parts(source["repository"])
            commit = resolve_commit(owner, repo, ref, token)
            tree = list_tree(owner, repo, commit, token)
        repository_license = None
        if source.get("license_scope") == "repository":
            license_path = source["license_files"][0]
            repository_license = (
                fetch_local_file(local_repository, commit, license_path, source["max_file_bytes"])
                if local_repository
                else fetch_tree_file(owner, repo, license_path, tree, source["max_file_bytes"], token)
            )
        for path in source["allowed_paths"]:
            content_kind = source.get("content_kind", "skill-directory")
            if local_repository:
                files = fetch_local_directory(local_repository, commit, path, source["max_file_bytes"], content_kind)
            else:
                files = fetch_directory(owner, repo, commit, path, tree, source["max_file_bytes"], token, content_kind)
            candidate = candidate_document(source, path, commit, files, checked_at, repository_license)
            package_id = source.get("package_ids", {}).get(path, path.rstrip("/").split("/")[-1])
            name = f"{package_id}-{commit[:12]}.json"
            target = output / name
            target.write_text(json.dumps(candidate, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            written.append(target)
    return written


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="同步允许来源到候选区（不会发布）")
    parser.add_argument("--ref", default="main", help="上游 ref；结果始终解析成提交哈希")
    parser.add_argument("--checked-at", help="固定候选时间，便于可复现测试")
    parser.add_argument("--output", type=Path, help="候选输出目录")
    parser.add_argument(
        "--local-source", action="append", default=[], metavar="SOURCE_ID=PATH",
        help="从匹配 origin 的本地 Git 对象读取；可重复指定，未指定来源仍走 GitHub API",
    )
    parser.add_argument("--source", action="append", default=[], help="只同步指定来源 ID；可重复指定")
    args = parser.parse_args(argv)
    try:
        local_sources = {}
        for value in args.local_source:
            source_id, separator, raw_path = value.partition("=")
            if not separator or not source_id or not raw_path:
                raise ValueError("--local-source 格式必须为 SOURCE_ID=PATH")
            if source_id in local_sources:
                raise ValueError(f"本地来源 ID 重复：{source_id}")
            local_sources[source_id] = Path(raw_path).resolve()
        paths = sync(ref=args.ref, checked_at=args.checked_at, output=args.output, local_sources=local_sources, source_ids=set(args.source))
    except Exception as exc:
        print(f"同步失败：{exc}", file=sys.stderr)
        return 1
    print(f"已生成 {len(paths)} 个候选；未修改公开目录")
    for path in paths:
        print(f"- {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

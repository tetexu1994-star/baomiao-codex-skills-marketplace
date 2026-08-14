"""Validate approved entries before they can reach the public catalog."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import List, Optional, Set, Tuple

from jsonschema import Draft202012Validator, FormatChecker

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from scripts.net import fetch_bytes
else:
    from .net import fetch_bytes

ROOT = Path(__file__).resolve().parents[1]
APPROVED = ROOT / "catalog" / "approved"


def load_entries(directory: Path = APPROVED) -> List[Tuple[Path, dict]]:
    return [(path, json.loads(path.read_text(encoding="utf-8"))) for path in sorted(directory.glob("*.json"))]


def semantic_errors(path: Path, entry: dict, *, root: Path = ROOT) -> List[str]:
    errors: List[str] = []
    source = entry.get("source", {})
    review = entry.get("review", {})
    risk = entry.get("risk", {})
    install = entry.get("install", {})
    commit = source.get("commit", "")
    source_path = source.get("path", "")
    repository = source.get("repository", "")
    if path.stem != entry.get("id"):
        errors.append("文件名必须与 id 一致")
    if review.get("status") != "approved":
        errors.append("公开目录只接受 approved 条目")
    if review.get("reviewer", "").lower() in {"machine", "automation", "sync-bot"}:
        errors.append("审核者不得是自动同步程序")
    evidence = review.get("evidence", "")
    if evidence and not (root / evidence).is_file():
        errors.append(f"审核证据不存在：{evidence}")
    if risk.get("level") not in {"low", "medium", "high"}:
        errors.append("blocked 风险不得发布")
    if risk.get("has_executable_files") is not False:
        errors.append("包含可执行文件的 Skill 不得发布")
    capabilities = risk.get("capabilities", [])
    if "none" in capabilities and len(capabilities) != 1:
        errors.append("能力 none 不能与其他能力并存")
    if install.get("requires_auth") and "credentials" not in capabilities:
        errors.append("需要认证时必须声明 credentials 能力")
    if risk.get("level") == "high":
        if "confirm-enhanced-permissions" not in install.get("preflight", []):
            errors.append("高风险条目必须启用增强权限确认")
        if capabilities == ["none"] or not capabilities:
            errors.append("高风险条目必须列出具体能力")
    match = re.fullmatch(r"https://github\.com/([^/]+)/([^/]+)", repository)
    if match and re.fullmatch(r"[0-9a-f]{40}", commit) and source_path:
        owner, repo = match.groups()
        prefix = f"https://raw.githubusercontent.com/{owner}/{repo}/{commit}/{source_path}"
        if source.get("skill_url") != f"{prefix}/SKILL.md":
            errors.append("skill_url 必须对应固定提交与目录")
        license_path = source.get("license_path", "")
        expected_license = (
            f"https://raw.githubusercontent.com/{owner}/{repo}/{commit}/{license_path}"
            if entry.get("license", {}).get("scope") == "repository"
            else f"{prefix}/{license_path}"
        )
        if source.get("license_url") != expected_license:
            errors.append("license_url 必须对应固定提交与目录")
    return errors


def bundle_errors(entry: dict, *, root: Path = ROOT) -> List[str]:
    """Ensure the installable plugin is byte-for-byte the reviewed candidate."""
    if entry.get("install", {}).get("mode") == "source-direct":
        return candidate_errors(entry, root=root)
    entry_id = entry["id"]
    errors: List[str] = []
    plugin_root = root / "plugins" / entry_id
    skill_root = plugin_root / "skills" / entry_id
    manifest_path = plugin_root / ".codex-plugin" / "plugin.json"
    candidate_paths = sorted((root / "catalog" / "candidates").glob(f"{entry_id}*.json"))
    if not candidate_paths:
        return ["缺少对应候选摘要"]
    if not manifest_path.is_file():
        return ["缺少 Codex plugin.json"]
    candidates = [json.loads(path.read_text(encoding="utf-8")) for path in candidate_paths]
    candidate = next((item for item in candidates if item.get("commit") == entry["source"]["commit"] and item.get("path") == entry["source"]["path"]), None)
    if candidate is None:
        return ["没有与 approved 固定来源相同的候选摘要"]
    if candidate.get("scan", {}).get("verdict") != "review-required":
        errors.append("候选自动扫描未通过")
    expected = {item["path"]: item["sha256"] for item in candidate.get("files", [])}
    if entry.get("license", {}).get("scope") == "repository":
        evidence = candidate.get("license_evidence", {})
        if not isinstance(evidence, dict) or not re.fullmatch(r"[0-9a-f]{64}", evidence.get("sha256", "")):
            errors.append("仓库级许可证候选证据不完整")
        else:
            expected["LICENSE"] = evidence["sha256"]
    actual_paths = sorted(path.relative_to(skill_root).as_posix() for path in skill_root.rglob("*") if path.is_file()) if skill_root.is_dir() else []
    if sorted(expected) != actual_paths:
        errors.append("插件 Skill 文件清单与审核候选不一致")
    for relative_path, expected_hash in expected.items():
        local_path = skill_root / relative_path
        if local_path.is_file() and hashlib.sha256(local_path.read_bytes()).hexdigest() != expected_hash:
            errors.append(f"插件文件摘要不匹配：{relative_path}")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("name") != entry_id:
        errors.append("plugin.json 名称与条目 id 不一致")
    if manifest.get("repository") != entry["source"]["repository"]:
        errors.append("plugin.json 没有保留原始仓库身份")
    if manifest.get("license") != entry["license"]["spdx"]:
        errors.append("plugin.json 许可证与审核条目不一致")
    if entry["source"]["commit"] not in manifest.get("homepage", ""):
        errors.append("plugin.json homepage 未固定到审核提交")
    return errors


def candidate_errors(entry: dict, *, root: Path = ROOT) -> List[str]:
    """Ensure source-direct entries still point at the exact reviewed candidate."""
    entry_id = entry["id"]
    candidates = [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted((root / "catalog" / "candidates").glob(f"{entry_id}-*.json"))
    ]
    candidate = next((item for item in candidates if item.get("commit") == entry["source"]["commit"] and item.get("path") == entry["source"]["path"]), None)
    if candidate is None:
        return ["没有与 source-direct 固定来源相同的候选摘要"]
    errors: List[str] = []
    if candidate.get("scan", {}).get("verdict") != "review-required":
        errors.append("source-direct 候选自动扫描未通过")
    if not any(item.get("path") == "SKILL.md" for item in candidate.get("files", [])):
        errors.append("source-direct 候选缺少 SKILL.md 摘要")
    evidence = candidate.get("license_evidence", {})
    if not isinstance(evidence, dict) or evidence.get("scope") != entry["license"]["scope"]:
        errors.append("source-direct 候选许可证作用域不匹配")
    elif evidence.get("path") != entry["source"]["license_path"] or not re.fullmatch(r"[0-9a-f]{64}", evidence.get("sha256", "")):
        errors.append("source-direct 候选许可证证据不完整")
    return errors


def marketplace_errors(entries: List[Tuple[Path, dict]], *, root: Path = ROOT) -> List[str]:
    path = root / ".agents" / "plugins" / "marketplace.json"
    if not path.is_file():
        return ["缺少 .agents/plugins/marketplace.json"]
    market = json.loads(path.read_text(encoding="utf-8"))
    errors: List[str] = []
    if market.get("name") != "baomiao-codex":
        errors.append("Codex 市场名必须为 baomiao-codex")
    plugins = market.get("plugins", [])
    bundled_entries = [entry for _, entry in entries if entry.get("install", {}).get("mode") == "copy-source-directory"]
    if {item.get("name") for item in plugins} != {entry["id"] for entry in bundled_entries}:
        errors.append("Codex 插件市场条目必须与 approved 中的打包条目完全一致")
    entries_by_id = {entry["id"]: entry for entry in bundled_entries}
    for plugin in plugins:
        expected_path = f"./plugins/{plugin.get('name')}"
        if plugin.get("source") != {"source": "local", "path": expected_path}:
            errors.append(f"{plugin.get('name')}: marketplace source 必须指向本仓库插件目录")
        policy = plugin.get("policy", {})
        entry = entries_by_id.get(plugin.get("name"), {})
        allowed_authentication = {"ON_INSTALL", "ON_USE"} if entry.get("install", {}).get("requires_auth") else {"ON_INSTALL"}
        if policy.get("installation") != "AVAILABLE" or policy.get("authentication") not in allowed_authentication:
            errors.append(f"{plugin.get('name')}: marketplace policy 不完整")
    return errors


def validate_all(directory: Path = APPROVED, *, root: Path = ROOT, online: bool = False) -> List[str]:
    schema = json.loads((root / "schema" / "skill.schema.json").read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors: List[str] = []
    seen: Set[str] = set()
    entries = load_entries(directory)
    if not entries:
        errors.append("公开目录不能为空")
    online_cache: dict[str, bytes] = {}
    for path, entry in entries:
        entry_errors: List[str] = []
        for error in sorted(validator.iter_errors(entry), key=lambda item: list(item.path)):
            location = ".".join(str(part) for part in error.path) or "$"
            entry_errors.append(f"{location}: {error.message}")
        entry_id = entry.get("id")
        if entry_id in seen:
            entry_errors.append(f"id 重复：{entry_id}")
        seen.add(entry_id)
        entry_errors.extend(semantic_errors(path, entry, root=root))
        errors.extend(f"{path.name}: {message}" for message in entry_errors)
        if directory.resolve() == (root / "catalog" / "approved").resolve():
            errors.extend(f"{path.name}: {message}" for message in bundle_errors(entry, root=root))
        if online and not entry_errors:
            try:
                skill_url = entry["source"]["skill_url"]
                license_url = entry["source"]["license_url"]
                skill = online_cache.setdefault(skill_url, fetch_bytes(skill_url)) if skill_url not in online_cache else online_cache[skill_url]
                license_text = online_cache.setdefault(license_url, fetch_bytes(license_url)) if license_url not in online_cache else online_cache[license_url]
                if not skill.startswith(b"---"):
                    errors.append(f"{path.name}: 上游 SKILL.md 缺少 frontmatter")
                if entry["license"]["spdx"] == "Apache-2.0" and b"Apache License" not in license_text:
                    errors.append(f"{path.name}: 上游许可证证据与 SPDX 不匹配")
                if entry["license"]["spdx"] == "MIT" and b"Permission is hereby granted, free of charge" not in license_text:
                    errors.append(f"{path.name}: 上游许可证证据与 SPDX 不匹配")
            except Exception as exc:
                errors.append(f"{path.name}: 在线校验失败：{exc}")
    if directory.resolve() == (root / "catalog" / "approved").resolve():
        errors.extend(marketplace_errors(entries, root=root))
    return errors


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="校验所有已审核 Skill")
    parser.add_argument("--online", action="store_true", help="同时回读固定上游文件")
    args = parser.parse_args(argv)
    errors = validate_all(online=args.online)
    if errors:
        print("目录校验失败：", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"目录校验通过：{len(load_entries())} 个已审核条目")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

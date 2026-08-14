"""Package the manually approved, script-free official Skill bundles.

This command reads committed Git objects only. It writes candidate evidence first,
then updates exactly the packages listed in REVIEWED_PACKAGES. Adding a source to
sources.json never makes it publishable by itself.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path
from typing import Dict

from scripts.sync_candidates import (
    candidate_document,
    fetch_local_directory,
    fetch_local_file,
    normalize_git_url,
)

ROOT = Path(__file__).resolve().parents[1]
REVIEWED_AT = "2026-08-14T05:00:00Z"
CHECKED_AT = "2026-08-14T04:30:00Z"
EVIDENCE = "docs/reviews/official-plugin-expansion-2026-08-14.md"

REVIEWED_PACKAGES = {
    "amazon-location-service": {
        "source_id": "aws-agent-plugins-official",
        "commit": "bab56a3b9991aa0c6857b05198a61ba14a60bce4",
        "path": "plugins/amazon-location-service/skills",
        "entrypoint": "amazon-location-service/SKILL.md",
        "name": "Amazon 地图与位置服务",
        "summary": "为应用接入地图、地点搜索、地理编码、路线规划和围栏能力，并提供 Amazon Location Service 的认证与集成建议。",
        "category": "研发工具",
        "tags": ["AWS", "地图", "地理编码", "路线规划"],
        "publisher": "Amazon Web Services",
        "publisher_url": "https://github.com/awslabs",
        "license": "Apache-2.0",
        "license_file": "LICENSE",
        "requires_auth": True,
        "risk": ["filesystem-read", "filesystem-write", "network", "shell", "credentials", "external-write"],
        "risk_note": "包内无脚本；工作流会修改项目并可能调用 AWS 服务，使用云账号前必须展示来源和权限。",
        "market_category": "Developer Tools",
    },
    "aws-amplify": {
        "source_id": "aws-agent-plugins-official",
        "commit": "bab56a3b9991aa0c6857b05198a61ba14a60bce4",
        "path": "plugins/aws-amplify/skills",
        "entrypoint": "amplify-workflow/SKILL.md",
        "name": "AWS Amplify 全栈开发",
        "summary": "使用 Amplify Gen 2 构建认证、数据、存储、GraphQL API 与函数，并生成适合当前项目的全栈落地步骤。",
        "category": "研发工具",
        "tags": ["AWS", "Amplify", "全栈", "云开发"],
        "publisher": "Amazon Web Services",
        "publisher_url": "https://github.com/awslabs",
        "license": "Apache-2.0",
        "license_file": "LICENSE",
        "requires_auth": True,
        "risk": ["filesystem-read", "filesystem-write", "network", "shell", "credentials", "external-write"],
        "risk_note": "包内无脚本；会生成项目配置并可能部署到 AWS，任何云端写入仍需用户逐次确认。",
        "market_category": "Developer Tools",
    },
    "codebase-documentor-for-aws": {
        "source_id": "aws-agent-plugins-official",
        "commit": "bab56a3b9991aa0c6857b05198a61ba14a60bce4",
        "path": "plugins/codebase-documentor-for-aws/skills",
        "entrypoint": "document-service/SKILL.md",
        "name": "AWS 代码库文档生成",
        "summary": "分析 CDK、CloudFormation、Terraform 与应用代码，生成带源码引用的架构和组件文档，适合接手存量 AWS 项目。",
        "category": "文档处理",
        "tags": ["AWS", "代码库", "架构文档", "IaC"],
        "publisher": "Amazon Web Services",
        "publisher_url": "https://github.com/awslabs",
        "license": "Apache-2.0",
        "license_file": "LICENSE",
        "requires_auth": False,
        "risk": ["filesystem-read", "filesystem-write", "shell", "network"],
        "risk_note": "包内无脚本；会遍历代码库并写入文档，联网仅用于按用户要求查询 AWS 资料。",
        "market_category": "Productivity",
    },
    "azure-agent-skills": {
        "source_id": "microsoft-agent-skills-official",
        "commit": "00be373fec26109c3087728188f6a45554c47617",
        "path": "skills",
        "entrypoint": "azure-architecture/SKILL.md",
        "name": "Azure 官方技能合集",
        "summary": "一个插件收录 202 个 Microsoft Azure Skills，覆盖计算、数据、AI、网络、安全、迁移和运维，不把同系列能力拆成数百张卡片。",
        "category": "研发工具",
        "tags": ["Microsoft", "Azure", "云计算", "合集"],
        "publisher": "Microsoft",
        "publisher_url": "https://github.com/MicrosoftDocs",
        "license": "CC-BY-4.0",
        "license_file": "LICENSE",
        "requires_auth": True,
        "risk": ["filesystem-read", "filesystem-write", "network", "shell", "credentials", "external-write", "system-config"],
        "risk_note": "包含 202 个纯文档 Skills；部分工作流会调用 Azure CLI 或修改云资源，执行前必须再次确认。",
        "market_category": "Developer Tools",
    },
    "nvidia-skills": {
        "source_id": "nvidia-skills-official",
        "commit": "e1b747ed9fc0492342f97cc6ba7ac954279ac48f",
        "path": "plugins/nvidia-skills/skills",
        "entrypoint": "nvidia-skill-finder/SKILL.md",
        "name": "NVIDIA Skill 查找器",
        "summary": "从 NVIDIA 官方技能体系中定位适合 GPU、CUDA、推理、训练、机器人和仿真的 Skill，并给出来源与安装建议。",
        "category": "研发工具",
        "tags": ["NVIDIA", "GPU", "CUDA", "AI"],
        "publisher": "NVIDIA",
        "publisher_url": "https://github.com/NVIDIA",
        "license": "CC-BY-4.0",
        "license_file": "LICENSE-CC-BY-4.0",
        "requires_auth": False,
        "risk": ["filesystem-read", "filesystem-write", "network", "shell"],
        "risk_note": "仅打包官方 Skill Finder，不批量复制 NVIDIA 大仓库；建议安装任何结果前仍需单独核对来源。",
        "market_category": "Developer Tools",
    },
}


def git_output(repository: Path, *args: str, text: bool = True):
    return subprocess.check_output(["git", "-C", str(repository), *args], text=text, stderr=subprocess.PIPE)


def verify_repository(repository: Path, expected_url: str, commit: str) -> None:
    origin = git_output(repository, "remote", "get-url", "origin").strip()
    if normalize_git_url(origin).lower() != normalize_git_url(expected_url).lower():
        raise ValueError(f"本地来源 origin 不匹配：{origin}")
    resolved = git_output(repository, "rev-parse", f"{commit}^{{commit}}").strip()
    if resolved != commit:
        raise ValueError(f"本地来源缺少审核固定提交：{commit}")


def reject_executable_modes(repository: Path, commit: str, source_path: str) -> None:
    listing = git_output(repository, "ls-tree", "-r", commit, "--", source_path).splitlines()
    for line in listing:
        mode, _, _, path = line.split(maxsplit=3)
        if mode == "120000":
            raise ValueError(f"候选包含符号链接：{path}")
        if mode.endswith("755"):
            raise ValueError(f"候选包含可执行文件模式：{path}")


def manifest(package_id: str, data: dict, repository_url: str) -> dict:
    capabilities = ["Read", "Write"]
    if "network" in data["risk"]:
        capabilities.append("Network")
    return {
        "name": package_id,
        "version": "1.0.0",
        "description": data["summary"],
        "author": {"name": data["publisher"], "url": data["publisher_url"]},
        "repository": repository_url,
        "homepage": f"{repository_url}/tree/{data['commit']}/{data['path']}",
        "license": data["license"],
        "skills": "./skills/",
        "interface": {
            "displayName": data["name"],
            "shortDescription": data["summary"],
            "longDescription": f"固定来源于 {data['publisher']} 官方仓库；{data['risk_note']}",
            "developerName": data["publisher"],
            "category": data["market_category"],
            "capabilities": capabilities,
            "defaultPrompt": [f"使用 {data['name']} 处理当前任务，并在执行命令或外部写入前说明影响。"],
        },
    }


def approved_entry(package_id: str, data: dict, source: dict) -> dict:
    owner_repo = source["repository"].removeprefix("https://github.com/")
    prefix = f"https://raw.githubusercontent.com/{owner_repo}/{data['commit']}"
    return {
        "schema_version": 1,
        "id": package_id,
        "name": data["name"],
        "summary_zh": data["summary"],
        "category": data["category"],
        "tags": data["tags"],
        "publisher": {"name": data["publisher"], "kind": "official", "url": data["publisher_url"]},
        "source": {
            "repository": source["repository"],
            "commit": data["commit"],
            "path": data["path"],
            "layout": "skill-bundle",
            "entrypoint_path": data["entrypoint"],
            "skill_url": f"{prefix}/{data['path']}/{data['entrypoint']}",
            "license_url": f"{prefix}/{data['license_file']}",
            "license_path": data["license_file"],
        },
        "license": {"spdx": data["license"], "scope": "repository", "verified_at": "2026-08-14"},
        "risk": {"level": "high", "capabilities": data["risk"], "has_executable_files": False, "notes_zh": data["risk_note"]},
        "review": {"status": "approved", "reviewer": "暴喵市场维护者（官方扩容）", "reviewed_at": REVIEWED_AT, "evidence": EVIDENCE},
        "install": {
            "mode": "copy-source-directory",
            "destination": f"%USERPROFILE%/.codex/skills/{package_id}",
            "requires_auth": data["requires_auth"],
            "preflight": [
                "verify-catalog-digest", "verify-source-commit", "verify-license", "scan-files",
                "show-source-and-risk", "confirm-user", "confirm-enhanced-permissions", "backup-existing",
            ],
        },
    }


def package(local_sources: Dict[str, Path]) -> int:
    source_document = json.loads((ROOT / "sources.json").read_text(encoding="utf-8"))
    sources = {source["id"]: source for source in source_document["sources"]}
    marketplace_path = ROOT / ".agents" / "plugins" / "marketplace.json"
    marketplace = json.loads(marketplace_path.read_text(encoding="utf-8"))
    marketplace["plugins"] = [entry for entry in marketplace["plugins"] if entry.get("name") != "appwrite"]
    market_entries = {entry["name"]: entry for entry in marketplace["plugins"]}

    # The Appwrite source failed the pipe-to-shell gate after scaffolding.
    rejected_scaffold = ROOT / "plugins" / "appwrite"
    if rejected_scaffold.exists():
        shutil.rmtree(rejected_scaffold)

    for package_id, data in REVIEWED_PACKAGES.items():
        source = sources[data["source_id"]]
        repository = local_sources.get(data["source_id"])
        if repository is None:
            raise ValueError(f"缺少 --local-source {data['source_id']}=PATH")
        verify_repository(repository, source["repository"], data["commit"])
        reject_executable_modes(repository, data["commit"], data["path"])
        files = fetch_local_directory(repository, data["commit"], data["path"], source["max_file_bytes"], "skill-bundle")
        license_bytes = fetch_local_file(repository, data["commit"], data["license_file"], source["max_file_bytes"])
        candidate = candidate_document(source, data["path"], data["commit"], files, CHECKED_AT, license_bytes)
        if candidate["scan"]["verdict"] != "review-required":
            blocked = ", ".join(f"{item['rule']}:{item['path']}" for item in candidate["scan"]["findings"] if item["severity"] == "blocked")
            raise ValueError(f"{package_id} 未通过自动门禁：{blocked}")
        candidate_path = ROOT / "catalog" / "candidates" / f"{package_id}-{data['commit'][:12]}.json"
        candidate_path.write_text(json.dumps(candidate, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

        plugin_root = ROOT / "plugins" / package_id
        manifest_path = plugin_root / ".codex-plugin" / "plugin.json"
        if not manifest_path.is_file():
            raise ValueError(f"插件尚未由 plugin-creator 创建：{package_id}")
        skill_root = plugin_root / "skills"
        if skill_root.exists():
            shutil.rmtree(skill_root)
        skill_root.mkdir(parents=True)
        for file_info in candidate["files"]:
            content = git_output(repository, "show", f"{data['commit']}:{data['path']}/{file_info['path']}", text=False)
            if hashlib.sha256(content).hexdigest() != file_info["sha256"]:
                raise ValueError(f"候选摘要不匹配：{package_id}/{file_info['path']}")
            target = skill_root / file_info["path"]
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
        (skill_root / "LICENSE").write_bytes(license_bytes)
        manifest_path.write_text(json.dumps(manifest(package_id, data, source["repository"]), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        approved = approved_entry(package_id, data, source)
        (ROOT / "catalog" / "approved" / f"{package_id}.json").write_text(json.dumps(approved, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        market_entry = market_entries.get(package_id)
        if market_entry is None:
            raise ValueError(f"marketplace 缺少 plugin-creator 条目：{package_id}")
        market_entry["category"] = data["market_category"]
        market_entry["policy"] = {
            "installation": "AVAILABLE",
            "authentication": "ON_USE" if data["requires_auth"] else "ON_INSTALL",
        }

    marketplace_path.write_text(json.dumps(marketplace, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return len(REVIEWED_PACKAGES)


def parse_local_sources(values: list[str]) -> Dict[str, Path]:
    result: Dict[str, Path] = {}
    for value in values:
        source_id, separator, path = value.partition("=")
        if not separator or not source_id or not path or not re.fullmatch(r"[a-z0-9-]+", source_id):
            raise ValueError("--local-source 格式必须为 SOURCE_ID=PATH")
        result[source_id] = Path(path).resolve()
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="封装人工审核通过的官方 Codex Skill 合集")
    parser.add_argument("--local-source", action="append", default=[], metavar="SOURCE_ID=PATH")
    args = parser.parse_args()
    try:
        count = package(parse_local_sources(args.local_source))
    except Exception as exc:
        print(f"官方插件封装失败：{exc}")
        return 1
    print(f"已封装 {count} 个官方 Codex 插件")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

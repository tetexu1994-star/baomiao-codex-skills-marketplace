"""Package reviewed Harness Skill directories as real Codex plugins.

The plugin roots must first be created with plugin-creator's scaffold command.
This command fills only the 52 entries recorded in REVIEW_METADATA, reads bytes
from the fixed Git commit, and adds the repository-scoped Apache license.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

from scripts.review_harness import COMMIT, REPOSITORY, REVIEW_METADATA, make_entry
from scripts.sync_candidates import normalize_git_url

ROOT = Path(__file__).resolve().parents[1]
CATEGORY_MAP = {
    "研发工具": "Developer Tools",
    "安全治理": "Developer Tools",
    "数据分析": "Productivity",
    "效率规划": "Productivity",
}


def git_bytes(repository: Path, object_name: str) -> bytes:
    return subprocess.check_output(
        ["git", "-C", str(repository), "show", object_name],
        stderr=subprocess.PIPE,
    )


def load_candidate(skill_id: str, entry: dict) -> dict:
    candidates = [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted((ROOT / "catalog" / "candidates").glob(f"{skill_id}-*.json"))
    ]
    return next(
        item for item in candidates
        if item.get("commit") == COMMIT and item.get("path") == entry["source"]["path"]
    )


def manifest(skill_id: str, entry: dict, external_write: bool) -> dict:
    capabilities = ["Network"]
    if external_write:
        capabilities.append("Write")
    return {
        "name": skill_id,
        "version": "1.0.0",
        "description": entry["summary_zh"],
        "author": {"name": "Harness", "url": "https://github.com/harness"},
        "repository": REPOSITORY,
        "homepage": f"{REPOSITORY}/tree/{COMMIT}/{entry['source']['path']}",
        "license": "Apache-2.0",
        "skills": "./skills/",
        "interface": {
            "displayName": entry["name"],
            "shortDescription": entry["summary_zh"],
            "longDescription": f"固定来源于 Harness 官方 Skills；{entry['risk']['notes_zh']}",
            "developerName": "Harness",
            "category": CATEGORY_MAP.get(entry["category"], "Productivity"),
            "capabilities": capabilities,
            "defaultPrompt": [f"使用 {entry['name']} 完成当前任务，并在外部写入前说明影响。"],
        },
    }


def package(repository: Path) -> int:
    origin = subprocess.check_output(
        ["git", "-C", str(repository), "remote", "get-url", "origin"],
        text=True,
        stderr=subprocess.PIPE,
    ).strip()
    if normalize_git_url(origin) != REPOSITORY:
        raise ValueError(f"本地来源 origin 不匹配：{origin}")
    resolved = subprocess.check_output(
        ["git", "-C", str(repository), "rev-parse", f"{COMMIT}^{{commit}}"],
        text=True,
        stderr=subprocess.PIPE,
    ).strip()
    if resolved != COMMIT:
        raise ValueError("本地来源缺少审核固定提交")

    license_bytes = git_bytes(repository, f"{COMMIT}:LICENSE")
    written = 0
    for skill_id, data in sorted(REVIEW_METADATA.items()):
        entry = make_entry(skill_id, data)
        candidate = load_candidate(skill_id, entry)
        plugin_root = ROOT / "plugins" / skill_id
        manifest_path = plugin_root / ".codex-plugin" / "plugin.json"
        if not manifest_path.is_file():
            raise ValueError(f"插件尚未由 plugin-creator 创建：{skill_id}")
        skill_root = plugin_root / "skills" / skill_id
        if skill_root.exists():
            shutil.rmtree(skill_root)
        skill_root.mkdir(parents=True)
        for file_info in candidate["files"]:
            relative_path = file_info["path"]
            target = skill_root / relative_path
            target.parent.mkdir(parents=True, exist_ok=True)
            content = git_bytes(
                repository,
                f"{COMMIT}:{entry['source']['path']}/{relative_path}",
            )
            if hashlib.sha256(content).hexdigest() != file_info["sha256"]:
                raise ValueError(f"候选摘要不匹配：{skill_id}/{relative_path}")
            target.write_bytes(content)
        (skill_root / "LICENSE").write_bytes(license_bytes)
        manifest_path.write_text(
            json.dumps(manifest(skill_id, entry, data[3]), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        written += 1
    return written


def main() -> int:
    parser = argparse.ArgumentParser(description="把已审核 Harness 目录封装为 Codex 插件")
    parser.add_argument("--local-source", type=Path, required=True, help="Harness 官方仓库本地 Git 路径")
    args = parser.parse_args()
    try:
        count = package(args.local_source.resolve())
    except Exception as exc:
        print(f"插件封装失败：{exc}")
        return 1
    print(f"已封装 {count} 个 Harness Codex 插件")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

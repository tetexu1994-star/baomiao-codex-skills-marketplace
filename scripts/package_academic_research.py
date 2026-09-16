"""Package the reviewed, script-free academic research Skill bundle."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path

from scripts.sync_candidates import candidate_document, fetch_local_directory, fetch_local_file, normalize_git_url

ROOT = Path(__file__).resolve().parents[1]
SOURCE_ID = "academic-research-community"
PACKAGE_ID = "academic-research-toolkit"
COMMIT = "9b1b256e99055006725fe4c6b8f90d301ceef7b0"
SOURCE_PATH = "skills"
CHECKED_AT = "2026-09-16T08:00:00Z"
REVIEWED_AT = "2026-09-16T08:30:00Z"
EVIDENCE = "docs/reviews/chinese-academic-research-expansion-2026-09-16.md"

README_ZH = f"""# 中文学术研究工具箱

这个插件把 10 项学术研究工作流放进同一个中文入口，适合论文精读、文献综述、科研写作、研究设计、同行评审、图表和学术汇报。

## 直接这样问

- `用中文精读这篇论文，列出研究问题、方法、主要结论、证据强弱和局限。`
- `把这些论文整理成文献综述，按主题归类，并保留每个判断的出处。`
- `以审稿人视角检查这篇论文，按必须修改、建议修改和可选优化排序。`
- `帮我设计这个研究课题，区分研究问题、假设、方法、风险和下一步。`
- `把这组研究结果改成适合论文或答辩的图表，并说明图形选择理由。`

## 能力对应

| 中文任务 | 对应 Skill |
| --- | --- |
| 论文精读、跨论文综合 | `literature-reading-and-synthesis` |
| 科研写作与结构修改 | `scientific-writing` |
| 投稿、返修与同行评审 | `publishing-and-peer-review` |
| 研究设计与项目规划 | `research-strategy-and-project-design` |
| 科研图表 | `data-visualization-and-figures` |
| 学术汇报与公众表达 | `scientific-communication` |
| 基金申请 | `grant-writing` |
| 反馈、导师与实验室管理 | `research-feedback`、`mentoring-management-and-lab-culture` |
| 科研职业发展 | `career-development` |

## 使用边界

- 插件包仅包含 Markdown，不带安装脚本、可执行文件或账号凭证。
- 需要联网核对论文或引用时，应优先使用公开原始来源，并保留可追溯链接。
- SciSpace、Consensus、Scite、Elicit 等论文数据库属于 Codex 官方连接型插件，需要用户在 Codex 内自行连接；本插件不会代替登录或上传凭证。
- 任何投稿、提交或对外发布操作都应在执行前让用户确认。

## 来源说明

研究方法文件来自 [JJ Froehlich 的 agent-skills-for-academic-research](https://github.com/jjfroehlich/agent-skills-for-academic-research)，固定到提交 `{COMMIT}`，许可证为 MIT。上游内容保持原样；本中文说明、市场摘要和默认提示由暴喵市场补充。
"""


def git_output(repository: Path, *args: str, text: bool = True):
    return subprocess.check_output(["git", "-C", str(repository), *args], text=text, stderr=subprocess.PIPE)


def verify_repository(repository: Path, expected_url: str) -> None:
    if not (repository / ".git").is_dir():
        raise ValueError(f"不是 Git 仓库：{repository}")
    remote = git_output(repository, "remote", "get-url", "origin").strip()
    if normalize_git_url(remote) != normalize_git_url(expected_url):
        raise ValueError(f"上游 origin 不匹配：{remote}")
    resolved = git_output(repository, "rev-parse", "HEAD^{commit}").strip()
    if resolved != COMMIT:
        raise ValueError(f"上游提交不匹配：{resolved}")


def reject_executable_modes(repository: Path) -> None:
    listing = git_output(repository, "ls-tree", "-r", COMMIT, "--", SOURCE_PATH)
    executable = [line for line in listing.splitlines() if line.startswith("100755 ")]
    if executable:
        raise ValueError("上游包含 executable mode 文件")


def manifest(source: dict) -> dict:
    homepage = f"{source['repository']}/tree/{COMMIT}/{SOURCE_PATH}"
    return {
        "name": PACKAGE_ID,
        "version": "1.0.0",
        "description": "面向中文用户的论文阅读、文献综合、科研写作、同行评审与研究设计工具箱。",
        "author": {"name": "JJ Froehlich", "url": "https://github.com/jjfroehlich"},
        "repository": source["repository"],
        "homepage": homepage,
        "license": "MIT",
        "keywords": ["学术研究", "论文", "文献综述", "科研写作", "同行评审"],
        "skills": "./skills/",
        "interface": {
            "displayName": "中文学术研究工具箱",
            "shortDescription": "读论文、做综述、写作与同行评审。",
            "longDescription": "为中文研究者整理的 10 项学术工作流，配有中文说明与默认提示，覆盖论文精读、文献综合、科研写作、研究设计、投稿评审、图表与学术汇报。来源固定、无脚本、无需上传账号凭证。",
            "developerName": "JJ Froehlich",
            "category": "Productivity",
            "capabilities": ["Read", "Write", "Network"],
            "defaultPrompt": [
                "用中文精读这篇论文，提取主张、证据与局限。",
                "把这些论文整理成有出处的文献综述框架。",
                "用同行评审视角检查这篇论文并给出修改优先级。",
            ],
        },
    }


def approved_entry(source: dict) -> dict:
    prefix = f"https://raw.githubusercontent.com/jjfroehlich/agent-skills-for-academic-research/{COMMIT}"
    return {
        "schema_version": 1,
        "id": PACKAGE_ID,
        "name": "中文学术研究工具箱",
        "summary_zh": "配有中文说明与默认提示，覆盖论文精读、文献综合、科研写作、研究设计、同行评审、科研图表与学术汇报的 10 项研究工作流。",
        "category": "教育科研",
        "tags": ["论文", "文献综述", "科研写作", "同行评审", "研究设计", "科研图表"],
        "publisher": {"name": "JJ Froehlich", "kind": "community", "url": "https://github.com/jjfroehlich"},
        "source": {
            "repository": source["repository"],
            "commit": COMMIT,
            "path": SOURCE_PATH,
            "layout": "skill-bundle",
            "entrypoint_path": "literature-reading-and-synthesis/SKILL.md",
            "skill_url": f"{prefix}/{SOURCE_PATH}/literature-reading-and-synthesis/SKILL.md",
            "license_url": f"{prefix}/LICENSE",
            "license_path": "LICENSE",
        },
        "license": {"spdx": "MIT", "scope": "repository", "verified_at": "2026-09-16"},
        "risk": {
            "level": "medium",
            "capabilities": ["filesystem-read", "filesystem-write", "network", "browser"],
            "has_executable_files": False,
            "notes_zh": "插件包仅含 Markdown；按任务可能读取论文、联网核对公开来源并在用户目录生成研究笔记，不包含安装脚本或凭证文件。",
        },
        "review": {
            "status": "approved",
            "reviewer": "暴喵市场维护者（中文科研扩容）",
            "reviewed_at": REVIEWED_AT,
            "evidence": EVIDENCE,
        },
        "install": {
            "mode": "copy-source-directory",
            "destination": "%USERPROFILE%/.codex/skills/academic-research-toolkit",
            "requires_auth": False,
            "preflight": [
                "verify-catalog-digest",
                "verify-source-commit",
                "verify-license",
                "scan-files",
                "show-source-and-risk",
                "confirm-user",
                "backup-existing",
            ],
        },
    }


def package(repository: Path) -> int:
    document = json.loads((ROOT / "sources.json").read_text(encoding="utf-8"))
    source = next(item for item in document["sources"] if item["id"] == SOURCE_ID)
    verify_repository(repository, source["repository"])
    reject_executable_modes(repository)
    files = fetch_local_directory(repository, COMMIT, SOURCE_PATH, source["max_file_bytes"], "skill-bundle")
    license_bytes = fetch_local_file(repository, COMMIT, "LICENSE", source["max_file_bytes"])
    candidate = candidate_document(source, SOURCE_PATH, COMMIT, files, CHECKED_AT, license_bytes)
    if candidate["scan"]["verdict"] != "review-required" or candidate["scan"]["findings"]:
        raise ValueError("候选未通过无脚本、无高危模式门禁")
    candidate_path = ROOT / "catalog" / "candidates" / f"{PACKAGE_ID}-{COMMIT[:12]}.json"
    candidate_path.write_text(json.dumps(candidate, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    plugin_root = ROOT / "plugins" / PACKAGE_ID
    manifest_path = plugin_root / ".codex-plugin" / "plugin.json"
    if not manifest_path.is_file():
        raise ValueError("插件尚未由 plugin-creator 创建")
    skill_root = plugin_root / "skills"
    if skill_root.exists():
        shutil.rmtree(skill_root)
    skill_root.mkdir(parents=True)
    for file_info in candidate["files"]:
        content = git_output(repository, "show", f"{COMMIT}:{SOURCE_PATH}/{file_info['path']}", text=False)
        if hashlib.sha256(content).hexdigest() != file_info["sha256"]:
            raise ValueError(f"候选摘要不匹配：{file_info['path']}")
        target = skill_root / file_info["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
    (skill_root / "LICENSE").write_bytes(license_bytes)
    (plugin_root / "README.zh-CN.md").write_text(README_ZH, encoding="utf-8")
    manifest_path.write_text(json.dumps(manifest(source), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    approved = approved_entry(source)
    (ROOT / "catalog" / "approved" / f"{PACKAGE_ID}.json").write_text(
        json.dumps(approved, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    marketplace_path = ROOT / ".agents" / "plugins" / "marketplace.json"
    marketplace = json.loads(marketplace_path.read_text(encoding="utf-8"))
    entry = next(item for item in marketplace["plugins"] if item["name"] == PACKAGE_ID)
    entry["category"] = "Productivity"
    entry["policy"] = {"installation": "AVAILABLE", "authentication": "ON_INSTALL"}
    marketplace_path.write_text(json.dumps(marketplace, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return len(files)


def main() -> int:
    parser = argparse.ArgumentParser(description="打包已审核的中文学术研究插件")
    parser.add_argument("--local-source", type=Path, required=True)
    args = parser.parse_args()
    count = package(args.local_source.resolve())
    print(f"已打包 {PACKAGE_ID}：{count} 个上游文件")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

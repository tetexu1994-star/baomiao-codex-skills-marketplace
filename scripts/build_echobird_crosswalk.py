"""Build a reproducible, read-only crosswalk against the Echobird marketplace.

This command inventories metadata only. It never copies third-party plugin bodies
or promotes entries into the public Baomiao marketplace.
"""

from __future__ import annotations

import argparse
import collections
import json
import subprocess
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_ORIGIN = "https://cnb.cool/echobird/codex-plugins"
PERMISSIVE_DECLARATIONS = {"MIT", "Apache-2.0", "Apache-2.0 AND CC-BY-4.0"}
EXECUTABLE_SUFFIXES = {".bat", ".cmd", ".exe", ".js", ".mjs", ".cjs", ".ps1", ".py", ".sh"}
LICENSE_NAMES = {"license", "license.md", "license.txt", "copying", "copying.md"}


def normalize_git_url(value: str) -> str:
    value = value.strip().removesuffix(".git").rstrip("/")
    if value.startswith("git@"):  # git@host:owner/repo
        host_path = value[4:].replace(":", "/", 1)
        return f"https://{host_path}"
    return value


def git_text(repository: Path, *args: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(repository), *args], text=True, stderr=subprocess.PIPE
    ).strip()


def plugin_shape(plugin_root: Path) -> list[str]:
    shape = []
    if (plugin_root / ".app.json").is_file():
        shape.append("App")
    if (plugin_root / ".mcp.json").is_file():
        shape.append("MCP")
    if (plugin_root / "skills").is_dir():
        shape.append("Skills")
    if (plugin_root / "scripts").is_dir():
        shape.append("Scripts")
    return shape or ["Manifest"]


def license_file(plugin_root: Path) -> str:
    for path in sorted(plugin_root.iterdir()):
        if path.is_file() and path.name.casefold() in LICENSE_NAMES:
            return path.name
    return ""


def executable_files(plugin_root: Path) -> list[str]:
    return sorted(
        path.relative_to(plugin_root).as_posix()
        for path in plugin_root.rglob("*")
        if path.is_file() and path.suffix.casefold() in EXECUTABLE_SUFFIXES
    )


def repository_host(repository: str) -> str:
    return urlparse(repository).netloc or "—"


def relation(plugin_id: str, upstream: str, ours: dict[str, str]) -> str:
    if plugin_id not in ours:
        return "未收录"
    if upstream and upstream == ours[plugin_id]:
        return "已覆盖同源"
    return "同名不同源"


def recommendation(relation_value: str, declared_license: str, evidence: str, executables: list[str]) -> tuple[str, str]:
    if relation_value == "已覆盖同源":
        return "已覆盖", "暴喵已发布相同 ID 与上游来源"
    if declared_license not in PERMISSIVE_DECLARATIONS:
        return "暂不接入", f"许可证声明为 {declared_license or '缺失'}"
    reasons = []
    if not evidence:
        reasons.append("包内缺少许可证证据")
    if executables:
        reasons.append(f"含 {len(executables)} 个脚本/可执行文件")
    if relation_value == "同名不同源":
        reasons.append("与现有同名插件来源不同")
    if reasons:
        return "需单独复核", "；".join(reasons)
    return "可进入候选", "许可文件随包，且未发现脚本/可执行文件"


def escape_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def build(source: Path, output: Path, expected_commit: str | None = None) -> dict:
    origin = normalize_git_url(git_text(source, "remote", "get-url", "origin"))
    if origin != EXPECTED_ORIGIN:
        raise ValueError(f"来源 origin 不匹配：{origin}")
    commit = git_text(source, "rev-parse", "HEAD")
    if expected_commit and commit != expected_commit:
        raise ValueError(f"来源提交不匹配：期望 {expected_commit}，实际 {commit}")

    market_path = source / ".agents" / "plugins" / "marketplace.json"
    market = json.loads(market_path.read_text(encoding="utf-8"))
    our_market = json.loads((ROOT / ".agents" / "plugins" / "marketplace.json").read_text(encoding="utf-8"))
    ours = {}
    for item in our_market["plugins"]:
        manifest_path = ROOT / item["source"]["path"] / ".codex-plugin" / "plugin.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        ours[item["name"]] = manifest.get("repository", "")

    rows = []
    for item in market["plugins"]:
        plugin_id = item["name"]
        plugin_root = source / "plugins" / plugin_id
        manifest_path = plugin_root / ".codex-plugin" / "plugin.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        upstream = manifest.get("repository", "")
        declared_license = manifest.get("license", "")
        evidence = license_file(plugin_root)
        executables = executable_files(plugin_root)
        relation_value = relation(plugin_id, upstream, ours)
        status, reason = recommendation(relation_value, declared_license, evidence, executables)
        rows.append({
            "id": plugin_id,
            "name": manifest.get("interface", {}).get("displayName") or manifest.get("name", plugin_id),
            "category": item.get("category", "Other"),
            "shape": "+".join(plugin_shape(plugin_root)),
            "license": declared_license or "缺失",
            "license_evidence": evidence or "—",
            "repository": upstream or "—",
            "host": repository_host(upstream),
            "relation": relation_value,
            "recommendation": status,
            "reason": reason,
        })

    recommendation_counts = collections.Counter(row["recommendation"] for row in rows)
    license_counts = collections.Counter(row["license"] for row in rows)
    shape_counts = collections.Counter(part for row in rows for part in row["shape"].split("+"))
    repository_counts = collections.Counter(row["repository"] for row in rows)
    external_count = sum(row["repository"] != "https://github.com/openai/plugins" for row in rows)

    lines = [
        "# 百灵鸟 Codex 插件市场逐项对标表",
        "",
        f"- 对标来源：[{EXPECTED_ORIGIN}]({EXPECTED_ORIGIN})",
        f"- 固定提交：`{commit}`",
        f"- 生成条目：{len(rows)}",
        f"- 暴喵当前插件：{len(our_market['plugins'])}",
        "- 用途：仅生成候选判断，不复制或自动发布第三方插件。",
        "",
        "## 结论",
        "",
        f"百灵鸟默认市场共有 **{len(rows)}** 个插件，其中 **{external_count}** 个没有把 `openai/plugins` 声明为上游，说明它确实聚合了多个外部来源。",
        "",
        "| 建议 | 数量 | 含义 |",
        "|---|---:|---|",
    ]
    meanings = {
        "已覆盖": "暴喵已有同 ID、同上游插件",
        "可进入候选": "包内有许可文件且未发现脚本，可进入候选同步，不代表自动发布",
        "需单独复核": "缺许可证据、含脚本或与现有同名插件来源不同",
        "暂不接入": "Proprietary、UNLICENSED 或许可证字段缺失",
    }
    for status in ("已覆盖", "可进入候选", "需单独复核", "暂不接入"):
        lines.append(f"| {status} | {recommendation_counts.get(status, 0)} | {meanings[status]} |")

    lines.extend(["", "## 内容形态", "", "| 形态 | 数量 |", "|---|---:|"])
    for name, count in sorted(shape_counts.items(), key=lambda pair: (-pair[1], pair[0])):
        lines.append(f"| {name} | {count} |")

    lines.extend(["", "## 许可证声明", "", "| 声明 | 数量 |", "|---|---:|"])
    for name, count in sorted(license_counts.items(), key=lambda pair: (-pair[1], pair[0])):
        lines.append(f"| {escape_cell(name)} | {count} |")

    lines.extend(["", "## 主要声明上游", "", "| 仓库 | 数量 |", "|---|---:|"])
    for name, count in repository_counts.most_common(12):
        display = f"[{name}]({name})" if name.startswith("https://") else name
        lines.append(f"| {escape_cell(display)} | {count} |")

    lines.extend([
        "",
        "## 180 项逐项对标",
        "",
        "| # | 插件 ID | 显示名称 | 分类 | 形态 | 许可声明 | 许可文件 | 声明上游 | 与暴喵关系 | 建议 | 原因 |",
        "|---:|---|---|---|---|---|---|---|---|---|---|",
    ])
    for index, row in enumerate(rows, 1):
        upstream = f"[{row['host']}]({row['repository']})" if row["repository"].startswith("https://") else row["repository"]
        cells = [index, row["id"], row["name"], row["category"], row["shape"], row["license"], row["license_evidence"], upstream, row["relation"], row["recommendation"], row["reason"]]
        lines.append("| " + " | ".join(escape_cell(cell) for cell in cells) + " |")

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {
        "commit": commit,
        "entries": len(rows),
        "external_sources": external_count,
        "recommendations": dict(sorted(recommendation_counts.items())),
        "output": str(output),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="生成百灵鸟插件市场逐项对标表")
    parser.add_argument("--source", type=Path, required=True, help="百灵鸟仓库本地克隆目录")
    parser.add_argument("--commit", help="要求匹配的固定提交")
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "docs" / "reviews" / "echobird-marketplace-crosswalk-2026-08-14.md",
    )
    args = parser.parse_args()
    try:
        result = build(args.source.resolve(), args.output.resolve(), args.commit)
    except Exception as exc:
        print(f"生成失败：{exc}")
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

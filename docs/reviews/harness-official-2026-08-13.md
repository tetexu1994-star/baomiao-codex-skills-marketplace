# Harness 官方 Skills 专项复核（2026-08-13）

## 结论

- 来源：`https://github.com/harness/harness-skills`
- 固定提交：`e75f841df3482c00d90144cca37d9b2a3b6ff0fb`
- 许可证：仓库根目录 `LICENSE`，Apache-2.0；公开条目固定到同一提交的许可证原文。
- 文件形态：55 个允许目录均包含 `SKILL.md`，部分目录另含 Markdown 参考资料；没有 `.exe`、`.ps1`、`.bat`、`.cmd`、`.sh`、`.py`、`.js` 等可执行或脚本文件。
- 交付：其中 52 个目录采用 `source-direct`。暴喵仓库不复制正文，客户端从页面展示的 Harness 原始仓库固定提交下载，并逐文件校验候选摘要。
- 依赖：全部需要 Harness MCP v2 和用户自己的 Harness 授权；市场与暴喵客户端不得代管、上传或记录用户凭证。

## 风险分级

- 中风险：只读查询、分析、报告和建议类。声明 `network`、`credentials`。
- 增强权限：创建、更新、审批、运行、终止、签名、豁免或策略配置类。额外声明 `external-write`，安装前必须通过 `confirm-enhanced-permissions`。
- 静态扫描仅是人工审核入口，不代表运行安全。客户端每次安装仍须重算文件哈希、复扫并展示来源和能力。

## 人工取舍

本轮审核了 55 个目录，发布其中 52 个。它们来自同一个具名厂商官方仓库、许可证范围一致、目录结构一致且无可执行文件。没有把“官方”当作低风险依据；所有会改变 Harness 远端状态的 Skill 均按增强权限发布。

`create-service`、`enforce-sbom`、`enforce-slsa` 暂缓：正文会引用同仓库其他 Skill 的相对路径，单目录安装无法保证这些跨目录参考仍可解析。在客户端契约支持显式依赖图和闭包校验前，不把它们标成可安装。

# 参考仓库审查：leinatorX/codex-skills-marketplace

- 审查时间：2026-08-13（Asia/Shanghai）
- 仓库：<https://github.com/leinatorX/codex-skills-marketplace>
- 审查提交：`013ce9c192a69bd52641640c3901d8e519ee881c`
- 结论：**不镜像、不导入条目；只把公开目录形态作为格式参考。**

## LICENSE

GitHub 仓库 API 的 `license` 为 `null`，递归 tree 中也没有根 `LICENSE`、`COPYING` 或等价文件。公开可读与可 clone 不构成复制、修改或再分发授权，因此不能批量抓取其 Skill 内容发布到暴喵账号。

## README 与目录

README 仅说明市场名、下列目录形态和 Codex 命令：

```text
.agents/plugins/marketplace.json
plugins/<plugin>/.codex-plugin/plugin.json
plugins/<plugin>/skills/<skill>/SKILL.md
```

README 声称内容“建议以 SkillsHub Skills 仓库为唯一源”，但没有给出该源仓库 URL、同步提交或各插件许可证。`.agents/plugins/marketplace.json` 有 7 个本地插件条目和 Codex 所需的 `policy.installation`、`policy.authentication`、`category`，但没有来源提交、许可证、风险、人工审核或校验摘要。

## 抓取与镜像判断

| 行为 | 结论 | 原因 |
|---|---|---|
| 读取 GitHub API / README 做审查 | 允许 | 只读、少量、用于事实核验 |
| 借鉴公开目录概念后独立实现 | 允许 | 未复制其 Skill 正文或品牌内容 |
| 自动抓取全部插件作为候选 | 拒绝 | 缺少上游定位与许可证证据 |
| 将其插件复制到新市场 | 拒绝 | 根目录无许可证，条目也无独立许可 |
| 客户端把它作为备用镜像 | 拒绝 | 来源身份、更新链与再分发权均不清楚 |

## 上游内容与安全风险

递归 tree 显示 7 个插件：`ai-video-director`、`anxin-image-gen`、`anxin-ppt`、`anxin-video-aduit`、`emergency-wechat-writer`、`wechat-article-html-style`、`yingji-linglingqi-knowledge-graph`。

风险证据：

- `anxin-image-gen/scripts/generate_image.py`：可执行 Python。
- `anxin-ppt/scripts/capture-deck-screenshots.ps1`、`package-deck.ps1`、`validate-blue-deck.mjs`：PowerShell/Node 可执行脚本。
- `anxin-video-aduit/scripts/audit_video.py`：可执行 Python。
- 部分 Skill 引用 API 文档，可能涉及网络、认证或外部服务，但条目未声明权限和凭证处理方式。
- 大体积二进制图片和 HTML 模板增加审查面；当前没有每文件摘要或变更审计。

这不表示上述项目一定恶意，而是现有证据不足以满足面向 Windows 新手的一键安装门槛。任何未来纳入都必须找到原始仓库、确认许可证、固定提交、全目录扫描并由人复核。

## 对 MVP 的影响

本项目采用独立 schema、固定上游提交、许可证作用域、风险能力、人工审核证据和候选/发布隔离。没有沿用参考仓库的 Skill 内容、名称、品牌或市场清单。


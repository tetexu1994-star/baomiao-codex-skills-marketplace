# 首批 OpenAI Skills 人工审核

- 审核日期：2026-08-13
- 固定提交：`49f948faa9258a0c61caceaf225e179651397431`
- 仓库：<https://github.com/openai/skills>
- 结论：通过 3 项；所有条目仍须由客户端在安装前重做完整目录扫描。

## 共同证据

每个入选目录都包含独立 `LICENSE.txt`，正文为 Apache License 2.0；许可证与 Skill 作用域在同一目录，不依赖仓库根目录许可。候选同步器通过 GitHub tree API 枚举固定提交下的全部 blob，并记录每个文件的 SHA-256。静态扫描未发现脚本后缀、敏感文件名、pipe-to-shell、编码 PowerShell、危险删除或凭证外传模式。

## define-goal

- 文件：`SKILL.md`、`LICENSE.txt`、`agents/openai.yaml`。
- `SKILL.md` SHA-256：`708df89ff19cbae82a762efae036735d1914b5c7e44df1832e0b723f6cd9ee30`。
- 权限判断：纯目标澄清提示词，不要求文件、网络、Shell 或凭证。
- 风险：低。

## pdf

- 文件：`SKILL.md`、`LICENSE.txt`、`agents/openai.yaml`、`assets/pdf.png`。
- `SKILL.md` SHA-256：`d108cf2b36355ab37eb5962933f4d09785ec002f3105c506129320209306b9d2`。
- 权限判断：指示 Codex 读写 PDF、调用 Poppler/Python 依赖；目录自身无可执行脚本。
- 风险：中。安装页必须展示文件读写和 Shell 能力，运行时仍由 Codex 权限系统控制。

## security-threat-model

- 文件：`SKILL.md`、`LICENSE.txt`、`agents/openai.yaml`、两个 Markdown reference。
- `SKILL.md` SHA-256：`1283c0dd62a8104d9edda4583569b5d8510b4ddaa45120687c999250fd96bad2`。
- 权限判断：读取代码库并生成 Markdown 报告，无网络或脚本要求。
- 风险：中，因为可能读取敏感代码；用户应仅在已授权仓库内运行。

## 未纳入示例

- `screenshot`：含 PowerShell、Python、Shell、Swift 脚本；不符合 MVP 的“无可执行文件”门槛。
- `gh-fix-ci`：含 Python 脚本、网络写权限语境及 GitHub 认证；MVP 暂不纳入。
- `skill-installer`：系统 Skill 且含安装脚本；无必要重复分发，也不符合门槛。


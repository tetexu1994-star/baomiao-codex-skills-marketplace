# 外部市场与来源补充核查（2026-08-13）

## 已查看来源

- MicrosoftDocs/Agent-Skills：Microsoft / Azure 方向，仓库声明代码 MIT、文档 CC-BY-4.0。值得后续按内容类型拆分许可证后引入，未在本轮混用双许可证内容。
- NVIDIA/skills：NVIDIA 官方 Agent Skills，面向 Codex 等编码代理；仓库提供 Apache-2.0 与 CC-BY-4.0 许可说明、技能卡和签名机制。值得后续专项核查，但内容体量和工具链依赖较大。
- vercel-labs/agent-skills：Vercel 官方集合；当前核查的固定克隆中没有可供本市场自动证明作用域的根许可证文件，因此没有批量复制或发布。
- Harness/harness-skills：官方仓库、Apache-2.0 根许可证、明确说明兼容 OpenAI Codex，55 个允许目录在固定提交下均为 Markdown/参考文档且依赖 Harness MCP v2。本轮采用原始来源直装纳入 52 个；3 个存在跨 Skill 相对引用，暂缓到依赖图契约落地。

## 取舍

“别家条目多”可以说明用户需要规模，但不能代替逐条许可证和权限判断。本轮优先选择同源、同许可、目录结构一致且可固定提交的 Harness 条目，形成 72 条可用目录；Microsoft 与 NVIDIA 留作下一批独立许可映射。Vercel 页面虽声明 MIT，但本轮固定提交的仓库树中缺少可直接固定的许可证文件，因此继续暂缓打包。

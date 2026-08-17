# Codex 官方插件目录接入复核（2026-08-17）

## 核验结果

- OpenAI 官方说明将插件定义为可以包含 Skills、MCP 或两者的可安装包，并说明本地 marketplace 用于开发测试；公开插件由产品目录分发：<https://learn.chatgpt.com/docs/build-plugins>。
- `openai/plugins` 历史仓库包含 `.agents/plugins/marketplace.json` 和 `plugins/<name>/` 示例，但 GitHub 在 2026-08-16 将其标记为 archived：<https://github.com/openai/plugins>。
- 归档前默认清单曾包含 180 个条目；这个数字只说明历史快照，不代表用户当前 Codex 账号可见数量，也不进入暴喵市场统计。
- Codex 当前使用原生远程目录，例如 `openai-curated-remote` 与 `openai-api-curated`。这些名称只作为客户端识别提示；最终可用条目以本机 Codex 返回为准。

## 许可与来源结论

不批量复制 `openai/plugins`：仓库根目录没有覆盖全部插件包的统一再分发许可证，单个 manifest 可能声明 MIT、Apache-2.0、Proprietary 或第三方条款。manifest 的 `license` 字段是来源线索，不足以授权整库镜像。

本轮只发布事实型联邦来源描述：来源身份、官方文档、历史归档状态、Codex 只读发现命令和少量示例名称。它不包含插件代码、Skill 内容、App 配置、MCP 配置或认证信息。

## 客户端风险边界

1. 仅通过参数数组调用可信安装路径中的 `codex.exe`，不经过 shell。
2. 只运行 `plugin list --available --json`；网页描述不能覆盖命令或插入额外参数。
3. 官方账号登录、OAuth 和凭证始终由 Codex/对应服务处理，暴喵不读取、不缓存、不上传。
4. 不把历史仓库作为失败回退；原生目录不可用时保留暴喵精选目录，并提示用户从 Codex Plugins 页面查看。
5. 页面中的 GitHub、Figma、Notion、Google Drive、Vercel、Slack、Supabase、Zotero 只是目录示例，不承诺对所有账号可用。

## 取舍

选择“动态原生目录 + 少量示例”而不是在网页复制 180 张卡片。这样牺牲了表面上的大数字，但避免把停更快照伪装成实时目录，也保留了 OpenAI 的来源、认证和可用性判断。

## DeepSeek 独立复核

- 隔离副本、环境诊断和最小连通性测试均通过。
- 一次性只读复核在限定等待时间内没有返回实质内容，随后已主动终止。
- 因此本轮不把任何结论归因于 DeepSeek；交付结论以本地静态检查、自动化测试和浏览器验证为准。

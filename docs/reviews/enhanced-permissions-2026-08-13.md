# 增强权限扩容审查（2026-08-13）

## 结论

在不放宽来源、许可证和可执行文件门槛的前提下，新增 10 个 OpenAI 官方条目，公开目录由 10 个扩至 20 个。固定提交均为 `49f948faa9258a0c61caceaf225e179651397431`；OpenAI 自有目录采用 Apache-2.0，4 个 Notion 目录采用 Notion Labs, Inc. 的标准 MIT 文本。候选摘要记录完整文件清单与 SHA-256。

## 条目与权限

| 条目 | 风险层 | 主要能力 | 人工结论 |
|---|---|---|---|
| Linear | 增强 | OAuth、联网、外部写入 | 可创建/更新事项、项目、标签和评论；需独立确认 |
| Netlify Deploy | 增强 | Shell、凭证、部署 | 会运行 npx、关联/创建站点并发布；需独立确认 |
| Notion Knowledge Capture | 增强 | OAuth、外部写入 | 会创建或更新页面与关系；需独立确认 |
| Notion Meeting Intelligence | 增强 | OAuth、外部写入 | 会创建议程、会前材料和任务；需独立确认 |
| Notion Research Documentation | 增强 | OAuth、外部写入 | 会读取资料并写回报告；需独立确认 |
| Notion Spec to Implementation | 增强 | OAuth、外部写入 | 会创建计划、任务和状态；需独立确认 |
| Playwright Interactive | 增强 | 浏览器、Shell、系统配置 | 上游当前要求 js_repl 与无沙箱运行；必须醒目展示 |
| Security Best Practices | 中 | 文件读写 | 3 份文档含 subprocess 安全示例；人工确认不是安装或执行脚本 |
| WinUI App | 增强 | Shell、联网、系统配置 | 可能启用开发者模式并安装/更新 Visual Studio 与 SDK |
| Yeet | 增强 | Git 写入、凭证、外部写入 | 会暂存、提交、推送并创建/更新 GitHub PR，只在明确请求时使用 |

## 仍然阻断

- `playwright`、`vercel-deploy`、`gh-fix-ci`、`jupyter-notebook`、`migrate-to-codex`：目录含 Shell/Python 脚本。
- `sentry`、`render-deploy`、`cloudflare-deploy`：含 pipe-to-shell。
- Figma 系列：许可证不是可直接再分发的通用开源许可。
- 无许可证、疑似窃密、混淆或上传凭证的任何来源。

## 审核规则变化

静态扫描中的 `subprocess.run/Popen` 文档片段从自动阻断改为人工复核提示；真实 `.py/.sh/.ps1/.js` 文件和 `curl | bash` 仍然阻断。高权限条目需要 `confirm-enhanced-permissions`，普通确认无法替代。

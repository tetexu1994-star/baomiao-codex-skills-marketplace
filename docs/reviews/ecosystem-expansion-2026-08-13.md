# 生态扩容审查（2026-08-13）

> 后续状态：本报告中的 Playwright Interactive、WinUI、Linear、Notion 与 Netlify 暂缓结论，已在 [增强权限扩容审查](enhanced-permissions-2026-08-13.md) 中按新的双层权限策略重新复核；来源、许可和可执行文件结论不变。

## 结论

本轮从公开网络发现的来源中新增 7 个条目，公开目录由 3 个扩至 10 个。新增内容只来自 OpenAI 与 Anthropic 的官方 GitHub 仓库，固定到完整提交哈希；每个上架目录均自带 Apache-2.0 `LICENSE.txt`，完整目录静态扫描为 `review-required`，且人工复核确认不含脚本、二进制安装器、凭证文件或 pipe-to-shell。

“官方来源”只表示仓库发布者身份，不表示其认可暴喵市场。商标仍归各自权利人。

## 已批准条目

| 发布者 | 固定提交 | 路径 | 文件数 | 自动扫描 | 人工风险结论 |
|---|---|---|---:|---|---|
| OpenAI | `49f948faa9258a0c61caceaf225e179651397431` | `skills/.curated/aspnet-core` | 17 | 无命中 | 中；会读写项目并运行 dotnet 命令 |
| OpenAI | `49f948faa9258a0c61caceaf225e179651397431` | `skills/.curated/cli-creator` | 4 | 无命中 | 中；会创建 CLI、运行构建并可能使用目标 API 凭证 |
| Anthropic | `f17010c9bb483898c1d9c9f42dde2b3a98889434` | `skills/frontend-design` | 2 | 无命中 | 中；指导修改前端项目，不含执行文件 |
| Anthropic | `f17010c9bb483898c1d9c9f42dde2b3a98889434` | `skills/internal-comms` | 6 | 无命中 | 低；纯 Markdown 写作指南 |
| Anthropic | `f17010c9bb483898c1d9c9f42dde2b3a98889434` | `skills/theme-factory` | 13 | 无命中 | 中；含只读 PDF 预览，会修改指定制品 |
| Anthropic | `f17010c9bb483898c1d9c9f42dde2b3a98889434` | `skills/brand-guidelines` | 2 | 无命中 | 低；纯品牌参考，另有商标免责声明 |
| Anthropic | `f17010c9bb483898c1d9c9f42dde2b3a98889434` | `skills/claude-api` | 66 | 无命中 | 中；文档本身无脚本，实际 API 开发需要联网和本机凭证 |

以上目录的候选摘要位于 `catalog/candidates/`，插件包中的每个文件必须与候选 SHA-256 完全一致。Anthropic 根仓库包含部分仅 source-available 的办公文档 Skill；本轮只采用上述目录各自携带的 Apache-2.0 许可证，不将根仓库其他目录的许可结论外推。

## 已发现但暂缓或拒绝

| 来源/条目 | 结论 | 原因 |
|---|---|---|
| OpenAI `playwright` | 拒绝 | 自带 `scripts/playwright_cli.sh` |
| OpenAI `playwright-interactive` | 暂缓 | 无脚本但要求 `js_repl` 且当前说明要求关闭沙箱，权限过强 |
| OpenAI `sentry` | 拒绝 | `SKILL.md` 含 `curl ... \| bash` |
| OpenAI `security-best-practices` | 暂缓 | 参考文档包含 `subprocess.run/Popen` 示例，当前静态策略阻断，需隔离式人工分析 |
| OpenAI `winui-app` | 暂缓 | 会启用开发者模式并通过 WinGet 安装/更新 Visual Studio，虽适合 Windows 用户但系统改动较大 |
| OpenAI Figma 系列 | 拒绝 | 目录许可证是 Figma Developer Terms，不作为可自由再分发许可处理 |
| OpenAI 部署、Linear、Notion、Yeet 系列 | 暂缓 | 涉及 OAuth、外部写入、部署或推送，首轮扩容不发布高权限 Skill |
| Anthropic `docx/pdf/pptx/xlsx` | 拒绝 | 上游明确标为 source-available，且目录含脚本；不是本市场可直接再分发的 Apache 示例 |
| Anthropic `algorithmic-art/mcp-builder/skill-creator/slack-gif-creator/webapp-testing/web-artifacts-builder` | 拒绝 | 目录含 JS、Python、Shell 或打包脚本 |
| Anthropic `canvas-design` | 暂缓 | 超过 5 MB，包含大量字体资产与复合许可证，需单独审核 |
| Vercel Labs `agent-skills` | 暂缓 | 当前固定提交未发现根许可证文本；个别 frontmatter 声明不足以替代完整许可证证据 |
| Sentry `sentry-agent-skills` | 拒绝 | 当前固定提交未发现许可证，并已迁移/停止维护 |
| Harness `harness-skills` | 暂缓 | 根许可证明确，但条目以认证后的外部服务读写为主，不适合本轮低风险扩容 |
| NVIDIA `skills` | 候选池 | 官方仓库有双许可证、来源卡、签名与评测；目录规模很大且多含评测/安装脚本，待按单目录完成许可和权限复核后再上架 |
| 社区聚合站与个人合集 | 不镜像 | 可用于发现原始来源，不能替代原作者仓库、固定提交和许可证证据 |

## 关键取舍

1. 从 3 个扩至 10 个，而不是按搜索结果批量导入。Codex 启动时只加载 Skill 名称与描述且会按上下文预算截断，精选的触发描述比数量更重要。
2. 对 Windows 用户有吸引力不等于低风险。WinUI 的系统配置与 Playwright Interactive 的无沙箱要求均保持暂缓。
3. 许可证按最小明确作用域判断。Anthropic 仓库内不同目录许可不同，只批准自带 Apache-2.0 文本的目录。
4. GitHub API 限流不降低验证。同步器增加本地 Git 对象模式，要求 origin 与允许来源一致，按固定提交读取 blob，不信任未提交工作树。
5. “默认候选、人工发布”不变。新增来源仍只由同步器生成候选；本次 approved 元数据、中文说明和权限声明均为独立人工复核结果。

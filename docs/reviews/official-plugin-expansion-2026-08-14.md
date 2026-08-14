# 官方插件扩容复核（2026-08-14）

本轮目标不是增加卡片数量，而是给已可被 Codex 注册的暴喵市场补充一批来源明确、固定版本、适合 Windows 用户的官方能力包。所有结论均从上游 Git 对象读取；市场只发布下表“发布”的 Skill 目录，不复制测试、安装脚本、hooks 或未经固定的运行时依赖。

## 发布清单

| 暴喵插件 | 原始来源 | 固定提交 | 包含 Skill | 许可证 | 自动检查 | 结论 |
|---|---|---:|---:|---|---|---|
| `amazon-location-service` | `awslabs/agent-plugins` | `bab56a3b9991aa0c6857b05198a61ba14a60bce4` | 1 | Apache-2.0 | 无脚本/可执行文件 | 发布 Skill 子树 |
| `aws-amplify` | `awslabs/agent-plugins` | `bab56a3b9991aa0c6857b05198a61ba14a60bce4` | 1 | Apache-2.0 | 无脚本/可执行文件 | 发布 Skill 子树 |
| `codebase-documentor-for-aws` | `awslabs/agent-plugins` | `bab56a3b9991aa0c6857b05198a61ba14a60bce4` | 1 | Apache-2.0 | 无脚本/可执行文件 | 发布 Skill 子树 |
| `azure-agent-skills` | `MicrosoftDocs/Agent-Skills` | `00be373fec26109c3087728188f6a45554c47617` | 202 | CC-BY-4.0 | 217 个文本文件，无脚本/可执行文件 | 作为 1 个官方合集插件发布 |
| `nvidia-skills` | `NVIDIA/skills` | `e1b747ed9fc0492342f97cc6ba7ac954279ac48f` | 1 | CC-BY-4.0 | Skill Finder 子树 7 个文件，无脚本/可执行文件 | 发布官方查找器 Skill 子树 |

合计新增 5 个可安装插件、206 个 Skill。市场总插件数由 72 增至 77；能力数量的增长主要来自 Azure 官方合集，而不是把 202 个相关 Skill 拆成 202 张卡片。

## 为什么只复制 Skill 子树

AWS 的原始插件还包含 MCP 配置，并使用 `uvx ...@latest`，安装时会解析浮动运行时依赖；这不满足本市场“固定提交、可重放”的发布门禁。因此暴喵包明确做成 Skill-only wrapper：保留官方 Skill 原文和许可证，不带 MCP 配置，也不声称包含上游插件的全部运行能力。

NVIDIA 仓库包含大量技能、评测样例和可执行脚本。本轮只发布其官方 `nvidia-skill-finder` 子树；它用于查找合适的 NVIDIA Skill，不把整个大型仓库批量搬进市场。

## 暂缓或拒绝

| 来源/包 | 处理 | 原因 |
|---|---|---|
| AWS `aws-serverless` | 暂缓 | 包含 shell 脚本和 hooks；需逐文件人工复核后才能考虑 |
| AWS `aws-transform` | 暂缓 | Skill 子树包含 Python 工具脚本 |
| AWS `databases-on-aws` | 暂缓 | 包含集群创建、删除和连接脚本，具有明显外部写入能力 |
| AWS `deploy-on-aws` | 暂缓 | 包含 shell/Python 校验脚本和部署相关工作流 |
| AWS `sagemaker-ai` | 暂缓 | 包含多组集群诊断和 SSM shell 脚本 |
| `appwrite/codex-plugin` | 阻断 | `appwrite-cli/SKILL.md` 命中 pipe-to-shell；即使仓库有 BSD-3-Clause，也不能通过当前安全门禁 |
| `obra/superpowers` | 暂缓 | 完整插件包含 hooks、shell/JS 脚本；不能按当前无可执行文件门禁整包发布 |
| Temporal / Supabase / Zoom | 候选 | 百灵鸟副本不能替代原始仓库复核；须从各自官方仓库固定提交重新生成候选 |
| Echobird 其余条目 | 不自动导入 | 根仓库许可证不足以证明 180 个包的再分发许可，且多项依赖远程 App 身份或未固定来源 |

## 权限结论

这些 Skill 会指导 Codex 读写项目、运行开发命令或访问云服务，因此不能标记为低风险。Azure、AWS、Appwrite 和 NVIDIA 条目按实际能力声明 `filesystem-read`、`filesystem-write`、`shell`、`network`；涉及云账号的条目再声明 `credentials` 与 `external-write`，安装前必须显示增强权限确认。插件包本身不包含 token、Cookie、私钥或安装脚本。

## 可复跑方式

维护者先克隆官方仓库，再从已提交 Git 对象生成候选和包：

```powershell
python -m scripts.package_official_plugins `
  --local-source aws-agent-plugins-official=.cache/aws-agent-plugins `
  --local-source microsoft-agent-skills-official=.cache/microsoft-agent-skills `
  --local-source nvidia-skills-official=.cache/nvidia-skills
```

生成器核对 origin、40 位提交、Git 文件模式、文件大小、敏感文件名与高风险静态模式。来源变化会直接失败，不会自动换到新提交或把候选改成 approved。

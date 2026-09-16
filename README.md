# 暴喵 Codex 插件市场

面向中国大陆 Windows 用户的中文 Codex 插件市场。每个插件包封装一个可被 Codex 加载的 Skill，并明确展示发布者、原始来源、固定版本、许可证和所需权限。

暴喵客户端可以利用自身网络加速能力访问 GitHub 官方/原始来源，但不得改写来源、代理第三方身份或上传用户凭证。当前仓库是可发布的 MVP；它不是失效市场的镜像，也没有复制参考仓库中无明确许可的内容。

## 当前内容

- 中文静态首页：搜索、分类、官方/社区、风险筛选和来源详情；
- 严格的 [Skill 元数据 Schema](schema/skill.schema.json)；公开构建会在同一条目上附加 schema 已定义的 `integrity` 文件摘要；
- `catalog/candidates/` 与 `catalog/approved/` 双区隔离；
- 允许来源、固定提交、完整目录枚举和保守型安全扫描；
- 人工审核后才构建的 `dist/catalog.json` + SHA-256；
- GitHub 仓库直连：网页复制 `owner/repo@固定提交`，用户在 Codex 的“添加插件市场”中粘贴后即可按需安装；
- [暴喵客户端接入契约](docs/client-contract.md)：保留为后续客户端增强能力，不是当前网页使用的前置条件；
- 经过独立 Schema 与 SHA-256 校验的 Codex 官方动态目录描述：只让本机 Codex 查询当前可用插件，不复制官方包；
- GitHub Actions CI 与 Pages 发布流程；
- 78 个真实、可核验、可由 Codex Marketplace 发现的插件：20 个 OpenAI / Anthropic、52 个 Harness、5 个 AWS / Microsoft / NVIDIA 官方插件，以及 1 个中文学术研究工具箱；
- 插件内部合计 288 个 Skills，其中 Azure 官方合集包含 202 个、中文学术工具箱包含 10 个，均不拆卡片虚增插件数；
- 所有插件包都保留上游许可证，下发逐文件 SHA-256、文件数、总字节数和许可证摘要；另保留完整暂缓与拒绝记录。

## 插件形态

78 个条目全部进入 `.agents/plugins/marketplace.json`。仓库中的每个 `plugins/<id>/` 都有 `.codex-plugin/plugin.json`；单 Skill 插件保存在 `skills/<id>/`，合集插件则在同一 `skills/` 下保留多个上游 Skill 目录。插件清单与候选摘要逐字节核对；“插件”是安装与发现单元，“Skill”是插件内承载的能力。

## 两种来源，不混在一起计数

- **暴喵精选市场：** 本仓库中的 78 个固定版本插件。用户复制仓库市场地址，在 Codex 中粘贴后再逐个启用。
- **Codex 官方插件目录：** 由用户本机 Codex 根据版本、产品和账号动态提供。网页提供中文用途说明和只读查看命令 `codex plugin list --available --json`，不镜像插件、不代替登录，也不把数量加到暴喵的 78 个里。

## 中文论文科研入口

- 暴喵精选新增 **中文学术研究工具箱**：一个插件包含论文精读、文献综合、科研写作、研究设计、同行评审、科研图表与学术汇报等 10 个 Skills；插件名称、摘要、标签、风险说明和默认提示全部使用简体中文。
- Codex 官方动态目录展示 SciSpace、Consensus、Sider Scholar、Scite、Elicit 等论文数据源的中文用途说明。它们需要用户在 Codex 中自行连接，暴喵不复制包、不接触凭证。
- 首页搜索同时识别“论文、文献、综述、引文、科研、PDF”等中文关键词；研究数据源和方法工具继续分开标源。

许可、安全边界和暂缓来源见 [中文学术研究扩容复核](docs/reviews/chinese-academic-research-expansion-2026-09-16.md) 与 [决策 0012](docs/decisions/0012-chinese-academic-research-routing.md)。

OpenAI 的历史 `openai/plugins` 仓库已于 2026-08-16 归档，因此不作为持续同步或安装回退。详细结论见 [官方目录接入复核](docs/reviews/openai-official-directory-2026-08-17.md) 与 [决策 0011](docs/decisions/0011-codex-native-official-directory.md)。

## 最简单的使用方式：粘贴仓库地址

首页会分别校验 `catalog.json`、`marketplace-import.json` 及其 SHA-256，只有目录摘要、插件数量、同源地址、固定提交和 Codex 参数数组全部一致时，才启用“复制市场地址”。用户打开 Codex 的插件页，点击“添加”→“添加插件市场”，粘贴网页复制的 `owner/repo@固定提交` 即可。搜索同时覆盖插件名称与合集内部 Skill ID，例如 `azure functions` 会命中 `azure-functions`，无需把 202 个 Azure Skills 拆成 202 张插件卡片。

命令行只作为备用方式：

```powershell
codex plugin marketplace add https://github.com/<暴喵账号>/<仓库名> --ref <40位发布提交>
```

加入市场只注册目录，不安装全部插件、不登录第三方服务，也不授予插件后续操作权限。当前网页不唤起自定义协议，也不要求暴喵客户端；后续如接入客户端协议，它仍只能作为可选便利层，不能冒充 Codex 官方深链。

## 信任边界

“已审核”不是绝对安全保证。市场会拒绝无许可证、浮动版本、可执行文件、疑似凭证、危险命令或未人工审核的条目。需要 OAuth、外部写入、浏览器控制、系统配置或无沙箱运行的内容可以进入“增强权限”层，但客户端必须额外展示并逐项确认。每次安装仍必须重新扫描固定提交的完整目录，并在替换旧版本前备份。

参考仓库的详细结论见 [审查报告](docs/reviews/reference-repository.md)。市场关键取舍见 [决策记录](docs/decisions/)。

## Windows 本地运行

要求：Windows 10/11、Git、Python 3.9 或更高版本。PowerShell 中执行：

```powershell
git clone https://github.com/<暴喵账号>/<仓库名>.git
Set-Location <仓库名>
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .
python -m scripts.validate_catalog
python -m scripts.build --generated-at 2026-08-13T08:00:00Z
python -m http.server 8000 --directory site
```

浏览器打开 <http://localhost:8000>。不要直接双击 `site/index.html`，因为浏览器会阻止页面读取本地 JSON。

也可以直接把本仓库作为 Codex marketplace 添加，再安装已审核插件：

```powershell
codex plugin marketplace add <暴喵账号>/<仓库名> --ref main
codex plugin add pdf@baomiao-codex
codex plugin add define-goal@baomiao-codex
codex plugin add security-threat-model@baomiao-codex
codex plugin add aspnet-core@baomiao-codex
codex plugin add internal-comms@baomiao-codex
codex plugin add frontend-design@baomiao-codex
codex plugin add linear@baomiao-codex
codex plugin add notion-knowledge-capture@baomiao-codex
codex plugin add winui-app@baomiao-codex
```

这些插件包是对明确许可的固定上游目录的合规打包，包内保留许可证；每个 `plugin.json` 的 `homepage` 指向审核提交。上述方式适用于全部 78 个插件。

macOS/Linux 的命令相同，只需把虚拟环境激活改为：

```bash
source .venv/bin/activate
```

## 测试与验证

```powershell
python -m unittest discover -s tests -v
python -m scripts.validate_catalog
python -m scripts.validate_catalog --online
python -m scripts.build --generated-at 2026-08-13T08:00:00Z
```

正式发布构建必须额外写入最终 GitHub 仓库、Pages 地址和本次发布提交：

```powershell
python -m scripts.build `
  --generated-at 2026-08-14T08:00:00Z `
  --marketplace-source https://github.com/<暴喵账号>/<仓库名> `
  --marketplace-ref <40位发布提交> `
  --public-base-url https://<暴喵账号>.github.io/<仓库名>
```

`--online` 会读取每条记录中固定提交的 `SKILL.md` 与许可证，适合发布前运行；普通单元测试不依赖网络。

## 同步候选

允许来源只在 [sources.json](sources.json) 中配置。同步永远只写候选区：

```powershell
python -m scripts.sync_candidates --ref main
```

GitHub 公共 API 无 token 也可使用，但有速率限制。维护者如需提高额度，可以只在本机进程环境设置 `GITHUB_TOKEN`；程序不会把 token 写入文件、URL 或输出。不要把 token 提交到仓库。

同步器把 `main` 解析成完整提交哈希，再枚举允许目录的全部文件。候选文件名包含提交哈希前缀，因此新同步不会覆盖旧审核证据。候选中的 `scan.verdict` 仅表示自动扫描结果，不能把 `candidate` 状态自动改成 `approved`。完整审核步骤见 [CONTRIBUTING.md](CONTRIBUTING.md)。

来源较多时可用 `--source` 只同步一组，例如：

```powershell
python -m scripts.sync_candidates --source harness-official --ref main
```

GitHub API 限流时，可以先用 Git 克隆官方仓库，再让同步器直接读取固定提交的 Git 对象；它会核对 `origin`，不会读取未提交工作树：

```powershell
git clone --filter=blob:none https://github.com/openai/skills.git .cache/openai-skills
git clone --filter=blob:none https://github.com/anthropics/skills.git .cache/anthropic-skills
git clone --filter=blob:none https://github.com/harness/harness-skills.git .cache/harness-skills
python -m scripts.sync_candidates --ref main `
  --local-source openai-curated=.cache/openai-skills `
  --local-source anthropic-official=.cache/anthropic-skills `
  --local-source harness-official=.cache/harness-skills
```

本轮全网来源审查、7 个新增条目与暂缓原因见 [生态扩容审查](docs/reviews/ecosystem-expansion-2026-08-13.md)。
增强权限层的 10 个新增条目和逐项能力复核见 [增强权限扩容审查](docs/reviews/enhanced-permissions-2026-08-13.md)。
Harness 官方 55 个候选（发布 52 个、暂缓 3 个）的许可、目录和风险分组见 [Harness 专项复核](docs/reviews/harness-official-2026-08-13.md)。
AWS、Microsoft、NVIDIA 官方来源的固定版本、206 个新增 Skills 与拒绝项见 [官方插件扩容复核](docs/reviews/official-plugin-expansion-2026-08-14.md)。
百灵鸟默认市场 180 个插件与暴喵现状的逐项来源、形态、许可证和接入建议见 [百灵鸟市场对标表](docs/reviews/echobird-marketplace-crosswalk-2026-08-14.md)。该表可通过 `scripts.build_echobird_crosswalk` 从固定提交重新生成，只生成研究清单，不自动复制或发布插件。

## 生成物

- `dist/catalog.json`：客户端稳定接口；
- `dist/catalog.sha256`：目录原始字节的摘要；
- `site/catalog.json` 与 `site/catalog.sha256`：GitHub Pages 同源副本。
- `site/marketplace-import.json` 与 `site/marketplace-import.sha256`：暴喵客户端一键导入描述及摘要。
- `dist/federated-sources.json` 与 `dist/federated-sources.sha256`：Codex 原生官方目录接入描述及摘要；构建时复制到 `site/`。

固定 `--generated-at` 时构建结果可复现。发布流水线使用提交时间生成该字段，避免构建机器当前时间造成漂移。

## 发布到 GitHub

1. 在暴喵 AI 管家的 GitHub 组织或账号下新建**空的公开仓库**，不要预生成 README/LICENSE。
2. 启用 Settings → Pages → Source: **GitHub Actions**。
3. 本地执行：

```powershell
git init
git add .
git commit -m "feat: launch reviewed Codex skills marketplace MVP"
git branch -M main
git remote add origin https://github.com/<暴喵账号>/<仓库名>.git
git push -u origin main
```

4. `CI` 通过后，`Deploy Pages` 会构建并发布 `site/`。
5. 在暴喵客户端配置中写入最终 Pages 与 raw 地址；重新运行全部验证后再发布客户端入口。
6. 建议为 `main` 开启分支保护，要求 `CI / test-and-validate` 通过且至少 1 人审核。

## 许可证

本市场的代码与文档采用 [MIT](LICENSE)。各插件内的 Skill 仍归各自上游作者，采用条目 `license` 和 `source.license_url` 指向的许可证。`plugins/` 内只包含许可范围明确、固定版本且通过当前门禁的 78 个插件包。

# 暴喵 Codex Skills 市场

面向中国大陆 Windows 用户的中文 Codex Skill 索引。这里不追求“搬得多”，而是让每个条目都能回答：**谁发布、从哪里下载、固定到哪个版本、采用什么许可证、需要哪些权限、谁审核过。**

暴喵客户端可以利用自身网络加速能力访问 GitHub 官方/原始来源，但不得改写来源、代理第三方身份或上传用户凭证。当前仓库是可发布的 MVP；它不是失效市场的镜像，也没有复制参考仓库中无明确许可的内容。

## 当前内容

- 中文静态首页：搜索、分类、官方/社区、风险筛选和来源详情；
- 严格的 [Skill 元数据 Schema](schema/skill.schema.json)；
- `catalog/candidates/` 与 `catalog/approved/` 双区隔离；
- 允许来源、固定提交、完整目录枚举和保守型安全扫描；
- 人工审核后才构建的 `dist/catalog.json` + SHA-256；
- [暴喵客户端一键安装契约](docs/client-contract.md)；
- GitHub Actions CI 与 Pages 发布流程；
- 3 个少量但真实、可核验的 OpenAI 官方 Skill 条目。

## 信任边界

“已审核”不是绝对安全保证。MVP 会拒绝无许可证、浮动版本、可执行文件、疑似凭证、危险命令、高风险或未人工审核的条目。客户端每次安装仍必须重新扫描固定提交的完整目录，并在替换旧版本前备份。

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
```

这些插件包是对明确采用 Apache-2.0 的固定上游目录的合规打包，包内保留许可证；每个 `plugin.json` 的 `homepage` 指向审核提交。暴喵客户端自有的一键安装流程仍应按客户端契约直接读取原始上游，而不是把本市场包装冒充上游。

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

`--online` 会读取每条记录中固定提交的 `SKILL.md` 与许可证，适合发布前运行；普通单元测试不依赖网络。

## 同步候选

允许来源只在 [sources.json](sources.json) 中配置。同步永远只写候选区：

```powershell
python -m scripts.sync_candidates --ref main
```

GitHub 公共 API 无 token 也可使用，但有速率限制。维护者如需提高额度，可以只在本机进程环境设置 `GITHUB_TOKEN`；程序不会把 token 写入文件、URL 或输出。不要把 token 提交到仓库。

同步器把 `main` 解析成完整提交哈希，再枚举允许目录的全部文件。候选文件名包含提交哈希前缀，因此新同步不会覆盖旧审核证据。候选中的 `scan.verdict` 仅表示自动扫描结果，不能把 `candidate` 状态自动改成 `approved`。完整审核步骤见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 生成物

- `dist/catalog.json`：客户端稳定接口；
- `dist/catalog.sha256`：目录原始字节的摘要；
- `site/catalog.json` 与 `site/catalog.sha256`：GitHub Pages 同源副本。

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

本市场的代码与文档采用 [MIT](LICENSE)。各 Skill 仍归各自上游作者，采用条目 `license` 和 `source.license_url` 指向的许可证；本仓库 MVP 不复制其正文。

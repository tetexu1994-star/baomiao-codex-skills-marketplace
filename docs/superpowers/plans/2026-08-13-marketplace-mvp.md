# 暴喵 Codex Skills 市场 MVP Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 交付一个面向中国大陆 Windows 新手、可审核、可复跑、可静态发布的中文 Codex Skills 市场。

**Architecture:** 仓库将“候选同步”和“公开发布”分离：同步器只从允许清单读取固定 GitHub 来源并生成候选，构建器仅接受通过 schema、安全门禁和人工审核的条目。GitHub Pages 静态站消费同一份生成目录；暴喵客户端按公开契约从原始来源安装并保留回退副本。

**Tech Stack:** Python 3.11+ 标准库、JSON Schema 2020-12、原生 HTML/CSS/JavaScript、GitHub Actions。

---

### Task 1: 审查与边界

**Files:**
- Create: `docs/reviews/reference-repository.md`
- Create: `docs/decisions/0001-no-unlicensed-mirroring.md`

- [ ] 记录参考仓库的根许可证、README、目录和插件来源字段证据。
- [ ] 将无许可证内容、可执行脚本、高权限与未知来源设为阻断条件。
- [ ] 记录“只索引固定上游、不复制正文”的 MVP 决策。

### Task 2: 严格目录模型

**Files:**
- Create: `schema/skill.schema.json`
- Create: `catalog/approved/*.json`
- Create: `sources.json`
- Test: `tests/test_catalog.py`

- [ ] 定义关闭额外字段的元数据 schema，覆盖来源、许可证、风险、审核与安装字段。
- [ ] 为每条首发记录写入固定提交、原始目录、许可证证据、风险能力和人工审核结论。
- [ ] 写测试证明缺少审核、浮动 ref、未知权限和额外字段不能发布。

### Task 3: 候选同步和安全扫描

**Files:**
- Create: `scripts/sync_candidates.py`
- Create: `scripts/security.py`
- Create: `tests/test_security.py`

- [ ] 仅允许 HTTPS GitHub API/raw 主机，限制响应体大小并拒绝重定向到未知主机。
- [ ] 扫描可执行文件、秘密模式、危险命令和高风险权限；同步只写 `catalog/candidates/`。
- [ ] 用离线 fixture 测试安全规则，用 `--check` 验证允许源仍可访问且提交固定。

### Task 4: 构建与客户端契约

**Files:**
- Create: `scripts/validate_catalog.py`
- Create: `scripts/build.py`
- Create: `docs/client-contract.md`
- Create: `dist/catalog.json`
- Create: `dist/catalog.sha256`

- [ ] 构建前验证 schema、唯一 ID、许可证证据、固定提交、审核状态与风险门禁。
- [ ] 生成确定性的公开目录和 SHA-256 校验文件。
- [ ] 规定客户端预检、来源展示、原始来源加速、无凭证上传和原子回退流程。

### Task 5: 中文静态首页

**Files:**
- Create: `site/index.html`
- Create: `site/assets/app.js`
- Create: `site/assets/styles.css`

- [ ] 用真实目录渲染搜索、分类、官方/社区、风险和详情字段。
- [ ] 使用安全 DOM API，不使用 `innerHTML` 或第三方脚本。
- [ ] 支持键盘、减少动效偏好、空状态以及 320/768/1024/1440px。

### Task 6: 运行、测试和发布

**Files:**
- Create: `README.md`
- Create: `CONTRIBUTING.md`
- Create: `SECURITY.md`
- Create: `.github/workflows/ci.yml`
- Create: `.github/workflows/pages.yml`

- [ ] 写 Windows PowerShell 优先的本地启动、审核、构建、GitHub 发布步骤。
- [ ] 运行单元测试、目录验证、确定性构建和在线来源检查。
- [ ] 在无 GitHub 身份写权限时停在本地可发布状态，并列出上线所需账号信息。


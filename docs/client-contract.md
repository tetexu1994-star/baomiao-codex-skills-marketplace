# 暴喵客户端接入契约 v1

本契约描述客户端如何消费 `dist/catalog.json` 并安装市场中的 Codex 插件。它是暴喵市场自定义的前置校验契约，不冒充 Codex 官方插件协议；最终插件注册与加载行为应以用户当前 Codex 版本为准。

## 0. 一键导入整个市场

网站主按钮使用以下自定义协议把请求交给暴喵客户端：

```text
baomiao://codex/marketplace/import?manifest=<URL编码后的marketplace-import.json地址>&digest=<64位SHA-256>
```

这不是 Codex 或 OpenAI 官方深链。它只用于唤起暴喵；最终注册动作必须调用用户本机当前版本的 Codex CLI。客户端按以下顺序处理：

1. 只接受 `baomiao://codex/marketplace/import`，拒绝额外 action、fragment、用户名、密码与未知查询参数。
2. 正式版 `manifest` 只接受 HTTPS 且必须属于暴喵发布配置中的 Pages 域名；开发版可以显式允许 `http://127.0.0.1` 或 `http://localhost`，不得接受局域网 IP。
3. 下载原始字节，计算 SHA-256 并与 URL 中 `digest` 比对；再按 `schema/marketplace-import.schema.json` 校验。禁止跟随到非允许域名，限制响应大小为 64 KiB。
4. 只接受 `profile: release`、GitHub HTTPS `marketplace.source`、40 位 `marketplace.ref`、固定清单路径 `.agents/plugins/marketplace.json`。开发构建可以接受当前机器的 `local-preview`，但不得进入正式客户端。
5. 从 GitHub 固定提交读取市场清单，核对 `manifest_sha256`、市场名 `baomiao-codex` 和 `plugin_count`。同时校验目录及其摘要。
6. 确认页明确展示来源仓库、完整提交、市场名、插件数，以及“只添加市场，不自动安装插件”。用户点击确认前不得修改 Codex 配置。
7. 不经过 shell，不执行描述文件中的 `command.display`，而是客户端自行构造参数数组：`["plugin", "marketplace", "add", source, "--ref", ref]`，调用可信安装路径中的 `codex.exe`。
8. 添加前调用 `codex plugin marketplace list`。同名同来源已存在时返回 `already-added`；同名不同来源时阻断并让用户选择，不得静默覆盖。
9. 添加失败不改变原配置。用户要撤销时调用 `codex plugin marketplace remove baomiao-codex`；卸载市场不等于删除用户项目或第三方账号数据。

网页必须同时显示等价的 Codex 命令并提供复制按钮。自定义协议未注册、客户端未启动或校验失败时，用户仍能手动运行该命令；页面不得伪装成已经成功导入。

## 0.5 Codex 官方动态目录

`federated-sources.json` 描述的是另一个来源通道，不属于暴喵 Git marketplace，也不能合并进上述一键导入：

1. 客户端先校验 `federated-sources.sha256` 和 `schema/federated-source.schema.json`，只接受 `id: codex-official-directory`、`access.mode: codex-native`。
2. 不经过 shell，只能以参数数组 `["plugin", "list", "--available", "--json"]` 调用可信安装路径中的 `codex.exe`。网页中的 `command.display` 仅用于复制，不得直接执行。
3. 以 Codex 返回的 marketplace/source 身份为准；`openai-curated-remote`、`openai-api-curated` 只是已知官方标识，不允许描述文件把第三方来源改写成官方。
4. 插件数量、版本和可见范围以用户当前 Codex 版本、产品和账号为准。暴喵不得缓存为永久总数，也不得把官方条目计入 77 个暴喵精选插件。
5. 官方登录、OAuth、API key 和 Cookie 只在 Codex 或对应服务的官方界面处理。暴喵不读取 Codex 列表中的凭证字段、不代理登录、不上传列表结果。
6. `https://github.com/openai/plugins` 已于 2026-08-16 归档，只能显示为历史来源证据；原生目录失败时不得克隆该仓库、注册保留名称或用其 180 条历史快照回退。
7. 原生目录读取失败不影响暴喵精选市场。客户端应提示用户打开 Codex 的 Plugins 页面，并返回稳定错误码 `OFFICIAL_DIRECTORY_UNAVAILABLE`。

## 1. 获取目录

客户端通过暴喵的网络加速能力请求暴喵 GitHub 仓库的 raw/Pages 地址；加速层只做网络传输，不改写内容、来源字段或发布者身份。获取 `catalog.json` 后必须同时获取 `catalog.sha256`，按原始字节计算 SHA-256 并比对。解析器只接受 `schema_version: 1` 和 HTTPS URL。

加速失败时可以回退到同一个暴喵 GitHub 原始地址的直连请求。不得回退到匿名镜像、转存文件或伪造为上游作者的地址。

## 2. 安装前展示

确认界面至少展示：

- 插件名称、中文说明、分类与插件 ID；
- 发布者名称与“官方/社区”标记；
- 原始 GitHub 仓库、完整提交哈希和目录；
- SPDX 许可证、作用域与许可证原文链接；
- 插件所含 Skill 的真正上游身份，不得把封装者显示成原作者；
- 风险等级、能力清单、是否含可执行文件；
- 人工审核者、审核时间和证据；
- 目标安装目录与现有版本是否会被替换。

不得用“安全”“官方”等图标替代文字。市场的 `official` 表示“由来源仓库所属组织发布”，不是暴喵对其功能、服务或安全作担保。

## 3. 强制预检

按条目 `install.preflight` 顺序执行，任一步失败即停止：

1. `verify-catalog-digest`：验证市场目录摘要。
2. `verify-source-commit`：只下载 `source.commit` 指定的 40 位提交，禁止用 `main`/tag 替代。
3. `verify-license`：读取 `source.license_url`，核对 SPDX、作用域与 `integrity.license_evidence.sha256`。目录级许可证必须包含在下载文件清单内；仓库级许可证可以位于 `source.path` 外，但必须单独下载为随附许可说明。
4. `scan-files`：先枚举完整目录，再下载；限制单文件和总大小，拒绝符号链接、路径穿越、设备文件及未知重定向。重跑与市场同步器相同或更严格的秘密、高危命令和可执行文件扫描。
5. `show-source-and-risk`：把第 2 节信息显示给用户。
6. `confirm-user`：用户明确点击“安装此插件”。
7. `confirm-enhanced-permissions`：仅对 `risk.level: high` 执行；用独立确认页逐项列出 OAuth/凭证、外部写入、浏览器控制、本机命令、系统配置与无沙箱要求。不得与普通安装确认合并，也不得预选同意。
8. `backup-existing`：替换前创建本地原子备份。

扫描规则要随客户端版本更新；不能因为条目已由市场审核就跳过安装时扫描。

增强权限条目允许功能更强，但不代表自动获得权限。OAuth 必须由对应服务的官方登录页完成；系统配置、部署、推送、创建外部记录或关闭沙箱等动作仍应在实际使用时遵循 Codex 的逐次授权与用户指令。客户端不得代替用户保存第三方 token，也不得把“安装插件”解释成“授权所有后续操作”。

## 4. 下载与身份边界

- 客户端获取市场插件包时必须覆盖插件内完整 Skill 目录，不能只取 `SKILL.md` 而遗漏许可证、references 或 assets；也可以从展示的原始仓库固定提交回读同一目录进行复检。
- 按 `integrity.files` 校验相对路径、文件数、总字节数和每个文件的 SHA-256；上游目录多出、缺少或改变任何文件都以 `SOURCE_CHANGED` 阻断。
- 请求目标仅限 `github.com`、`api.github.com`、`raw.githubusercontent.com`，重定向后重新校验主机。
- 公共来源无需 token。私有来源不属于 v1 市场。
- 不把 GitHub token、Codex 凭证、Cookie、设备标识或安装目录上传给市场、暴喵加速层或上游。
- 不在 URL、日志、崩溃报告中记录凭证。若未来支持用户自带 token，只能保存在操作系统凭证库并直接发给对应 GitHub 主机。
- User-Agent 可声明暴喵客户端，但不得冒充 GitHub、OpenAI 或上游作者。

## 5. 原子安装与回退

下载到 `%LOCALAPPDATA%/Baomiao/plugin-staging/<随机ID>/`，验证所有相对路径仍在 staging 内。验证通过后：

1. 若目标不存在，把 staging 原子移动到 `install.destination`。
2. 若目标存在，先移动到 `%LOCALAPPDATA%/Baomiao/plugin-backups/<plugin-id>/<timestamp>/`，再移动新目录。
3. 新目录移动失败时立即恢复备份。
4. 安装成功后记录本地 `id`、来源仓库、提交、文件摘要与备份路径；记录不得包含凭证。

“回退”只恢复上一次本地备份，不去下载另一个来源。卸载仅删除当前插件；备份保留期限由客户端策略明确展示。

## 6. 最小接口

```ts
type MarketplaceImportRequestV1 = {
  manifestUrl: string;
  expectedManifestDigest: string;
};

type MarketplaceImportResultV1 = {
  status: "added" | "already-added" | "cancelled" | "blocked" | "failed";
  marketplaceName?: "baomiao-codex";
  installedRef?: string;
  reasonCode?: string;
};

type InstallRequestV1 = {
  catalogUrl: string;
  catalogSha256Url: string;
  skillId: string;
  expectedCommit: string;
  expectedCatalogDigest: string;
};

type InstallResultV1 = {
  status: "installed" | "cancelled" | "blocked" | "rolled-back";
  installedCommit?: string;
  destination?: string;
  backupId?: string;
  reasonCode?: string;
};
```

客户端不得接受请求体覆盖条目中的来源、许可证、风险或目标目录。`reasonCode` 使用稳定枚举并提供中文解释，例如 `CATALOG_DIGEST_MISMATCH`、`SOURCE_CHANGED`、`EXECUTABLE_FOUND`、`USER_CANCELLED`、`ROLLBACK_COMPLETED`。

对增强权限条目，客户端还应记录用户确认的能力枚举与确认时间，但不得记录 token、OAuth code、Cookie 或外部服务内容。若客户端版本不认识某个能力枚举，必须以 `UNSUPPORTED_CAPABILITY` 阻断，不能忽略未知能力。

市场导入稳定错误码至少包括 `IMPORT_DIGEST_MISMATCH`、`IMPORT_SOURCE_NOT_ALLOWED`、`IMPORT_SCHEMA_UNSUPPORTED`、`MARKETPLACE_MANIFEST_MISMATCH`、`MARKETPLACE_NAME_CONFLICT`、`CODEX_NOT_FOUND`、`USER_CANCELLED`。日志可以记录来源域名、提交和错误码，不得记录 URL 凭证、用户目录、Codex 配置全文或第三方 token。

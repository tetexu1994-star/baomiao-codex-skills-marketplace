# 暴喵客户端接入契约 v1

本契约描述客户端如何消费 `dist/catalog.json`。它是暴喵市场自定义契约，不冒充 Codex 官方插件协议。Codex Skill 的最终安装位置与加载行为应以用户当前 Codex 版本为准。

## 1. 获取目录

客户端通过暴喵的网络加速能力请求暴喵 GitHub 仓库的 raw/Pages 地址；加速层只做网络传输，不改写内容、来源字段或发布者身份。获取 `catalog.json` 后必须同时获取 `catalog.sha256`，按原始字节计算 SHA-256 并比对。解析器只接受 `schema_version: 1` 和 HTTPS URL。

加速失败时可以回退到同一个暴喵 GitHub 原始地址的直连请求。不得回退到匿名镜像、转存文件或伪造为上游作者的地址。

## 2. 安装前展示

确认界面至少展示：

- Skill 名称、中文说明、分类；
- 发布者名称与“官方/社区”标记；
- 原始 GitHub 仓库、完整提交哈希和目录；
- SPDX 许可证与许可证原文链接；
- 风险等级、能力清单、是否含可执行文件；
- 人工审核者、审核时间和证据；
- 目标安装目录与现有版本是否会被替换。

不得用“安全”“官方”等图标替代文字。市场的 `official` 表示“由来源仓库所属组织发布”，不是暴喵对其功能、服务或安全作担保。

## 3. 强制预检

按条目 `install.preflight` 顺序执行，任一步失败即停止：

1. `verify-catalog-digest`：验证市场目录摘要。
2. `verify-source-commit`：只下载 `source.commit` 指定的 40 位提交，禁止用 `main`/tag 替代。
3. `verify-license`：目标目录内许可证须存在，并与声明 SPDX 相符。
4. `scan-files`：先枚举完整目录，再下载；限制单文件和总大小，拒绝符号链接、路径穿越、设备文件及未知重定向。重跑与市场同步器相同或更严格的秘密、高危命令和可执行文件扫描。
5. `show-source-and-risk`：把第 2 节信息显示给用户。
6. `confirm-user`：用户明确点击“从原始来源安装”。
7. `backup-existing`：替换前创建本地原子备份。

扫描规则要随客户端版本更新；不能因为条目已由市场审核就跳过安装时扫描。

## 4. 下载与身份边界

- 客户端下载 `source.path` 整个目录，不能只下载 `SKILL.md` 而遗漏许可证、references 或 assets。
- 请求目标仅限 `github.com`、`api.github.com`、`raw.githubusercontent.com`，重定向后重新校验主机。
- 公共来源无需 token。私有来源不属于 v1 市场。
- 不把 GitHub token、Codex 凭证、Cookie、设备标识或安装目录上传给市场、暴喵加速层或上游。
- 不在 URL、日志、崩溃报告中记录凭证。若未来支持用户自带 token，只能保存在操作系统凭证库并直接发给对应 GitHub 主机。
- User-Agent 可声明暴喵客户端，但不得冒充 GitHub、OpenAI 或上游作者。

## 5. 原子安装与回退

下载到 `%LOCALAPPDATA%/Baomiao/skill-staging/<随机ID>/`，验证所有相对路径仍在 staging 内。验证通过后：

1. 若目标不存在，把 staging 原子移动到 `install.destination`。
2. 若目标存在，先移动到 `%LOCALAPPDATA%/Baomiao/skill-backups/<skill-id>/<timestamp>/`，再移动新目录。
3. 新目录移动失败时立即恢复备份。
4. 安装成功后记录本地 `id`、来源仓库、提交、文件摘要与备份路径；记录不得包含凭证。

“回退”只恢复上一次本地备份，不去下载另一个来源。卸载仅删除当前 Skill；备份保留期限由客户端策略明确展示。

## 6. 最小接口

```ts
type InstallRequestV1 = {
  catalogUrl: string;
  catalogSha256Url: string;
  skillId: string;
  expectedCommit: string;
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


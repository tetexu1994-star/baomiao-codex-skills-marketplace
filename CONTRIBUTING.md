# 贡献与人工审核

## 可以提交什么

优先考虑中文用户常见的文档、研发、规划、安全和数据任务。来源必须与 Codex Skill 兼容，具有明确的上游仓库与许可证。规模扩张不能绕过审核门禁。

以下内容直接拒绝：

- 没有明确许可证，或许可证作用域不覆盖 Skill；
- 通过复制仓库、网盘、匿名镜像隐藏真实来源；
- 安装脚本、二进制、混淆/编码命令、pipe-to-shell；
- 读取浏览器 Cookie、SSH key、钱包、密码库或系统凭证；
- 上传环境变量、token、工作区内容或设备信息到未声明服务；
- 要求管理员权限、关闭安全软件、绕过平台政策；
- 无法完整枚举的仓库树，或无法向用户解释具体影响的高权限行为。

## 审核流程

1. 只在 `sources.json` 添加经维护者同意的 HTTPS GitHub 来源与精确允许目录。
2. 运行 `python -m scripts.sync_candidates --ref <ref>`。确认只改动 `catalog/candidates/`。GitHub API 限流时可用 `--local-source SOURCE_ID=PATH`；同步器会核对 Git origin 并从固定提交读取 blob。
3. 审核候选记录的完整文件清单和摘要；不要只读 `SKILL.md`。
4. 打开固定提交下的许可证原文，确认 SPDX 和作用域。
5. 阅读 Skill、references、assets、agent 配置；按实际行为填写能力，不能因发布者知名而降级。
   `high` 条目必须包含 `confirm-enhanced-permissions`，并在风险说明中写清外部服务、系统改动、浏览器/沙箱或远端写入影响。
6. 在 `docs/reviews/` 写证据，包含提交、文件、摘要、权限与拒绝项。
7. 手工创建 `catalog/approved/<id>.json`，状态设为 `approved`，署真实可追责的审核者名称。大批同源、同许可、同目录形态的条目可以由审核表生成，但审核表本身必须逐项记录中文用途和权限判断。
8. 选择交付方式：需要进入 Codex marketplace 的条目使用 `copy-source-directory` 并提交逐字节一致的插件包；不复制正文的条目使用 `source-direct`，且仍须保留候选摘要供客户端校验。
9. 运行测试、离线验证、在线验证和构建；检查 diff 中没有 token 或非预期上游正文。
10. Pull Request 至少由另一位维护者复核。同步机器人不能批准自己的候选。

## 变更规则

上游更新必须生成新候选并重新完整审核；禁止只替换 `commit`。撤下问题条目时，从 approved 删除并发布新目录，不静默改源。风险分级变更要在审核证据中说明原因。

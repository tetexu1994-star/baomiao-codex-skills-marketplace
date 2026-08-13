# 安全最佳实践审查

## 摘要

本次审查覆盖 Python 同步/验证/构建工具、原生 JavaScript 静态站、Codex marketplace 包与 GitHub Actions。未发现 Critical/High 漏洞；发布门禁已经采用固定提交、主机允许清单、大小限制、完整文件摘要、许可证证据、人工审核、无凭证持久化和固定 Action 提交。

## 已落实控制

- `scripts/net.py`：仅允许 HTTPS GitHub API/raw 主机，重定向后重新校验，限制响应大小，URL 禁止内嵌凭证。
- `scripts/security.py`：阻断脚本/可执行后缀、敏感文件名、pipe-to-shell、编码 PowerShell、危险删除、凭证外传与 Shell 执行模式。
- `scripts/sync_candidates.py`：把浮动 ref 解析成提交，完整枚举 tree，拒绝截断，结果只写候选区且按提交留档。
- `scripts/validate_catalog.py`：公开条目必须人工 approved、风险不高于 medium、无可执行文件、证据存在；插件包逐文件 SHA-256 必须与候选一致。
- `site/assets/app.js`：只用 `textContent`/DOM API 渲染，不使用 `innerHTML`、`eval`、远程脚本或本地存储；外链强制 HTTPS 和 `noopener noreferrer`。
- `.github/workflows/`：最小权限，第三方 Action 固定到完整提交。

## Low / 运维注意事项

### SEC-001：GitHub Pages 响应头需上线后复核

- 严重度：Low
- 位置：`site/index.html`、`site/contract.html`
- 证据：静态页以 `<meta http-equiv="Content-Security-Policy">` 提供 CSP。
- 影响：meta CSP 不支持 `frame-ancestors` 等部分响应头能力。
- 处理：当前 CSP 已阻止非同源脚本、对象和表单；上线后使用浏览器网络面板确认 GitHub Pages 实际响应头。若未来使用自定义域/CDN，在边缘设置 `Content-Security-Policy`（含 `frame-ancestors 'none'`）、`X-Content-Type-Options: nosniff` 与合适的 `Referrer-Policy`。

### SEC-002：目录摘要当前不提供发布者签名

- 严重度：Low
- 位置：`dist/catalog.sha256`、`docs/client-contract.md`
- 证据：客户端通过同源 SHA-256 检测传输/落盘损坏，但摘要与目录由同一发布通道提供。
- 影响：若 GitHub 仓库写权限本身被攻破，攻击者可以同时替换目录和摘要。
- 处理：MVP 已由固定上游提交、分支保护建议和 CI 降低风险。正式客户端达到稳定规模后，可增加离线签名的 release manifest，并把公钥固定在客户端；不要把签名私钥放入前端或仓库。


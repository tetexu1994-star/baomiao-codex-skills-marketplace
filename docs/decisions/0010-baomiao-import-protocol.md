# 0010：一键导入是 Codex CLI 的可审计封装

- 状态：采纳
- 日期：2026-08-14

## 决定

首页通过 `baomiao://codex/marketplace/import` 唤起暴喵客户端。协议只携带导入描述文件 URL 与摘要，不携带 token、用户路径或任意命令。客户端验证来源与固定提交、展示确认页，然后不经 shell 调用 `codex plugin marketplace add <GitHub URL> --ref <commit>`。

## 理由

当前 Codex CLI 明确提供 marketplace `add/list/upgrade/remove`，但公开 OpenAI 文档未定义可供第三方网站直接使用的 marketplace 深链。自定义暴喵协议可以给 Windows 新手提供一键入口，同时保留 Codex 作为实际注册者，不伪造官方身份。

## 回退

页面永久显示等价 Codex 命令。暴喵协议不可用时，用户复制命令即可；客户端添加失败时不改原配置。撤销使用 `codex plugin marketplace remove baomiao-codex`。

## 上线条件

正式导入描述必须由发布流水线写入最终 GitHub 仓库 URL、Pages URL 与 40 位发布提交。在暴喵客户端完成协议注册和参数数组调用前，网页按钮只能视为前端与契约已就绪，不能宣称客户端功能已经发布。

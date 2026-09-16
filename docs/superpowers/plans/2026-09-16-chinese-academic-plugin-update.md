# 中文学术插件更新 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为暴喵市场补充中文展示的学术研究插件包，并把当前可用的论文数据源以中文方式呈现在官方目录入口。

**Architecture:** 暴喵精选新增一个固定提交、MIT 许可、纯 Markdown 的社区插件包；官方论文数据源继续走 Codex 原生目录，不复制包、不接触凭证。静态站沿用摘要校验的 JSON 接口，增加研究入口、中文说明和搜索别名。

**Tech Stack:** Python 3.9、JSON Schema、原生 HTML/CSS/JavaScript、Codex plugin manifest、GitHub Pages。

---

### Task 1: 固定并审核学术研究来源

**Files:** `sources.json`、`docs/reviews/chinese-academic-research-expansion-2026-09-16.md`、`docs/decisions/0012-chinese-academic-research-routing.md`、候选摘要。

- [x] 将上游以仓库级 MIT、`skills` bundle、candidate-only 方式加入允许来源。
- [x] 从固定提交生成候选摘要，确认无脚本、凭证或阻断项。
- [x] 记录 10 个 Skills、许可范围和暂缓脚本型来源的原因。

### Task 2: 生成可安装的中文学术研究插件

**Files:** `plugins/academic-research-toolkit/**`、`catalog/approved/academic-research-toolkit.json`、`.agents/plugins/marketplace.json`、`THIRD_PARTY_NOTICES.md`。

- [x] 用 repo marketplace scaffold 创建插件。
- [x] 按候选摘要复制固定提交中的 10 个 Skills 与许可证。
- [x] 写入中文插件名、摘要、标签、默认提示、来源和权限。
- [x] 验证 manifest、候选摘要和安装包逐文件一致。

### Task 3: 更新中文官方研究入口和首页体验

**Files:** `schema/federated-source.schema.json`、`catalog/federated/codex-official.json`、`site/index.html`、`site/assets/app.js`、`site/assets/styles.css`。

- [x] 为官方示例增加中文摘要、搜索词和账号连接标记。
- [x] 增加“论文科研”快捷入口，让搜索覆盖官方研究插件和暴喵精选。
- [x] 展示当前可用研究来源，不镜像、不保证所有账号可用。
- [x] 保持键盘操作、移动端单列、错误态和摘要校验。

### Task 4: 消除硬编码数量并补齐测试文档

**Files:** `tests/test_catalog.py`、`README.md`、`outputs/DELIVERY.md` 及公开构建物。

- [x] 将测试中的固定数量改为从批准条目与实际 Skills 计算。
- [x] 更新 README 和交付说明。
- [x] 运行单元测试、目录校验、插件校验和可复现构建。
- [x] 启动站点完成桌面与移动端浏览器验收。

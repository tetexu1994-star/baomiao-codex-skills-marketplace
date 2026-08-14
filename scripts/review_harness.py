"""Materialize the human-reviewed Harness plugin catalog entries.

This is deliberately separate from candidate sync: the sync command never publishes.
Running this file reproduces only the review decisions recorded in REVIEW_METADATA.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMIT = "e75f841df3482c00d90144cca37d9b2a3b6ff0fb"
REPOSITORY = "https://github.com/harness/harness-skills"

# id: Chinese title, category, concise reviewed purpose, mutates external systems
REVIEW_METADATA = {
    "ai-operations": ("AI 运维分析", "研发工具", "分析 Harness AI 运维数据、异常和服务状态，辅助排障与运维决策。", False),
    "analyze-costs": ("云成本分析", "数据分析", "查询 Harness CCM 云成本、异常和节省机会，生成成本优化建议。", False),
    "approve-exempt": ("漏洞豁免审批", "安全治理", "复核并审批 Harness 漏洞豁免申请，记录安全治理决策。", True),
    "audit-report": ("审计报告", "安全治理", "查询 Harness 审计轨迹，整理用户操作、资源变化和合规证据。", False),
    "chaos-experiment": ("混沌实验", "安全治理", "配置并运行 Harness 混沌实验，验证服务在故障条件下的韧性。", True),
    "configure-agent-pr-attestation": ("PR 证明配置", "安全治理", "为代码仓库配置 Harness 代理式 PR 证明和供应链校验。", True),
    "configure-container-scan": ("容器扫描配置", "安全治理", "在 Harness 流水线中配置容器镜像安全扫描步骤。", True),
    "configure-dast-scan": ("DAST 扫描配置", "安全治理", "在 Harness 流水线中配置动态应用安全测试步骤。", True),
    "configure-repo-scan": ("仓库扫描配置", "安全治理", "在 Harness 流水线中配置代码仓库安全扫描步骤。", True),
    "configure-secret-scan": ("密钥扫描配置", "安全治理", "在 Harness 流水线中配置敏感信息和密钥扫描步骤。", True),
    "create-agent": ("创建 Harness Agent", "研发工具", "创建并配置 Harness Agent 资源，用于自动化研发与交付任务。", True),
    "create-agent-template": ("创建 Agent 模板", "研发工具", "生成并创建可复用的 Harness Agent 模板和参数定义。", True),
    "create-connector": ("创建连接器", "研发工具", "创建 Harness 云、代码仓库或制品库连接器并配置认证。", True),
    "create-environment": ("创建部署环境", "研发工具", "生成并创建 Harness 开发、预发或生产环境定义。", True),
    "create-infrastructure": ("创建基础设施定义", "研发工具", "创建 Harness Kubernetes、ECS 或云部署目标定义。", True),
    "create-pipeline": ("创建 CI/CD 流水线", "研发工具", "生成 Harness v0 CI/CD 流水线并按确认结果写入平台。", True),
    "create-pipeline-v1": ("创建 V1 流水线", "研发工具", "生成结构更简洁的 Harness v1 流水线并写入平台。", True),
    "create-policy": ("创建治理策略", "安全治理", "创建 Harness 治理策略和规则，用于约束交付与安全流程。", True),
    "create-sbom": ("生成 SBOM", "安全治理", "向现有流水线添加 SBOM 生成步骤，支持 SPDX 与 CycloneDX。", True),
    "create-secret": ("创建 Harness 密钥", "安全治理", "在 Harness 密钥管理中创建受保护的文本或文件密钥。", True),
    "create-template": ("创建 Harness 模板", "研发工具", "生成并创建可复用的流水线、步骤组或服务模板。", True),
    "create-trigger": ("创建流水线触发器", "研发工具", "为 Harness 流水线创建 Webhook、定时或制品触发器。", True),
    "dbops-changeset": ("数据库变更集", "研发工具", "创建并管理 Harness DB DevOps 数据库变更集和执行流程。", True),
    "debug-pipeline": ("流水线故障诊断", "研发工具", "读取 Harness 执行日志与阶段耗时，定位失败原因和性能瓶颈。", False),
    "deployment-readiness": ("部署就绪评估", "研发工具", "比较环境差异并给出发布前检查和金丝雀推进建议。", False),
    "dora-metrics": ("DORA 指标报告", "数据分析", "查询部署频率、变更前置时间、失败率和恢复时间等 DORA 指标。", False),
    "exempt-vuln": ("申请漏洞豁免", "安全治理", "为指定漏洞提交带理由和期限的 Harness 豁免申请。", True),
    "generate-slsa": ("生成 SLSA 证明", "安全治理", "在流水线中生成 SLSA 构建来源证明并关联制品。", True),
    "gitops-status": ("GitOps 状态", "研发工具", "查询 Harness GitOps 与 Argo CD 应用健康、同步和部署状态。", False),
    "incident-response": ("事故响应分析", "安全治理", "关联近期部署、评估影响范围并生成事故复盘素材。", False),
    "manage-artifacts": ("制品管理", "研发工具", "查询、整理或修改 Harness 制品库中的制品与版本。", True),
    "manage-cde": ("云开发环境管理", "研发工具", "创建、更新或管理 Harness 云开发环境和工作区。", True),
    "manage-delegates": ("Delegate 管理", "研发工具", "查询和管理 Harness Delegate 运行状态与配置。", True),
    "manage-feature-flags": ("功能开关管理", "研发工具", "创建、启停、归档或删除 Harness Feature Flags。", True),
    "manage-freeze-windows": ("发布冻结窗口", "效率规划", "创建和维护 Harness 发布冻结窗口，控制敏感时段部署。", True),
    "manage-iacm": ("IaCM 工作区管理", "研发工具", "管理 Harness 基础设施即代码工作区、计划和执行。", True),
    "manage-idp": ("开发者门户管理", "研发工具", "管理 Harness IDP 目录、工作流和开发者自助服务。", True),
    "manage-pull-requests": ("Pull Request 管理", "研发工具", "创建、评审、合并 Harness Code PR，并管理评论和检查。", True),
    "manage-roles": ("角色权限管理", "安全治理", "创建和维护 Harness 角色、资源组与访问控制绑定。", True),
    "manage-slos": ("SLO 与值班辅助", "安全治理", "查询部署和执行历史，生成值班交接、运行手册与 SLO 分析。", False),
    "manage-supply-chain": ("软件供应链管理", "安全治理", "管理 Harness 软件供应链安全、制品证明和合规流程。", True),
    "manage-users": ("用户管理", "安全治理", "邀请、更新或移除 Harness 用户并管理账号访问。", True),
    "migrate-pipeline": ("流水线迁移", "研发工具", "分析旧流水线并迁移为 Harness 支持的流水线定义。", True),
    "optimize-pipeline": ("流水线性能优化", "研发工具", "分析阶段耗时、缓存和测试并行度，提出 CI/CD 优化建议。", False),
    "pr-analysis": ("PR 影响分析", "研发工具", "分析代码变更影响的流水线、服务、环境与安全风险。", False),
    "run-pipeline": ("运行流水线", "研发工具", "触发、监控、审批、重试或终止 Harness 流水线执行。", True),
    "scorecard-review": ("工程评分卡评审", "数据分析", "查询 Harness 工程评分卡，分析团队或服务的质量与成熟度。", False),
    "security-report": ("安全合规报告", "安全治理", "汇总 Harness 漏洞、SBOM、扫描和豁免数据形成安全报告。", False),
    "sei-analytics": ("研发效能分析", "数据分析", "分析迭代速度、估算准确率、投入分布和发布就绪度。", False),
    "sign-artifact": ("制品签名", "安全治理", "在 Harness 流水线中为制品生成签名并记录证明。", True),
    "template-usage": ("模板使用分析", "数据分析", "查询 Harness 模板引用与使用情况，辅助模板治理和升级。", False),
    "verify-sign": ("验证制品签名", "安全治理", "在 Harness 流水线中验证制品签名和来源证明。", True),
}


def make_entry(skill_id: str, data: tuple[str, str, str, bool]) -> dict:
    title, category, summary, external_write = data
    source_path = f"skills/{skill_id}"
    capabilities = ["network", "credentials"]
    if external_write:
        capabilities.append("external-write")
    preflight = [
        "verify-catalog-digest", "verify-source-commit", "verify-license", "scan-files",
        "show-source-and-risk", "confirm-user", "backup-existing",
    ]
    if external_write:
        preflight.insert(-1, "confirm-enhanced-permissions")
    return {
        "schema_version": 1,
        "id": skill_id,
        "name": title,
        "summary_zh": summary,
        "category": category,
        "tags": ["Harness", "MCP", "DevOps", "官方插件"],
        "publisher": {"name": "Harness", "kind": "official", "url": "https://github.com/harness"},
        "source": {
            "repository": REPOSITORY,
            "commit": COMMIT,
            "path": source_path,
            "skill_url": f"https://raw.githubusercontent.com/harness/harness-skills/{COMMIT}/{source_path}/SKILL.md",
            "license_url": f"https://raw.githubusercontent.com/harness/harness-skills/{COMMIT}/LICENSE",
            "license_path": "LICENSE",
        },
        "license": {"spdx": "Apache-2.0", "scope": "repository", "verified_at": "2026-08-13"},
        "risk": {
            "level": "high" if external_write else "medium",
            "capabilities": capabilities,
            "has_executable_files": False,
            "notes_zh": "需要连接 Harness MCP v2 并使用用户自己的 Harness 授权；" + ("可修改远端资源，执行前必须逐项确认。" if external_write else "默认用于读取、分析和生成建议。"),
        },
        "review": {
            "status": "approved",
            "reviewer": "暴喵市场维护者（Harness 专项复核）",
            "reviewed_at": "2026-08-13T13:10:00Z",
            "evidence": "docs/reviews/harness-official-2026-08-13.md",
        },
        "install": {
            "mode": "copy-source-directory",
            "destination": f"%USERPROFILE%/.codex/skills/{skill_id}",
            "requires_auth": True,
            "preflight": preflight,
        },
    }


def main() -> None:
    approved = ROOT / "catalog" / "approved"
    approved.mkdir(parents=True, exist_ok=True)
    for target in approved.glob("*.json"):
        existing = json.loads(target.read_text(encoding="utf-8"))
        if existing.get("source", {}).get("repository") == REPOSITORY and existing.get("id") not in REVIEW_METADATA:
            target.unlink()
    for skill_id, data in sorted(REVIEW_METADATA.items()):
        target = approved / f"{skill_id}.json"
        target.write_text(json.dumps(make_entry(skill_id, data), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"已从人工复核表生成 {len(REVIEW_METADATA)} 个 Harness 插件条目")


if __name__ == "__main__":
    main()

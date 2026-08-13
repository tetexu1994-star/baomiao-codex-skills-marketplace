"""Conservative static checks for remotely sourced Skill directories."""

from __future__ import annotations

import hashlib
import re
from dataclasses import asdict, dataclass
from pathlib import PurePosixPath
from typing import Iterable

EXECUTABLE_SUFFIXES = {
    ".bat", ".cmd", ".com", ".dll", ".exe", ".jar", ".js", ".mjs",
    ".msi", ".ps1", ".py", ".sh", ".so", ".swift", ".ts", ".vbs",
}
SENSITIVE_NAMES = {".env", ".npmrc", ".pypirc", "credentials", "id_rsa", "id_ed25519"}
TEXT_SUFFIXES = {"", ".md", ".txt", ".json", ".yaml", ".yml", ".toml"}
BLOCKED_PATTERNS = {
    "pipe-to-shell": re.compile(r"(?:curl|wget)[^\n|]{0,300}\|\s*(?:ba)?sh\b", re.I),
    "destructive-delete": re.compile(r"\brm\s+-[a-z]*r[a-z]*f\s+(?:/|~|\$HOME)\b", re.I),
    "powershell-eval": re.compile(r"\b(?:Invoke-Expression|IEX)\b", re.I),
    "encoded-command": re.compile(r"\b(?:powershell|pwsh)\b[^\n]{0,160}\s-(?:enc|encodedcommand)\b", re.I),
    "credential-exfiltration": re.compile(r"(?:curl|wget|requests\.(?:post|put))[^\n]{0,500}(?:GITHUB_TOKEN|GH_TOKEN|OPENAI_API_KEY|AWS_SECRET_ACCESS_KEY)", re.I),
    "shell-execution": re.compile(r"(?:shell\s*=\s*True|\bos\.system\s*\(|\bsubprocess\.(?:run|Popen)\s*\()", re.I),
}


@dataclass(frozen=True)
class Finding:
    severity: str
    rule: str
    path: str
    detail: str


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def scan_files(files: Iterable[tuple[str, bytes]]) -> dict:
    """Return a serializable, deterministic scan report."""
    findings: list[Finding] = []
    total_bytes = 0
    file_count = 0
    for raw_path, content in sorted(files, key=lambda item: item[0]):
        path = PurePosixPath(raw_path)
        file_count += 1
        total_bytes += len(content)
        if path.name.lower() in SENSITIVE_NAMES:
            findings.append(Finding("blocked", "sensitive-file", raw_path, "疑似凭证或私密配置文件"))
        if path.suffix.lower() in EXECUTABLE_SUFFIXES:
            findings.append(Finding("blocked", "executable-file", raw_path, "包含可执行或脚本文件"))
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        text = content.decode("utf-8", errors="replace")
        for rule, pattern in BLOCKED_PATTERNS.items():
            if pattern.search(text):
                findings.append(Finding("blocked", rule, raw_path, "命中高风险静态模式，需人工拒绝或隔离分析"))
    findings.sort(key=lambda item: (item.severity, item.rule, item.path))
    return {
        "verdict": "blocked" if findings else "review-required",
        "file_count": file_count,
        "total_bytes": total_bytes,
        "findings": [asdict(item) for item in findings],
    }


def has_executable_paths(paths: Iterable[str]) -> bool:
    return any(PurePosixPath(path).suffix.lower() in EXECUTABLE_SUFFIXES for path in paths)


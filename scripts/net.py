"""Small HTTPS client with host allowlisting and response limits."""

from __future__ import annotations

import json
from typing import Optional
import urllib.error
import urllib.parse
import urllib.request

ALLOWED_HOSTS = {"api.github.com", "raw.githubusercontent.com"}
USER_AGENT = "baomiao-codex-marketplace/0.1 (+https://github.com/)"


class SafeRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: ANN001
        validate_url(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


OPENER = urllib.request.build_opener(SafeRedirectHandler())


def validate_url(url: str) -> None:
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != "https" or parsed.hostname not in ALLOWED_HOSTS:
        raise ValueError(f"拒绝访问非允许来源：{url}")
    if parsed.username or parsed.password:
        raise ValueError("来源 URL 不得内嵌凭证")


def fetch_bytes(url: str, *, max_bytes: int = 524_288, token: Optional[str] = None) -> bytes:
    validate_url(url)
    headers = {"Accept": "application/vnd.github+json", "User-Agent": USER_AGENT}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)
    try:
        with OPENER.open(request, timeout=25) as response:
            declared = response.headers.get("Content-Length")
            if declared and int(declared) > max_bytes:
                raise ValueError(f"响应超过 {max_bytes} 字节限制")
            data = response.read(max_bytes + 1)
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"上游返回 HTTP {exc.code}: {url}") from exc
    if len(data) > max_bytes:
        raise ValueError(f"响应超过 {max_bytes} 字节限制")
    return data


def fetch_json(url: str, *, max_bytes: int = 2_097_152, token: Optional[str] = None):
    return json.loads(fetch_bytes(url, max_bytes=max_bytes, token=token))

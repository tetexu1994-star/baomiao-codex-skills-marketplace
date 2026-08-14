"use strict";

const PAGE_SIZE = 18;
const state = { entries: [], query: "", category: "", publisher: "", origin: "", risk: "", limit: PAGE_SIZE };
const importState = { descriptor: null, digest: "", returnFocus: null };
const labels = {
  official: "官方来源", community: "社区来源", low: "低风险", medium: "中风险", high: "增强权限",
  "filesystem-read": "读取文件", "filesystem-write": "写入文件", shell: "运行本机命令",
  browser: "浏览器", network: "联网", credentials: "使用凭证", "external-write": "写入外部服务", "system-config": "修改系统配置", none: "无需额外权限"
};

function element(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

function safeLink(url, text, className) {
  const link = element("a", className, text);
  const parsed = new URL(url);
  if (parsed.protocol !== "https:") throw new Error("目录包含非 HTTPS 链接");
  link.href = parsed.href;
  link.target = "_blank";
  link.rel = "noopener noreferrer";
  return link;
}

function makePill(text, type) {
  return element("span", `pill pill-${type}`, text);
}

function renderCard(entry) {
  const article = element("article", "skill-card");
  const top = element("div", "card-top");
  const badges = element("div", "badges");
  badges.append(makePill(labels[entry.publisher.kind], entry.publisher.kind));
  badges.append(makePill(labels[entry.risk.level], entry.risk.level));
  top.append(badges, element("span", "category-label", entry.category));

  const title = element("h3", "", entry.name);
  const summary = element("p", "summary", entry.summary_zh);
  const capabilityBox = element("div", "capabilities");
  capabilityBox.append(element("span", "capability-label", "运行能力"));
  const capabilityList = element("ul");
  entry.risk.capabilities.forEach((capability) => {
    capabilityList.append(element("li", "", labels[capability] || capability));
  });
  capabilityBox.append(capabilityList);

  const facts = element("dl", "facts");
  const skillCount = entry.integrity.files.filter((file) => file.path.endsWith("SKILL.md")).length;
  const factRows = [
    ["插件 ID", entry.id],
    ["包含 Skills", String(skillCount)],
    ["发布者", entry.publisher.name],
    ["许可证", `${entry.license.spdx} · ${entry.license.scope === "skill-directory" ? "目录级" : "仓库级"}`],
    ["固定版本", entry.source.commit.slice(0, 12)]
  ];
  factRows.forEach(([term, detail]) => {
    facts.append(element("dt", "", term), element("dd", "", detail));
  });

  const details = element("details", "review-details");
  details.append(element("summary", "", "查看来源与权限说明"));
  const detailsBody = element("div", "details-body");
  detailsBody.append(element("p", "", entry.risk.notes_zh));
  const path = element("code", "source-path", entry.source.path);
  detailsBody.append(path);
  const links = element("div", "source-links");
  links.append(
    safeLink(entry.source.repository, "原始仓库 ↗"),
    safeLink(entry.source.skill_url, "固定版本 SKILL.md ↗"),
    safeLink(entry.source.license_url, "许可证原文 ↗")
  );
  detailsBody.append(links);
  details.append(detailsBody);

  article.append(top, title, summary);
  if (entry.risk.level === "high") article.append(element("p", "enhanced-notice", "安装前需逐项确认增强权限"));
  article.append(capabilityBox, facts, details);
  return article;
}

function matches(entry) {
  const haystack = [entry.name, entry.summary_zh, entry.category, entry.publisher.name, ...entry.tags].join(" ").toLocaleLowerCase("zh-CN");
  return (!state.query || haystack.includes(state.query)) &&
    (!state.category || entry.category === state.category) &&
    (!state.publisher || entry.publisher.name === state.publisher) &&
    (!state.origin || entry.publisher.kind === state.origin) &&
    (!state.risk || entry.risk.level === state.risk);
}

function render() {
  const list = document.querySelector("#catalog-list");
  const visible = state.entries.filter(matches);
  const rendered = visible.slice(0, state.limit);
  list.replaceChildren(...rendered.map(renderCard));
  list.setAttribute("aria-busy", "false");
  document.querySelector("#empty-state").hidden = visible.length !== 0;
  document.querySelector("#catalog-meta").textContent = `显示 ${rendered.length} / 匹配 ${visible.length} · 共 ${state.entries.length} 个插件`;
  const more = document.querySelector("#load-more");
  more.hidden = rendered.length >= visible.length;
  more.textContent = `继续显示（还剩 ${Math.max(0, visible.length - rendered.length)} 个）`;
}

function bindFilters() {
  const form = document.querySelector("#filters");
  const read = () => {
    state.query = document.querySelector("#search").value.trim().toLocaleLowerCase("zh-CN");
    state.category = document.querySelector("#category").value;
    state.publisher = document.querySelector("#publisher").value;
    state.origin = document.querySelector("#origin").value;
    state.risk = document.querySelector("#risk").value;
    state.limit = PAGE_SIZE;
    render();
  };
  form.addEventListener("input", read);
  form.addEventListener("change", read);
  form.addEventListener("reset", () => window.setTimeout(read, 0));
  document.querySelector("#load-more").addEventListener("click", () => {
    state.limit += PAGE_SIZE;
    render();
  });
}

async function loadCatalog() {
  try {
    const response = await fetch("catalog.json", { cache: "no-store", credentials: "same-origin" });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const payload = await response.json();
    if (payload.schema_version !== 1 || !Array.isArray(payload.entries)) throw new Error("目录版本不支持");
    state.entries = payload.entries;
    const categories = [...new Set(state.entries.map((entry) => entry.category))].sort((a, b) => a.localeCompare(b, "zh-CN"));
    const select = document.querySelector("#category");
    categories.forEach((category) => {
      const option = element("option", "", category);
      option.value = category;
      select.append(option);
    });
    const publishers = [...new Set(state.entries.map((entry) => entry.publisher.name))].sort((a, b) => a.localeCompare(b, "zh-CN"));
    const publisherSelect = document.querySelector("#publisher");
    publishers.forEach((publisher) => {
      const option = element("option", "", publisher);
      option.value = publisher;
      publisherSelect.append(option);
    });
    document.querySelector("#approved-count").textContent = String(state.entries.length);
    document.querySelector("#footer-count").textContent = String(state.entries.length);
    render();
  } catch (error) {
    document.querySelector("#catalog-list").setAttribute("aria-busy", "false");
    document.querySelector("#catalog-meta").textContent = "目录读取失败";
    document.querySelector("#error-state").hidden = false;
  }
}

function isAllowedManifestUrl(url) {
  if (url.protocol === "https:") return true;
  return url.protocol === "http:" && ["127.0.0.1", "localhost"].includes(url.hostname);
}

async function sha256Hex(buffer) {
  const digest = await crypto.subtle.digest("SHA-256", buffer);
  return [...new Uint8Array(digest)].map((value) => value.toString(16).padStart(2, "0")).join("");
}

function validateImportDescriptor(descriptor) {
  const market = descriptor.marketplace || {};
  const command = descriptor.command || {};
  if (descriptor.schema_version !== 1 || market.id !== "baomiao-codex") throw new Error("导入描述版本不支持");
  if (!/^[0-9a-f]{40}$/.test(market.ref) || !Number.isInteger(market.plugin_count) || market.plugin_count < 1) throw new Error("导入描述缺少固定版本");
  if (market.manifest_path !== ".agents/plugins/marketplace.json") throw new Error("市场清单路径不受支持");
  if (command.executable !== "codex" || !Array.isArray(command.args) || !command.display.startsWith("codex plugin marketplace add ")) throw new Error("导入命令不受支持");
  if (descriptor.profile === "release" && !market.source.startsWith("https://github.com/")) throw new Error("发布市场必须来自 GitHub HTTPS 仓库");
}

function setImportStatus(message) {
  document.querySelector("#import-status").textContent = message;
}

async function copyImportCommand() {
  const command = importState.descriptor?.command?.display;
  if (!command) return;
  let copied = false;
  try {
    await navigator.clipboard.writeText(command);
    copied = true;
  } catch (error) {
    const field = element("textarea");
    field.value = command;
    field.setAttribute("readonly", "");
    field.className = "clipboard-fallback";
    document.body.append(field);
    field.select();
    copied = document.execCommand("copy");
    field.remove();
  }
  setImportStatus(copied ? "Codex 导入命令已复制。" : "复制失败，请在确认框中手动选择命令。");
}

function openImportDialog() {
  if (!importState.descriptor) return;
  const dialog = document.querySelector("#import-dialog");
  importState.returnFocus = document.activeElement;
  dialog.showModal();
  document.querySelector("#close-import").focus();
}

function closeImportDialog() {
  const dialog = document.querySelector("#import-dialog");
  if (dialog.open) dialog.close();
  importState.returnFocus?.focus();
}

function handoffToBaomiao() {
  if (!importState.descriptor) return;
  const manifestUrl = new URL("marketplace-import.json", window.location.href);
  if (!isAllowedManifestUrl(manifestUrl)) {
    setImportStatus("当前页面来源不受支持，请复制 Codex 命令导入。");
    closeImportDialog();
    return;
  }
  const deepLink = `baomiao://codex/marketplace/import?manifest=${encodeURIComponent(manifestUrl.href)}&digest=${importState.digest}`;
  setImportStatus("已把导入请求交给暴喵客户端；若没有弹出客户端，请复制 Codex 命令。");
  closeImportDialog();
  window.location.href = deepLink;
}

function bindImportControls() {
  document.querySelector("#open-import").addEventListener("click", openImportDialog);
  document.querySelector("#close-import").addEventListener("click", closeImportDialog);
  document.querySelector("#cancel-import").addEventListener("click", closeImportDialog);
  document.querySelector("#confirm-import").addEventListener("click", handoffToBaomiao);
  document.querySelector("#copy-import-command").addEventListener("click", copyImportCommand);
  document.querySelector("#copy-dialog-command").addEventListener("click", copyImportCommand);
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && document.querySelector("#import-dialog").open) closeImportDialog();
  });
}

async function loadImportDescriptor() {
  const openButton = document.querySelector("#open-import");
  const copyButton = document.querySelector("#copy-import-command");
  try {
    const [descriptorResponse, digestResponse] = await Promise.all([
      fetch("marketplace-import.json", { cache: "no-store", credentials: "same-origin" }),
      fetch("marketplace-import.sha256", { cache: "no-store", credentials: "same-origin" }),
    ]);
    if (!descriptorResponse.ok || !digestResponse.ok) throw new Error("导入描述读取失败");
    const bytes = await descriptorResponse.arrayBuffer();
    const expectedDigest = (await digestResponse.text()).trim().split(/\s+/)[0];
    const actualDigest = await sha256Hex(bytes);
    if (!/^[0-9a-f]{64}$/.test(expectedDigest) || actualDigest !== expectedDigest) throw new Error("导入描述摘要不匹配");
    const descriptor = JSON.parse(new TextDecoder().decode(bytes));
    validateImportDescriptor(descriptor);
    importState.descriptor = descriptor;
    importState.digest = actualDigest;
    document.querySelector("#import-source").textContent = descriptor.marketplace.source;
    document.querySelector("#import-ref").textContent = descriptor.marketplace.ref.slice(0, 12);
    document.querySelector("#import-count").textContent = `${descriptor.marketplace.plugin_count} 个插件`;
    document.querySelector("#import-command").textContent = descriptor.command.display;
    document.querySelector("#import-summary").textContent = `${descriptor.marketplace.plugin_count} 个插件，加入市场后在 Codex 里按需启用。来源与固定版本会在执行前再次展示。`;
    openButton.textContent = "暴喵一键导入";
    openButton.disabled = false;
    copyButton.disabled = false;
  } catch (error) {
    openButton.textContent = "一键导入暂不可用";
    document.querySelector("#import-summary").textContent = "导入描述校验失败。插件目录仍可浏览，请稍后刷新页面。";
    setImportStatus("未执行任何导入操作。");
  }
}

bindFilters();
bindImportControls();
loadCatalog();
loadImportDescriptor();

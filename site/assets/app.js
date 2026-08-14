"use strict";

const PAGE_SIZE = 18;
const state = { entries: [], catalogDigest: "", query: "", category: "", publisher: "", origin: "", risk: "", limit: PAGE_SIZE };
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

function skillNames(entry) {
  return entry.integrity.files
    .filter((file) => file.path.endsWith("SKILL.md"))
    .map((file) => {
      const segments = file.path.split("/");
      return segments.length > 1 ? segments.at(-2) : entry.id;
    })
    .filter(Boolean);
}

function normalizeSearch(value) {
  return value.normalize("NFKC")
    .toLocaleLowerCase("zh-CN")
    .replace(/[-_./\\]+/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function matchesQuery(value) {
  if (!state.query) return true;
  const haystack = normalizeSearch(value);
  return state.query.split(" ").every((token) => haystack.includes(token));
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
  const includedSkills = skillNames(entry);
  const skillCount = includedSkills.length;
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

  let bundlePreview = null;
  if (skillCount > 1) {
    const matchedSkills = state.query ? includedSkills.filter((name) => matchesQuery(name)) : [];
    const previewSkills = (matchedSkills.length ? matchedSkills : includedSkills).slice(0, 8);
    bundlePreview = element("div", "bundle-preview");
    bundlePreview.append(element("span", "bundle-label", matchedSkills.length ? "匹配 Skills" : "包含 Skills"));
    const bundleList = element("ul");
    previewSkills.forEach((name) => bundleList.append(element("li", "", name)));
    bundlePreview.append(bundleList);
    const hiddenCount = (matchedSkills.length || skillCount) - previewSkills.length;
    if (hiddenCount > 0) bundlePreview.append(element("small", "", `另有 ${hiddenCount} 个，可继续搜索`));
  }

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
  article.append(capabilityBox);
  if (bundlePreview) article.append(bundlePreview);
  article.append(facts, details);
  return article;
}

function matches(entry) {
  const haystack = [entry.name, entry.id, entry.summary_zh, entry.category, entry.publisher.name, ...entry.tags, ...skillNames(entry)].join(" ");
  return matchesQuery(haystack) &&
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
  document.querySelector("#catalog-meta").textContent = `目录已校验 · 显示 ${rendered.length} / 匹配 ${visible.length} · 共 ${state.entries.length} 个插件`;
  const more = document.querySelector("#load-more");
  more.hidden = rendered.length >= visible.length;
  more.textContent = `继续显示（还剩 ${Math.max(0, visible.length - rendered.length)} 个）`;
}

function bindFilters() {
  const form = document.querySelector("#filters");
  const read = () => {
    state.query = normalizeSearch(document.querySelector("#search").value);
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
    const { payload, digest } = await fetchVerifiedJson("catalog.json", "catalog.sha256", "目录");
    if (payload.schema_version !== 1 || !Array.isArray(payload.entries)) throw new Error("目录版本不支持");
    state.entries = payload.entries;
    state.catalogDigest = digest;
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
    renderImportReadiness();
  } catch (error) {
    document.querySelector("#catalog-list").setAttribute("aria-busy", "false");
    document.querySelector("#catalog-meta").textContent = "目录读取失败";
    document.querySelector("#error-state").hidden = false;
    failImport("市场目录校验失败。一键导入已停用，刷新后仍失败请检查网络。", "目录未通过校验，未执行任何导入操作。");
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

async function fetchVerifiedJson(documentPath, digestPath, label) {
  const [documentResponse, digestResponse] = await Promise.all([
    fetch(documentPath, { cache: "no-store", credentials: "same-origin" }),
    fetch(digestPath, { cache: "no-store", credentials: "same-origin" }),
  ]);
  if (!documentResponse.ok || !digestResponse.ok) throw new Error(`${label}读取失败`);
  const bytes = await documentResponse.arrayBuffer();
  const expectedDigest = (await digestResponse.text()).trim().split(/\s+/)[0];
  const actualDigest = await sha256Hex(bytes);
  if (!/^[0-9a-f]{64}$/.test(expectedDigest) || actualDigest !== expectedDigest) throw new Error(`${label}摘要不匹配`);
  return { payload: JSON.parse(new TextDecoder().decode(bytes)), digest: actualDigest };
}

function validateImportDescriptor(descriptor) {
  const market = descriptor.marketplace || {};
  const catalog = descriptor.catalog || {};
  const command = descriptor.command || {};
  if (descriptor.schema_version !== 1 || !["release", "local-preview"].includes(descriptor.profile) || market.id !== "baomiao-codex") throw new Error("导入描述版本不支持");
  if (!/^[0-9a-f]{40}$/.test(market.ref) || !Number.isInteger(market.plugin_count) || market.plugin_count < 1) throw new Error("导入描述缺少固定版本");
  if (market.manifest_path !== ".agents/plugins/marketplace.json") throw new Error("市场清单路径不受支持");
  if (descriptor.profile === "release") {
    if (!/^https:\/\/github\.com\/[A-Za-z0-9_.-]+\/[A-Za-z0-9_.-]+$/.test(market.source)) throw new Error("发布市场必须来自 GitHub HTTPS 仓库");
    const sourceUrl = new URL(market.source);
    const segments = sourceUrl.pathname.split("/").filter(Boolean);
    if (sourceUrl.protocol !== "https:" || sourceUrl.hostname !== "github.com" || sourceUrl.port || sourceUrl.username || sourceUrl.password || sourceUrl.search || sourceUrl.hash || segments.length !== 2) throw new Error("发布市场必须来自 GitHub HTTPS 仓库");
  } else if (!isAllowedManifestUrl(new URL(window.location.href)) || typeof market.source !== "string" || market.source.length < 2) {
    throw new Error("本地预览来源不受支持");
  }
  const expectedCommandArgs = ["plugin", "marketplace", "add", market.source];
  if (descriptor.profile === "release") expectedCommandArgs.push("--ref", market.ref);
  if (command.executable !== "codex" || JSON.stringify(command.args) !== JSON.stringify(expectedCommandArgs) || !command.display.startsWith("codex plugin marketplace add ")) throw new Error("导入命令不受支持");
  if (!/^[0-9a-f]{64}$/.test(catalog.sha256)) throw new Error("目录摘要无效");
  const expectedCatalogUrl = new URL("catalog.json", window.location.href).href;
  const expectedCatalogDigestUrl = new URL("catalog.sha256", window.location.href).href;
  if (new URL(catalog.url).href !== expectedCatalogUrl || new URL(catalog.sha256_url).href !== expectedCatalogDigestUrl) throw new Error("目录地址与当前市场不一致");
}

function setImportStatus(message) {
  document.querySelector("#import-status").textContent = message;
}

function failImport(summary, status) {
  const openButton = document.querySelector("#open-import");
  const copyButton = document.querySelector("#copy-import-command");
  openButton.textContent = "一键导入暂不可用";
  openButton.disabled = true;
  copyButton.disabled = true;
  document.querySelector("#import-summary").textContent = summary;
  setImportStatus(status);
}

function renderImportReadiness() {
  if (!importState.descriptor || !state.catalogDigest) return;
  const descriptor = importState.descriptor;
  if (descriptor.catalog.sha256 !== state.catalogDigest || descriptor.marketplace.plugin_count !== state.entries.length) {
    failImport("市场目录与导入描述不一致。一键导入已停用，请刷新页面。", "校验未通过，未执行任何导入操作。");
    return;
  }
  document.querySelector("#import-source").textContent = descriptor.marketplace.source;
  document.querySelector("#import-ref").textContent = descriptor.marketplace.ref.slice(0, 12);
  document.querySelector("#import-count").textContent = `${descriptor.marketplace.plugin_count} 个插件`;
  document.querySelector("#import-command").textContent = descriptor.command.display;
  document.querySelector("#import-summary").textContent = `${descriptor.marketplace.plugin_count} 个插件，目录与导入描述已校验；加入市场后在 Codex 里按需启用。`;
  const openButton = document.querySelector("#open-import");
  openButton.textContent = "暴喵一键导入";
  openButton.disabled = false;
  document.querySelector("#copy-import-command").disabled = false;
  setImportStatus("目录与导入描述已校验。");
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
  try {
    const { payload: descriptor, digest } = await fetchVerifiedJson("marketplace-import.json", "marketplace-import.sha256", "导入描述");
    validateImportDescriptor(descriptor);
    importState.descriptor = descriptor;
    importState.digest = digest;
    renderImportReadiness();
  } catch (error) {
    failImport("导入描述校验失败。插件目录仍可浏览，请稍后刷新页面。", "未执行任何导入操作。");
  }
}

bindFilters();
bindImportControls();
loadCatalog();
loadImportDescriptor();

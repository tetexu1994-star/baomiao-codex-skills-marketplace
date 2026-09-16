"use strict";

const PAGE_SIZE = 18;
const OFFICIAL_LIST_ARGS = ["plugin", "list", "--available", "--json"];
const state = { entries: [], catalogDigest: "", query: "", category: "", publisher: "", origin: "", risk: "", limit: PAGE_SIZE };
const importState = { descriptor: null, pasteValue: "", returnFocus: null };
const federatedState = { source: null, command: "" };
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
  capabilityBox.append(element("span", "capability-label", "可能使用"));
  const capabilityList = element("ul");
  entry.risk.capabilities.forEach((capability) => {
    capabilityList.append(element("li", "", labels[capability] || capability));
  });
  capabilityBox.append(capabilityList);

  const facts = element("dl", "facts");
  const includedSkills = skillNames(entry);
  const skillCount = includedSkills.length;
  const cardMeta = element("p", "card-meta", `${entry.publisher.name} · ${skillCount} Skills · ${entry.license.spdx}`);
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
  details.append(element("summary", "", "来源、版本与权限"));
  const detailsBody = element("div", "details-body");
  detailsBody.append(element("p", "", entry.risk.notes_zh));
  const path = element("code", "source-path", entry.source.path);
  detailsBody.append(facts, path);
  const links = element("div", "source-links");
  links.append(
    safeLink(entry.source.repository, "原始仓库 ↗"),
    safeLink(entry.source.skill_url, "固定版本 SKILL.md ↗"),
    safeLink(entry.source.license_url, "许可证原文 ↗")
  );
  detailsBody.append(links);
  details.append(detailsBody);

  article.append(top, title, summary, cardMeta);
  if (entry.risk.level === "high") article.append(element("p", "enhanced-notice", "安装前需逐项确认增强权限"));
  article.append(capabilityBox);
  if (bundlePreview) article.append(bundlePreview);
  article.append(details);
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
  renderOfficialFeatured();
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
    document.querySelector("#router-approved-count").textContent = String(state.entries.length);
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

function marketplacePasteValue(descriptor) {
  const market = descriptor.marketplace;
  if (descriptor.profile === "local-preview") return market.source;
  const sourceUrl = new URL(market.source);
  const repository = sourceUrl.pathname.replace(/^\/+|\/+$/g, "").replace(/\.git$/, "");
  if (sourceUrl.hostname !== "github.com" || !/^[A-Za-z0-9_.-]+\/[A-Za-z0-9_.-]+$/.test(repository)) {
    return "";
  }
  return `${repository}@${market.ref}`;
}

function failImport(summary, status) {
  const openButton = document.querySelector("#open-import");
  const copyButton = document.querySelector("#copy-import-command");
  openButton.textContent = "市场地址暂不可用";
  openButton.disabled = true;
  copyButton.disabled = true;
  const kicker = document.querySelector("#import-kicker");
  kicker.className = "import-kicker is-error";
  kicker.textContent = "市场地址暂不可用";
  document.querySelector("#import-summary").textContent = summary;
  setImportStatus(status);
}

function renderImportReadiness() {
  if (!importState.descriptor || !state.catalogDigest) return;
  const descriptor = importState.descriptor;
  if (descriptor.catalog.sha256 !== state.catalogDigest || descriptor.marketplace.plugin_count !== state.entries.length) {
    failImport("市场目录与仓库描述不一致。复制功能已停用，请刷新页面。", "校验未通过，未复制任何内容。");
    return;
  }
  importState.pasteValue = marketplacePasteValue(descriptor);
  if (!importState.pasteValue) {
    failImport("仓库地址无法转换为 Codex 市场来源。", "校验未通过，未复制任何内容。");
    return;
  }
  document.querySelector("#import-source").textContent = descriptor.marketplace.source;
  document.querySelector("#import-ref").textContent = descriptor.marketplace.ref.slice(0, 12);
  document.querySelector("#import-count").textContent = `${descriptor.marketplace.plugin_count} 个插件`;
  document.querySelector("#import-paste-value").textContent = importState.pasteValue;
  document.querySelector("#import-command").textContent = descriptor.command.display;
  document.querySelector("#import-summary").textContent = `${descriptor.marketplace.plugin_count} 个插件已校验。复制市场地址，粘贴到 Codex 的“添加插件市场”即可。`;
  const kicker = document.querySelector("#import-kicker");
  kicker.className = "import-kicker is-ready";
  kicker.textContent = "GitHub 仓库与版本已校验";
  const openButton = document.querySelector("#open-import");
  openButton.textContent = "复制市场地址";
  openButton.disabled = false;
  document.querySelector("#copy-import-command").disabled = false;
  setImportStatus("无需终端，也不会批量安装插件。");
}

async function copyText(value) {
  let copied = false;
  try {
    await navigator.clipboard.writeText(value);
    copied = true;
  } catch (error) {
    const field = element("textarea");
    field.value = value;
    field.setAttribute("readonly", "");
    field.className = "clipboard-fallback";
    document.body.append(field);
    field.select();
    copied = document.execCommand("copy");
    field.remove();
  }
  return copied;
}

async function copyImportCommand() {
  const command = importState.descriptor?.command?.display;
  if (!command) return;
  const copied = await copyText(command);
  setImportStatus(copied ? "Codex 备用命令已复制。" : "复制失败，请在确认框中手动选择命令。");
}

async function copyMarketplaceSource() {
  if (!importState.pasteValue) return;
  const copied = await copyText(importState.pasteValue);
  setImportStatus(copied ? "市场地址已复制。打开 Codex → 插件 → 添加 → 添加插件市场，然后粘贴。" : "复制失败，请在确认框中手动选择市场地址。");
  if (document.querySelector("#import-dialog").open) closeImportDialog();
}

function validateFederatedDescriptor(descriptor) {
  if (descriptor.schema_version !== 1 || !Array.isArray(descriptor.sources) || descriptor.sources.length !== 1) throw new Error("联邦来源版本不支持");
  const source = descriptor.sources[0];
  const command = source.access?.command || {};
  const provenance = source.provenance || {};
  const boundaries = source.boundaries || {};
  if (source.id !== "codex-official-directory" || source.publisher?.name !== "OpenAI" || source.publisher?.kind !== "official") throw new Error("官方来源身份无效");
  if (source.access?.mode !== "codex-native" || command.executable !== "codex" || JSON.stringify(command.args) !== JSON.stringify(OFFICIAL_LIST_ARGS) || command.display !== "codex plugin list --available --json") throw new Error("官方来源命令不受支持");
  if (!Array.isArray(source.access.marketplace_ids) || source.access.marketplace_ids.length < 1 || !source.access.marketplace_ids.every((id) => ["openai-curated-remote", "openai-api-curated"].includes(id))) throw new Error("官方市场标识不受支持");
  if (provenance.historical_repository !== "https://github.com/openai/plugins" || provenance.historical_repository_status !== "archived" || provenance.archived_at !== "2026-08-16") throw new Error("历史来源状态无效");
  const docsUrl = new URL(provenance.documentation);
  if (docsUrl.protocol !== "https:" || docsUrl.hostname !== "learn.chatgpt.com") throw new Error("官方文档地址无效");
  if (boundaries.mirror_packages !== false || boundaries.availability !== "account-and-product-dependent" || boundaries.credentials_handled_by !== "codex" || boundaries.count_mode !== "runtime") throw new Error("官方来源边界无效");
  if (!Array.isArray(source.featured_plugins) || source.featured_plugins.length < 1 || !source.featured_plugins.every((plugin) =>
    /^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(plugin.id) &&
    typeof plugin.name === "string" && plugin.name.length > 0 &&
    typeof plugin.name_zh === "string" && plugin.name_zh.length > 0 &&
    typeof plugin.summary_zh === "string" && plugin.summary_zh.length >= 8 &&
    Array.isArray(plugin.search_terms_zh) && plugin.search_terms_zh.length > 0 &&
    typeof plugin.requires_connection === "boolean"
  )) throw new Error("官方插件示例无效");
  if (!Array.isArray(boundaries.notes_zh) || boundaries.notes_zh.length < 2) throw new Error("官方来源说明不完整");
  return source;
}

function renderFederatedSource(source) {
  federatedState.source = source;
  federatedState.command = source.access.command.display;
  const status = document.querySelector("#official-source-status");
  status.className = "source-state source-state-native";
  status.textContent = "Codex 原生 · 动态";
  renderOfficialFeatured();
  document.querySelector("#official-boundary").textContent = source.boundaries.notes_zh.join(" ");
  document.querySelector("#official-command").textContent = source.access.command.display;
  document.querySelector("#official-docs").href = source.provenance.documentation;
  document.querySelector("#official-provenance").textContent = `历史示例仓库已于 ${source.provenance.archived_at} 归档，仅作来源证据，不作为安装回退。`;
  document.querySelector("#copy-official-command").disabled = false;
  document.querySelector("#sources").setAttribute("aria-busy", "false");
}

function renderOfficialFeatured() {
  if (!federatedState.source) return;
  const featured = document.querySelector("#official-featured");
  const plugins = federatedState.source.featured_plugins.filter((plugin) => {
    const haystack = [plugin.name, plugin.name_zh, plugin.category_zh, plugin.summary_zh, ...plugin.search_terms_zh].join(" ");
    return matchesQuery(haystack);
  });
  if (!plugins.length) {
    featured.replaceChildren(element("li", "official-empty", "官方推荐中没有匹配项；暴喵精选结果仍显示在下方。"));
    return;
  }
  featured.replaceChildren(...plugins.map((plugin) => {
    const item = element("li");
    const copy = element("div", "official-plugin-copy");
    copy.append(element("strong", "", plugin.name_zh), element("p", "", plugin.summary_zh));
    const meta = element("div", "official-plugin-meta");
    meta.append(element("small", "", plugin.category_zh));
    if (plugin.requires_connection) meta.append(element("small", "official-connect", "在 Codex 中连接"));
    item.append(copy, meta);
    return item;
  }));
}

function failFederatedSource() {
  const status = document.querySelector("#official-source-status");
  status.className = "source-state source-state-error";
  status.textContent = "来源描述未通过校验";
  document.querySelector("#official-boundary").textContent = "暴喵精选目录仍可正常浏览。官方插件请直接在 Codex 的 Plugins 页面查看。";
  document.querySelector("#official-provenance").textContent = "未执行命令，也未读取任何账号或凭证。";
  document.querySelector("#sources").setAttribute("aria-busy", "false");
}

async function loadFederatedSources() {
  try {
    const { payload } = await fetchVerifiedJson("federated-sources.json", "federated-sources.sha256", "官方来源描述");
    renderFederatedSource(validateFederatedDescriptor(payload));
  } catch (error) {
    failFederatedSource();
  }
}

async function copyOfficialCommand() {
  if (!federatedState.command) return;
  const copied = await copyText(federatedState.command);
  document.querySelector("#official-command-status").textContent = copied ? "官方目录命令已复制。" : "复制失败，请在 Codex 的 Plugins 页面查看官方目录。";
}

function bindFederatedControls() {
  document.querySelector("#copy-official-command").addEventListener("click", copyOfficialCommand);
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

function bindImportControls() {
  document.querySelector("#open-import").addEventListener("click", copyMarketplaceSource);
  document.querySelector("#close-import").addEventListener("click", closeImportDialog);
  document.querySelector("#cancel-import").addEventListener("click", closeImportDialog);
  document.querySelector("#confirm-import").addEventListener("click", copyMarketplaceSource);
  document.querySelector("#copy-import-command").addEventListener("click", openImportDialog);
  document.querySelector("#copy-dialog-command").addEventListener("click", copyImportCommand);
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && document.querySelector("#import-dialog").open) closeImportDialog();
  });
}

async function loadImportDescriptor() {
  try {
    const { payload: descriptor } = await fetchVerifiedJson("marketplace-import.json", "marketplace-import.sha256", "导入描述");
    validateImportDescriptor(descriptor);
    importState.descriptor = descriptor;
    renderImportReadiness();
  } catch (error) {
    failImport("导入描述校验失败。插件目录仍可浏览，请稍后刷新页面。", "未执行任何导入操作。");
  }
}

bindFilters();
bindImportControls();
bindFederatedControls();
loadCatalog();
loadImportDescriptor();
loadFederatedSources();

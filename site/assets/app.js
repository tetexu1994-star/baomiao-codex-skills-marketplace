"use strict";

const PAGE_SIZE = 18;
const state = { entries: [], query: "", category: "", publisher: "", origin: "", risk: "", limit: PAGE_SIZE };
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
  const factRows = [
    ["插件 ID", entry.id],
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
    render();
  } catch (error) {
    document.querySelector("#catalog-list").setAttribute("aria-busy", "false");
    document.querySelector("#catalog-meta").textContent = "目录读取失败";
    document.querySelector("#error-state").hidden = false;
  }
}

bindFilters();
loadCatalog();

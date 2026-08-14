# Marketplace Visual Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Redesign the marketplace so a Chinese Windows beginner immediately understands the product, trusts the one-click import, and can scan plugins without the page looking like an old admin console.

**Architecture:** Preserve the static HTML/CSS/JavaScript runtime and every import/security validation. Restructure only the presentation hierarchy: one contained hero shell combines the product promise, a three-step signal rail, and the import action; a unified light canvas contains a modern filter toolbar and lower-density plugin cards whose source details remain available on demand.

**Tech Stack:** Semantic HTML, dependency-free CSS, vanilla JavaScript, Python `unittest`, Playwright CLI, browser-verification artifacts.

---

## Design system

- **Subject:** 暴喵客户端里的 Codex 插件入口，而不是独立技术文档站。
- **Audience:** 中国大陆 Windows 小白。
- **Single job:** 先放心加入市场，再找到并按需启用插件。
- **Palette:** canvas `#F4F7FB`, surface `#FFFFFF`, ink `#10233F`, navy `#071B33`, amber `#FFB319`, blue `#2F6BFF`, success `#16815F`.
- **Typography:** Chinese display/body use `Microsoft YaHei UI`; Latin numerals and utility labels use Windows-native `Bahnschrift` and `Cascadia Mono` fallbacks.
- **Layout:** a centered 1240px product shell; dark product story on the left, light import card on the right; catalog flows below on the same canvas.
- **Signature:** a three-node amber “signal rail” that encodes the real user sequence: 加入市场 → 选择插件 → 按需启用.
- **Restraint:** hero shell gets the largest radius, cards use a smaller radius, controls use 8–10px, and pills alone use capsule geometry. No decorative gradients or shadow stacks.

### Task 1: Lock the new hierarchy with a regression test

**Files:**
- Modify: `tests/test_catalog.py`

- [x] **Step 1: Add a failing structural design test**

Add `test_homepage_uses_product_shell_and_progressive_card_details`. It must require `hero-shell`, `journey-steps`, `card-meta`, semantic color tokens, and the cache-buster `20260814d`; it must also reject the old 1px-gap table filter declaration.

- [x] **Step 2: Run the focused test**

Run: `.venv/bin/python -m unittest tests.test_catalog.CatalogTests.test_homepage_uses_product_shell_and_progressive_card_details -v`

Expected: FAIL because the current HTML has separate full-width hero/import strips and table-style filters.

### Task 2: Rebuild the product story and import hierarchy

**Files:**
- Modify: `site/index.html`
- Modify: `site/assets/styles.css`

- [x] **Step 1: Create the contained hero shell**

Wrap the intro and import action in `<div class="hero-shell">`. Keep one `h1`, move the plugin count into a compact product statistic, and use the copy “找到插件，一键加入 Codex”.

- [x] **Step 2: Add the signal rail**

Add this real ordered sequence inside the intro:

```html
<ol class="journey-steps" aria-label="使用步骤">
  <li><span>1</span><b>加入市场</b><small>只添加目录</small></li>
  <li><span>2</span><b>选择插件</b><small>查看来源权限</small></li>
  <li><span>3</span><b>按需启用</b><small>不会批量安装</small></li>
</ol>
```

- [x] **Step 3: Turn the import strip into a focused action card**

Keep all existing IDs and live regions, but present verified state, boundary text, primary action, and command fallback in one light panel. Replace technical top navigation with “一键导入 / 浏览插件”; keep the client contract in the footer.

### Task 3: Reduce catalog and card density

**Files:**
- Modify: `site/assets/app.js`
- Modify: `site/assets/styles.css`

- [x] **Step 1: Add a compact plugin meta line**

Render `<p class="card-meta">发布者 · N Skills · SPDX</p>` immediately after the summary.

- [x] **Step 2: Move technical facts into details**

Keep plugin ID, fixed commit, license scope, source path, risk notes, and source links, but append the facts list inside `.details-body`. Change the disclosure label to “来源、版本与权限”.

- [x] **Step 3: Rebuild filters as a toolbar**

Use a padded surface with real gaps, independently outlined controls, a dominant search field, and a quiet reset button. Never use a 1px-gap background grid.

- [x] **Step 4: Restyle cards**

Use subtle border/shadow separation, consistent 14px card radius, readable 12–15px secondary type, compact capability chips, and restrained hover lift. Keep risk and official/community labels visible without thick top borders.

### Task 4: Responsive and dialog polish

**Files:**
- Modify: `site/assets/styles.css`
- Modify: `site/index.html`

- [x] **Step 1: Define layout breakpoints**

At 980px stack hero columns and use two catalog columns. At 680px reduce the outer hero radius, stack filters/cards/actions, keep navigation usable, and preserve 44px minimum controls.

- [x] **Step 2: Harmonize the dialog**

Use the same navy/surface/amber tokens, reduce the shadow, improve fact spacing, and preserve existing focus/Escape behavior.

- [x] **Step 3: Respect reduced motion**

Keep hover transition under 180ms and retain the existing `prefers-reduced-motion` override.

### Task 5: Verify, document, and commit

**Files:**
- Modify: `docs/superpowers/plans/2026-08-14-marketplace-visual-redesign.md`
- Create: `docs/reviews/deepseek-ui-review-2026-08-14.md`

- [x] **Step 1: Run syntax, focused, full, and catalog checks**

Run `node --check site/assets/app.js`, the focused test, `.venv/bin/python -m unittest discover -s tests -v`, and `.venv/bin/python -m scripts.validate_catalog`.

Expected: all tests pass and 77 approved entries validate.

- [ ] **Step 2: Verify 320, 768, 1024, and 1440 pixels**

Check horizontal overflow, visible one-click boundary, search for `azure functions`, single-Skill count, dialog focus return, empty state, and console warnings/errors.

> Blocked in this run: the in-app browser refused control of the local URL under its URL security policy. The local server was restored for manual refresh, but no alternate browser surface was used to bypass the policy.

- [x] **Step 3: Record the independent opinion and decisions**

Summarize DeepSeek's five findings and document which were accepted, adapted, or rejected. Do not describe model output as verification.

- [x] **Step 4: Commit the reviewed implementation**

Stage only task files and commit with `feat: redesign marketplace experience`. Browser-verification artifacts remain intentionally absent until the URL policy permits a real visual pass.

# Marketplace Hardening and Discovery Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the public marketplace verify the catalog it renders, let users discover Skills contained inside bundle plugins, and only enable one-click import when every linked artifact agrees.

**Architecture:** Keep the static GitHub Pages architecture and existing visual language. Add small client-side helpers in `site/assets/app.js` for SHA-256 verification, normalized search terms, bundle Skill summaries, and strict descriptor checks; expose verification state through existing status regions and style only the new bundle-search affordance.

**Tech Stack:** Static HTML/CSS/JavaScript, Python `unittest`, JSON/SHA-256 artifacts, in-app browser verification.

---

### Task 1: Lock the behavior with regression tests

**Files:**
- Modify: `tests/test_catalog.py`

- [x] **Step 1: Add a failing static contract test**

Assert that the homepage script fetches `catalog.sha256`, compares the descriptor catalog digest, validates exact command arguments, and derives searchable names from `SKILL.md` paths.

- [x] **Step 2: Run the focused test and verify it fails**

Run: `python -m unittest tests.test_catalog.CatalogTests.test_homepage_verifies_catalog_and_searches_bundle_skills -v`

Expected: FAIL because the current script only fetches `catalog.json` and only searches entry-level metadata.

### Task 2: Verify the rendered catalog and import linkage

**Files:**
- Modify: `site/assets/app.js`
- Modify: `site/index.html`

- [x] **Step 1: Fetch catalog bytes and digest together**

Compute SHA-256 over the exact `catalog.json` bytes before parsing, reject malformed digest files, and keep the verified digest in application state.

- [x] **Step 2: Gate one-click import on cross-artifact agreement**

Validate `marketplace-import.json` profile, source URL, exact command argument array, same-origin catalog URLs, and require `descriptor.catalog.sha256` to equal the verified catalog digest before enabling both import buttons.

- [x] **Step 3: Surface verification in plain Chinese**

Keep the controls disabled until both artifacts are verified, then announce “目录与导入描述已校验” through the existing polite live region. On mismatch, leave browsing available but keep import disabled with a concrete recovery message.

### Task 3: Make bundle Skills discoverable

**Files:**
- Modify: `site/assets/app.js`
- Modify: `site/assets/styles.css`

- [x] **Step 1: Derive bundle Skill names**

Extract each parent directory from integrity paths ending in `SKILL.md`, normalize separators and punctuation, and add those names to the search index.

- [x] **Step 2: Use token-aware matching**

Normalize Unicode and punctuation, then require every query token to appear in the combined entry and bundle-Skill haystack. This makes `azure functions` match `azure-functions` without introducing a fuzzy-search dependency.

- [x] **Step 3: Explain why a bundle matched**

For multi-Skill plugins, show a compact “包含 Skills” preview. When the query matches internal names, show the matching names first and label them as matches; otherwise show a short representative preview and the remaining count.

### Task 4: Verify and deliver

**Files:**
- Modify: `docs/superpowers/plans/2026-08-14-marketplace-hardening-and-discovery.md`
- Create: `evidence/browser-verifications/<timestamp>-*.md`
- Create: `evidence/browser-verifications/<timestamp>-*.json`
- Create: `evidence/browser-verifications/screenshots/*`

- [x] **Step 1: Run focused and full tests**

Run: `python -m unittest tests.test_catalog.CatalogTests.test_homepage_verifies_catalog_and_searches_bundle_skills -v`

Run: `python -m unittest discover -s tests -v`

Expected: all tests PASS.

- [x] **Step 2: Rebuild and validate**

Run: `python -m scripts.build --generated-at "$(git show -s --format=%cI HEAD)"`

Run: `python -m scripts.validate_catalog`

Expected: 77 approved entries validate and local import artifacts are regenerated.

- [x] **Step 3: Verify the browser at 320, 768, 1024, and 1440 pixels**

Check no horizontal overflow, no console errors, verified import status, `azure functions` returning the Azure bundle with its matching Skill, keyboard dialog open/close, and the empty-search recovery state.

- [x] **Step 4: Persist browser evidence and commit**

Generate the standard browser-verification Markdown/JSON pair, mark all plan checkboxes complete, then commit the reviewed diff with a focused message.

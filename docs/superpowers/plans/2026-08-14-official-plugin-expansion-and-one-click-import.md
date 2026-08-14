# Official Plugin Expansion And One-click Import Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Expand the reviewed marketplace with license-clear official Codex plugin sources and add a Baomiao one-click whole-market import flow with a Codex CLI fallback.

**Architecture:** Keep the Baomiao repository as the single marketplace users register. A deterministic packager vendors only reviewed plugin/skill files from fixed upstream commits, while the catalog remains the source of Chinese product metadata and integrity evidence. A small import descriptor carries the repository/ref identity; the web CTA opens a Baomiao custom protocol after showing the source and always exposes the equivalent `codex plugin marketplace add` command.

**Tech Stack:** Python 3.9+, JSON Schema, Codex plugin manifests, vanilla HTML/CSS/JavaScript, unittest, Git.

---

### Task 1: Freeze and review official upstreams

**Files:**
- Modify: `sources.json`
- Create: `docs/reviews/official-plugin-expansion-2026-08-14.md`
- Create: `docs/decisions/0009-federated-official-bundles.md`
- Test: `tests/test_official_expansion.py`

- [x] **Step 1: Write failing source-policy tests**

Assert every new source uses an HTTPS GitHub repository, candidate-only policy, repository or directory license evidence, a fixed-size limit, and `allow_executable_files: false`.

- [x] **Step 2: Run the focused test and confirm failure**

Run: `python -m unittest tests.test_official_expansion -v`
Expected: FAIL because the official expansion sources and review record do not exist.

- [x] **Step 3: Inspect each upstream at a fixed commit**

Record the repository, resolved 40-character commit, marketplace/plugin paths, license scope, executable/script findings, and the exact publish/defer decision. Do not copy deferred files.

- [x] **Step 4: Add only approved paths to `sources.json`**

Every new source remains `candidate-only`; automatic synchronization must never edit `catalog/approved`, `plugins`, or `.agents/plugins/marketplace.json`.

- [x] **Step 5: Run the focused test**

Run: `python -m unittest tests.test_official_expansion -v`
Expected: PASS.

### Task 2: Add deterministic official-plugin packaging

**Files:**
- Create: `scripts/package_official_plugins.py`
- Modify: `.agents/plugins/marketplace.json`
- Create: `catalog/approved/<new-plugin>.json`
- Create: `catalog/candidates/<new-plugin>-<commit>.json`
- Create: `plugins/<new-plugin>/.codex-plugin/plugin.json`
- Create: `plugins/<new-plugin>/skills/**`
- Test: `tests/test_official_expansion.py`

- [x] **Step 1: Extend tests for package reproducibility and manifest identity**

Assert folder name equals manifest name, every marketplace source path exists, package license evidence is present, and rerunning the packager produces no Git diff.

- [x] **Step 2: Run the focused test and confirm failure**

Run: `python -m unittest tests.test_official_expansion -v`
Expected: FAIL because packages do not exist.

- [x] **Step 3: Implement the fixed-commit packager**

Read committed Git objects only, reject origin mismatches, symlinks, oversized files, executable bits, install scripts, secret-like content, and dangerous-command findings. Generate candidates first; copy into public plugin directories only for an explicit reviewed allowlist in the script.

- [x] **Step 4: Generate Chinese catalog and Codex manifests**

Append new plugins in stable order with `policy.installation: AVAILABLE`, explicit authentication timing, and meaningful categories. Preserve upstream authorship and licenses.

- [x] **Step 5: Validate all generated plugins**

Run: `python /Users/tetexu/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py plugins/<new-plugin>` for every new plugin.
Expected: every invocation prints a valid result and exits 0.

- [x] **Step 6: Run focused tests twice**

Run the packager, `git diff --exit-code`, then rerun `python -m unittest tests.test_official_expansion -v`.
Expected: no diff after the second generation and all tests PASS.

### Task 3: Build the whole-market import descriptor

**Files:**
- Modify: `scripts/build.py`
- Create: `schema/marketplace-import.schema.json`
- Create: `site/marketplace-import.json`
- Create: `site/marketplace-import.sha256`
- Modify: `tests/test_catalog.py`

- [x] **Step 1: Write failing descriptor tests**

Assert the descriptor has a schema version, marketplace ID, HTTPS Git source, fixed ref, expected marketplace path, catalog URLs, plugin count, digest, and no credentials.

- [x] **Step 2: Run the focused test and confirm failure**

Run: `python -m unittest tests.test_catalog -v`
Expected: FAIL because the import descriptor is not built.

- [x] **Step 3: Extend the deterministic builder**

Add `--marketplace-source`, `--marketplace-ref`, and `--public-base-url`. Build the descriptor and SHA-256 beside the catalog without tokens or user-specific paths. Release builds require HTTPS URLs and a 40-character ref; local preview may use the explicit local-preview profile.

- [x] **Step 4: Run focused tests**

Run: `python -m unittest tests.test_catalog -v`
Expected: PASS.

### Task 4: Add accessible one-click import UI

**Files:**
- Modify: `site/index.html`
- Modify: `site/assets/app.js`
- Modify: `site/assets/styles.css`
- Test: `tests/test_catalog.py`

- [x] **Step 1: Add static UI contract tests**

Assert the page exposes a real button, a source-confirmation dialog, a copy-command fallback, visible status text, keyboard-close behavior, and no hard-coded token.

- [x] **Step 2: Run the focused test and confirm failure**

Run: `python -m unittest tests.test_catalog -v`
Expected: FAIL because the one-click controls do not exist.

- [x] **Step 3: Implement the import interaction**

Fetch and verify the import descriptor metadata, show repository/ref/plugin count, and open `baomiao://codex/marketplace/import?manifest=<encoded HTTPS URL>&digest=<sha256>` only after confirmation. Copy the exact Codex CLI command when the protocol is unavailable or the user chooses manual import.

- [x] **Step 4: Polish responsive and accessible behavior**

Keep the existing compact industrial visual language, use a single high-emphasis import strip as the signature element, support 320/768/1024/1440 widths, visible focus, escape-to-close, live status messages, and reduced motion.

- [x] **Step 5: Run focused tests**

Run: `python -m unittest tests.test_catalog -v`
Expected: PASS.

### Task 5: Document the client handoff and release process

**Files:**
- Modify: `docs/client-contract.md`
- Modify: `README.md`
- Modify: `outputs/DELIVERY.md`
- Create: `docs/decisions/0010-baomiao-import-protocol.md`

- [x] **Step 1: Document protocol validation and confirmation**

Specify the custom-protocol request, allowlisted HTTPS manifest retrieval, digest check, Git source/ref/path display, confirmation, Codex CLI invocation without a shell, idempotent already-added behavior, and rollback/remove fallback.

- [x] **Step 2: Document local preview and release build commands**

Include exact Windows commands and the release-only values that require the final Baomiao GitHub repository and Pages URL.

- [x] **Step 3: Record the product decision**

State that Baomiao one-click is a client convenience around the supported Codex marketplace command, not an OpenAI deep link or silent install mechanism.

### Task 6: Full verification and optimization pass

**Files:**
- Modify: files above only when verification finds a concrete defect
- Create: `evidence/browser-verifications/20260814-暴喵市场一键导入与官方扩容.md`
- Create: `evidence/browser-verifications/screenshots/one-click-import.jpg`

- [x] **Step 1: Run all automated checks**

Run: `python -m unittest discover -s tests -v`, `python -m scripts.validate_catalog`, the online validator, the deterministic build, and every new plugin validator.
Expected: all commands exit 0.

- [x] **Step 2: Verify the site in a real browser**

Test initial load, search/filter, import dialog, command copy, escape close, keyboard focus, console errors, and widths 320/768/1024/1440.

- [x] **Step 3: Perform the requested second optimization pass**

Review the screenshot for density, wrapping, button clarity, and accidental emphasis. Make only evidence-driven fixes, rerun browser verification, and persist the final artifact.

- [x] **Step 4: Confirm repository scope and clean status**

Run: `git status --short`, confirm `/Users/tetexu/724tool` was never accessed, and list the exact GitHub account/repository data still needed to publish.

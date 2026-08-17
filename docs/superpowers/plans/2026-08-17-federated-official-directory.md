# Federated Official Directory Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a clearly separated Codex-native official plugin source beside the 77 reviewed Baomiao plugins without mirroring the now-archived `openai/plugins` repository or pretending its historical count is current.

**Architecture:** Keep the Baomiao Git marketplace and its 77 reviewed packages unchanged. Add a signed static federation descriptor that tells the website and Baomiao client how to discover the current official directory through the user's installed Codex CLI; render it as a source-routing panel, not as locally reviewed cards. Treat the archived OpenAI repository as historical evidence only.

**Tech Stack:** JSON Schema 2020-12, Python 3.9 build/validation, semantic HTML, dependency-free CSS and JavaScript, Python `unittest`.

---

## Design system extension

- **Subject:** A Windows-friendly routing panel between two truthful plugin sources.
- **Audience:** Chinese mainland Windows users who should not need to understand repository mirroring.
- **Single job:** Know which source they are browsing and what the next action does.
- **Palette:** Reuse canvas `#F4F7FB`, navy `#071B33`, amber `#FFB319`, blue `#2F6BFF`, success `#16815F`; reserve blue for the Codex-native route.
- **Type:** Keep Microsoft YaHei UI for Chinese, Bahnschrift/Cascadia Mono for source IDs and commands.
- **Layout:** A two-lane “source router” below the hero: Baomiao reviewed Git marketplace on the left, Codex native directory on the right. On mobile the lanes stack without losing source labels.
- **Signature:** A central route rail visually joins the two sources while their badges and actions remain distinct.

### Task 1: Lock the federation contract with failing tests

**Files:**
- Modify: `tests/test_catalog.py`

- [x] **Step 1: Add a federation build test**

Require `build()` to emit `dist/federated-sources.json`, `dist/federated-sources.sha256`, and same-origin copies in `site/`; validate the JSON against `schema/federated-source.schema.json`, assert `access.mode == "codex-native"`, assert the only executable is `codex`, and reject an install command that targets the archived Git repository.

- [x] **Step 2: Add a homepage source-routing test**

Require `source-router`, `official-directory`, verified loading of `federated-sources.json`, copy-command fallback, the cachebuster `20260817a`, and wording that the official directory is provided by the local Codex installation.

- [x] **Step 3: Run the focused tests and confirm failure**

Run: `.venv/bin/python -m unittest tests.test_catalog.CatalogTests.test_build_writes_federated_source_descriptor tests.test_catalog.CatalogTests.test_homepage_explains_two_plugin_sources -v`

Expected: both fail because no federation descriptor or source router exists.

### Task 2: Add a strict, non-mirroring federation descriptor

**Files:**
- Create: `schema/federated-source.schema.json`
- Create: `catalog/federated/codex-official.json`
- Modify: `scripts/validate_catalog.py`
- Modify: `scripts/build.py`

- [x] **Step 1: Define the schema**

The schema must require a single source with `id`, Chinese name, official publisher, `access`, `provenance`, `featured_plugins`, and `boundaries`. `access.mode` is fixed to `codex-native`; the command is fixed to executable `codex` with argument array `plugin list --available --json`. `provenance.historical_repository_status` is fixed to `archived`; the descriptor must never contain a Git marketplace-add command.

- [x] **Step 2: Add reviewed source metadata**

Record `openai-curated-remote` and `openai-api-curated` as observed native marketplace IDs, feature a small practical set (GitHub, Figma, Notion, Google Drive, Vercel, Slack, Supabase, Zotero), state that availability depends on the user's Codex product/account, and preserve the archived repository URL only as provenance.

- [x] **Step 3: Validate and build verified copies**

Add `federated_source_errors()` to schema-validate the source document and enforce no credentials, no `marketplace add`, no mutable plugin count, and no non-Codex executable. Extend `build()` to serialize the validated source document deterministically, write SHA-256 sidecars, and copy both files into `site/`.

- [x] **Step 4: Run focused tests**

Run the two Task 1 tests. Expected: federation build passes; homepage test still fails.

### Task 3: Build the two-source routing experience

**Files:**
- Modify: `site/index.html`
- Modify: `site/assets/app.js`
- Modify: `site/assets/styles.css`

- [x] **Step 1: Add semantic source router markup**

Place a `section.source-router` between hero and catalog with one heading, two source lanes, a live status region, a featured-plugin list, an official command preview, and a real button `#copy-official-command`. Keep the Baomiao lane linked to the existing import section; label the official lane “由本机 Codex 提供”.

- [x] **Step 2: Load and verify federation metadata**

Use the existing `fetchVerifiedJson()` helper to fetch `federated-sources.json` and its digest. Validate the fixed source ID, native access mode, executable, exact read-only list arguments, archived-history marker, HTTPS docs URL, and nonempty featured list before rendering.

- [x] **Step 3: Add copy fallback and failure state**

Refactor clipboard handling into a reusable helper. The official button copies only `codex plugin list --available --json`; on failure, keep the Baomiao catalog usable and say the native directory can still be opened from Codex Plugins.

- [x] **Step 4: Style and make responsive**

Extend the existing tokens with an official blue tint, create a two-lane router with a single route rail, preserve AA contrast and 44px controls, stack at 680px, and keep reduced-motion behavior.

### Task 4: Record the source decision and update delivery truth

**Files:**
- Create: `docs/decisions/0011-codex-native-official-directory.md`
- Create: `docs/reviews/openai-official-directory-2026-08-17.md`
- Modify: `docs/client-contract.md`
- Modify: `README.md`
- Modify: `outputs/DELIVERY.md`

- [x] **Step 1: Record the archive finding**

Document that `openai/plugins` was archived on 2026-08-16, its 180-entry snapshot is historical, the native remote directory is reserved and account-dependent, and Baomiao will not clone or rebrand it.

- [x] **Step 2: Extend the client boundary**

Specify that the client asks the user's trusted `codex.exe` for available plugins, accepts native source IDs returned by Codex, never intercepts authentication, never uploads the result, and does not fall back to the archived repository.

- [x] **Step 3: Refresh delivery facts**

Change the stale 26/26 test claim to the actual total after implementation and clarify that prior browser evidence predates the redesigned source router.

### Task 5: Verify and review

**Files:**
- Modify: `docs/superpowers/plans/2026-08-17-federated-official-directory.md`

- [x] **Step 1: Run all deterministic checks**

Run `node --check site/assets/app.js`, `.venv/bin/python -m unittest discover -s tests -v`, `.venv/bin/python -m scripts.validate_catalog`, a fixed-time build, and `git diff --check`.

- [x] **Step 2: Ask DeepSeek Harness for a read-only adversarial review**

Review source truthfulness, archived-upstream handling, client security boundaries, and UI ambiguity. Verify useful findings locally before applying them. The isolated runtime checks passed, but the bounded one-off review returned no substantive result before termination; no conclusion is attributed to DeepSeek.

- [x] **Step 3: Perform browser verification when the local URL policy permits**

Check 320/768/1024/1440 widths, keyboard focus, source status, copy feedback, catalog search, and console errors. If the in-app browser again blocks the local URL, record that limitation and do not use another browser surface to bypass it.

- [x] **Step 4: Commit the reviewed changes**

Stage only this feature's files and commit with `feat: add Codex official directory federation`.

import copy
import hashlib
import json
import tempfile
from pathlib import Path
from unittest import TestCase

from jsonschema import Draft202012Validator, FormatChecker

from scripts.build import build
from scripts.validate_catalog import ROOT, marketplace_errors, semantic_errors, validate_all


class CatalogTests(TestCase):
    def setUp(self):
        approved = sorted((ROOT / "catalog" / "approved").glob("*.json"))
        self.sample = json.loads(approved[0].read_text(encoding="utf-8")) if approved else {}

    def test_approved_catalog_is_valid(self):
        self.assertEqual(validate_all(), [])

    def test_candidate_status_cannot_publish(self):
        entry = copy.deepcopy(self.sample)
        entry["review"]["status"] = "candidate"
        self.assertIn("公开目录只接受 approved 条目", semantic_errors(Path(f"{entry['id']}.json"), entry))

    def test_floating_ref_fails_schema(self):
        with tempfile.TemporaryDirectory() as temp:
            temp_path = Path(temp)
            (temp_path / "schema").mkdir()
            (temp_path / "docs" / "reviews").mkdir(parents=True)
            (temp_path / "schema" / "skill.schema.json").write_text(
                (ROOT / "schema" / "skill.schema.json").read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            entry = copy.deepcopy(self.sample)
            entry["source"]["commit"] = "main"
            (temp_path / "docs" / "reviews" / "x.md").write_text("ok", encoding="utf-8")
            entry["review"]["evidence"] = "docs/reviews/x.md"
            approved = temp_path / "approved"
            approved.mkdir()
            (approved / f"{entry['id']}.json").write_text(json.dumps(entry), encoding="utf-8")
            self.assertTrue(validate_all(approved, root=temp_path))

    def test_build_is_reproducible_with_fixed_time(self):
        first, _ = build(generated_at="2026-08-13T00:00:00Z")
        payload_one = first.read_bytes()
        payload = json.loads(payload_one)
        self.assertEqual(len(payload["entries"]), 77)
        self.assertEqual(sum(1 for entry in payload["entries"] for file in entry["integrity"]["files"] if file["path"].endswith("SKILL.md")), 278)
        self.assertTrue(all(entry["install"]["mode"] == "copy-source-directory" for entry in payload["entries"]))
        self.assertTrue(all(entry["integrity"]["files"] for entry in payload["entries"]))
        self.assertTrue(all(entry["integrity"]["algorithm"] == "sha256" for entry in payload["entries"]))
        self.assertTrue(all(entry["integrity"]["file_count"] == len(entry["integrity"]["files"]) for entry in payload["entries"]))
        schema = json.loads((ROOT / "schema" / "skill.schema.json").read_text(encoding="utf-8"))
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        self.assertEqual([error.message for entry in payload["entries"] for error in validator.iter_errors(entry)], [])
        second, _ = build(generated_at="2026-08-13T00:00:00Z")
        self.assertEqual(payload_one, second.read_bytes())

    def test_build_writes_one_click_import_descriptor(self):
        build(
            generated_at="2026-08-14T00:00:00Z",
            marketplace_source="https://github.com/baomiao-ai/codex-plugins",
            marketplace_ref="1234567890abcdef1234567890abcdef12345678",
            public_base_url="https://baomiao-ai.github.io/codex-plugins",
        )
        descriptor_path = ROOT / "site" / "marketplace-import.json"
        digest_path = ROOT / "site" / "marketplace-import.sha256"
        self.assertTrue(descriptor_path.is_file())
        self.assertTrue(digest_path.is_file())
        descriptor = json.loads(descriptor_path.read_text(encoding="utf-8"))
        import_schema = json.loads((ROOT / "schema" / "marketplace-import.schema.json").read_text(encoding="utf-8"))
        self.assertEqual([error.message for error in Draft202012Validator(import_schema).iter_errors(descriptor)], [])
        self.assertEqual(descriptor["schema_version"], 1)
        self.assertEqual(descriptor["marketplace"]["id"], "baomiao-codex")
        self.assertEqual(descriptor["marketplace"]["source"], "https://github.com/baomiao-ai/codex-plugins")
        self.assertEqual(descriptor["marketplace"]["ref"], "1234567890abcdef1234567890abcdef12345678")
        self.assertEqual(descriptor["marketplace"]["manifest_path"], ".agents/plugins/marketplace.json")
        self.assertEqual(descriptor["marketplace"]["plugin_count"], 77)
        self.assertEqual(descriptor["catalog"]["url"], "https://baomiao-ai.github.io/codex-plugins/catalog.json")
        self.assertNotIn("token", json.dumps(descriptor).lower())
        expected_digest = digest_path.read_text(encoding="utf-8").split()[0]
        self.assertEqual(expected_digest, hashlib.sha256(descriptor_path.read_bytes()).hexdigest())

    def test_build_writes_federated_source_descriptor(self):
        build(generated_at="2026-08-17T00:00:00Z")
        dist_path = ROOT / "dist" / "federated-sources.json"
        digest_path = ROOT / "dist" / "federated-sources.sha256"
        site_path = ROOT / "site" / "federated-sources.json"
        site_digest_path = ROOT / "site" / "federated-sources.sha256"
        self.assertTrue(dist_path.is_file())
        self.assertTrue(digest_path.is_file())
        self.assertEqual(dist_path.read_bytes(), site_path.read_bytes())
        self.assertEqual(digest_path.read_bytes(), site_digest_path.read_bytes())
        document = json.loads(dist_path.read_text(encoding="utf-8"))
        schema = json.loads((ROOT / "schema" / "federated-source.schema.json").read_text(encoding="utf-8"))
        self.assertEqual([error.message for error in Draft202012Validator(schema).iter_errors(document)], [])
        source = document["sources"][0]
        self.assertEqual(source["access"]["mode"], "codex-native")
        self.assertEqual(source["access"]["command"]["executable"], "codex")
        self.assertEqual(source["access"]["command"]["args"], ["plugin", "list", "--available", "--json"])
        self.assertEqual(source["provenance"]["historical_repository_status"], "archived")
        serialized = json.dumps(document).lower()
        self.assertNotIn("plugin marketplace add", serialized)
        self.assertNotIn("github.com/openai/plugins.git", serialized)
        expected_digest = digest_path.read_text(encoding="utf-8").split()[0]
        self.assertEqual(expected_digest, hashlib.sha256(dist_path.read_bytes()).hexdigest())

    def test_homepage_has_accessible_import_controls(self):
        html = (ROOT / "site" / "index.html").read_text(encoding="utf-8")
        script = (ROOT / "site" / "assets" / "app.js").read_text(encoding="utf-8")
        self.assertIn('id="open-import"', html)
        self.assertIn('id="import-dialog"', html)
        self.assertIn('id="copy-import-command"', html)
        self.assertIn('id="import-status"', html)
        self.assertIn("function marketplacePasteValue", script)
        self.assertIn("添加插件市场", html + script)
        self.assertIn("复制失败，请在确认框中手动选择", script)
        self.assertNotIn("baomiao://", html + script)
        self.assertIn('event.key === "Escape"', script)
        self.assertNotIn("GITHUB_TOKEN", html + script)

    def test_homepage_verifies_catalog_and_searches_bundle_skills(self):
        script = (ROOT / "site" / "assets" / "app.js").read_text(encoding="utf-8")
        self.assertIn('fetchVerifiedJson("catalog.json", "catalog.sha256"', script)
        self.assertIn("descriptor.catalog.sha256 !== state.catalogDigest", script)
        self.assertIn("expectedCommandArgs", script)
        self.assertIn("function skillNames(entry)", script)
        self.assertIn("segments.length > 1 ? segments.at(-2) : entry.id", script)
        self.assertIn("normalizeSearch", script)
        self.assertIn('"匹配 Skills"', script)

    def test_homepage_uses_product_shell_and_progressive_card_details(self):
        html = (ROOT / "site" / "index.html").read_text(encoding="utf-8")
        css = (ROOT / "site" / "assets" / "styles.css").read_text(encoding="utf-8")
        script = (ROOT / "site" / "assets" / "app.js").read_text(encoding="utf-8")
        self.assertIn('class="hero-shell"', html)
        self.assertIn('class="journey-steps"', html)
        self.assertIn("20260817b", html)
        self.assertIn("--canvas:", css)
        self.assertIn("--surface:", css)
        self.assertIn("--accent:", css)
        self.assertIn('"card-meta"', script)
        self.assertIn('detailsBody.append(facts', script)
        self.assertNotIn("gap: 1px; background: #afbbc8", css)

    def test_homepage_explains_two_plugin_sources(self):
        html = (ROOT / "site" / "index.html").read_text(encoding="utf-8")
        script = (ROOT / "site" / "assets" / "app.js").read_text(encoding="utf-8")
        self.assertIn('class="source-router"', html)
        self.assertIn('id="official-directory"', html)
        self.assertIn('id="copy-official-command"', html)
        self.assertIn("由本机 Codex 提供", html)
        self.assertIn("20260817b", html)
        self.assertIn('fetchVerifiedJson("federated-sources.json", "federated-sources.sha256"', script)
        self.assertIn("codex plugin list --available --json", script)
        self.assertIn("官方目录命令已复制", script)

    def test_pages_release_build_injects_repository_and_fixed_ref(self):
        workflow = (ROOT / ".github" / "workflows" / "pages.yml").read_text(encoding="utf-8")
        self.assertIn('--marketplace-source "https://github.com/${{ github.repository }}"', workflow)
        self.assertIn('--marketplace-ref "${{ github.sha }}"', workflow)
        self.assertIn('--public-base-url "$PUBLIC_BASE_URL"', workflow)
        self.assertIn("BAOMIAO_PAGES_URL", workflow)

    def test_runtime_auth_uses_on_use_policy(self):
        entry = copy.deepcopy(self.sample)
        entry["id"] = "runtime-auth"
        entry["install"]["mode"] = "copy-source-directory"
        entry["install"]["requires_auth"] = True
        entry["risk"]["capabilities"] = ["credentials"]
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / ".agents" / "plugins").mkdir(parents=True)
            marketplace = {
                "name": "baomiao-codex",
                "plugins": [{
                    "name": "runtime-auth",
                    "source": {"source": "local", "path": "./plugins/runtime-auth"},
                    "policy": {"installation": "AVAILABLE", "authentication": "ON_USE"},
                    "category": "Developer Tools",
                }],
            }
            (root / ".agents" / "plugins" / "marketplace.json").write_text(json.dumps(marketplace), encoding="utf-8")
            self.assertEqual(marketplace_errors([(Path("runtime-auth.json"), entry)], root=root), [])

    def test_high_risk_requires_enhanced_confirmation(self):
        entry = copy.deepcopy(self.sample)
        entry["risk"]["level"] = "high"
        entry["risk"]["capabilities"] = ["external-write"]
        errors = semantic_errors(Path(f"{entry['id']}.json"), entry)
        self.assertIn("高风险条目必须启用增强权限确认", errors)
        entry["install"]["preflight"].append("confirm-enhanced-permissions")
        self.assertNotIn("高风险条目必须启用增强权限确认", semantic_errors(Path(f"{entry['id']}.json"), entry))

    def test_source_direct_is_not_required_in_plugin_marketplace(self):
        entry = copy.deepcopy(self.sample)
        entry["install"]["mode"] = "source-direct"
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / ".agents" / "plugins").mkdir(parents=True)
            marketplace = {"name": "baomiao-codex", "plugins": []}
            (root / ".agents" / "plugins" / "marketplace.json").write_text(json.dumps(marketplace), encoding="utf-8")
            self.assertEqual(marketplace_errors([(Path(f"{entry['id']}.json"), entry)], root=root), [])

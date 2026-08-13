import copy
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
            (temp_path / "schema" / "skill.schema.json").write_text((ROOT / "schema" / "skill.schema.json").read_text(), encoding="utf-8")
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
        self.assertTrue(all(entry["integrity"]["files"] for entry in payload["entries"]))
        self.assertTrue(all(entry["integrity"]["algorithm"] == "sha256" for entry in payload["entries"]))
        schema = json.loads((ROOT / "schema" / "skill.schema.json").read_text(encoding="utf-8"))
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        self.assertEqual([error.message for entry in payload["entries"] for error in validator.iter_errors(entry)], [])
        second, _ = build(generated_at="2026-08-13T00:00:00Z")
        self.assertEqual(payload_one, second.read_bytes())

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

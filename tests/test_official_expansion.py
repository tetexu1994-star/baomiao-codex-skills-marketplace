import json
from pathlib import Path
from unittest import TestCase

from scripts.validate_catalog import ROOT


PACKAGE_IDS = {
    "amazon-location-service",
    "aws-amplify",
    "azure-agent-skills",
    "codebase-documentor-for-aws",
    "nvidia-skills",
}

SOURCE_IDS = {
    "appwrite-official",
    "aws-agent-plugins-official",
    "microsoft-agent-skills-official",
    "nvidia-skills-official",
}


class OfficialExpansionTests(TestCase):
    def test_sources_are_candidate_only_and_conservative(self):
        document = json.loads((ROOT / "sources.json").read_text(encoding="utf-8"))
        sources = {source["id"]: source for source in document["sources"]}
        self.assertTrue(SOURCE_IDS.issubset(sources))
        for source_id in SOURCE_IDS:
            source = sources[source_id]
            self.assertRegex(source["repository"], r"^https://github\.com/")
            self.assertEqual(source["policy"], "candidate-only")
            self.assertIn(source["license_scope"], {"repository", "skill-directory"})
            self.assertGreater(source["max_file_bytes"], 0)
            self.assertFalse(source["allow_executable_files"])
            self.assertIn(source["content_kind"], {"plugin-directory", "skill-bundle"})
            self.assertEqual(set(source["allowed_paths"]), set(source["package_ids"]))

    def test_review_and_decision_records_exist(self):
        self.assertTrue((ROOT / "docs/reviews/official-plugin-expansion-2026-08-14.md").is_file())
        self.assertTrue((ROOT / "docs/decisions/0009-federated-official-bundles.md").is_file())

    def test_all_reviewed_packages_are_real_codex_plugins(self):
        market = json.loads((ROOT / ".agents/plugins/marketplace.json").read_text(encoding="utf-8"))
        entries = {entry["name"]: entry for entry in market["plugins"]}
        self.assertTrue(PACKAGE_IDS.issubset(entries))
        for package_id in PACKAGE_IDS:
            plugin_root = ROOT / "plugins" / package_id
            manifest_path = plugin_root / ".codex-plugin" / "plugin.json"
            approved_path = ROOT / "catalog" / "approved" / f"{package_id}.json"
            self.assertTrue(manifest_path.is_file(), package_id)
            self.assertTrue(approved_path.is_file(), package_id)
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            approved = json.loads(approved_path.read_text(encoding="utf-8"))
            self.assertEqual(manifest["name"], package_id)
            self.assertEqual(approved["id"], package_id)
            self.assertEqual(entries[package_id]["source"], {"source": "local", "path": f"./plugins/{package_id}"})
            self.assertTrue(any(path.name == "SKILL.md" for path in (plugin_root / "skills").rglob("SKILL.md")))

    def test_package_sources_are_fixed_and_license_evidence_is_present(self):
        for package_id in PACKAGE_IDS:
            approved = json.loads((ROOT / "catalog" / "approved" / f"{package_id}.json").read_text(encoding="utf-8"))
            self.assertRegex(approved["source"]["commit"], r"^[0-9a-f]{40}$")
            self.assertIn(approved["source"]["layout"], {"plugin-directory", "skill-bundle"})
            candidates = [
                json.loads(path.read_text(encoding="utf-8"))
                for path in (ROOT / "catalog" / "candidates").glob(f"{package_id}-*.json")
            ]
            candidate = next(item for item in candidates if item["commit"] == approved["source"]["commit"])
            self.assertEqual(candidate["scan"]["verdict"], "review-required")
            self.assertRegex(candidate["license_evidence"]["sha256"], r"^[0-9a-f]{64}$")

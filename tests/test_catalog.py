import copy
import json
import tempfile
from pathlib import Path
from unittest import TestCase

from scripts.build import build
from scripts.validate_catalog import ROOT, semantic_errors, validate_all


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
        second, _ = build(generated_at="2026-08-13T00:00:00Z")
        self.assertEqual(payload_one, second.read_bytes())


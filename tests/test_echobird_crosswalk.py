from unittest import TestCase

from scripts.build_echobird_crosswalk import recommendation, relation


class EchobirdCrosswalkTests(TestCase):
    def test_same_id_different_repository_is_not_marked_covered(self):
        ours = {"linear": "https://github.com/openai/skills"}
        self.assertEqual(
            relation("linear", "https://github.com/openai/plugins", ours),
            "同名不同源",
        )

    def test_permissive_bundle_with_license_and_no_executable_is_candidate(self):
        self.assertEqual(
            recommendation("未收录", "MIT", "LICENSE", []),
            ("可进入候选", "许可文件随包，且未发现脚本/可执行文件"),
        )

    def test_unlicensed_bundle_is_held(self):
        status, reason = recommendation("未收录", "UNLICENSED", "", [])
        self.assertEqual(status, "暂不接入")
        self.assertIn("UNLICENSED", reason)

    def test_script_bundle_requires_separate_review(self):
        status, reason = recommendation("未收录", "Apache-2.0", "LICENSE", ["scripts/run.py"])
        self.assertEqual(status, "需单独复核")
        self.assertIn("1 个脚本", reason)

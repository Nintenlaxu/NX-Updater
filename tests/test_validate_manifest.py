import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from validate_manifest import ManifestError, validate  # noqa: E402


class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.sample = json.loads((ROOT / "manifests" / "stable.json").read_text(encoding="utf-8"))

    def test_empty_channel_is_valid(self):
        self.assertTrue(validate(self.sample, "stable"))

    def test_wrong_channel_is_rejected(self):
        with self.assertRaises(ManifestError):
            validate(self.sample, "beta")

    def test_unknown_platform_rejected(self):
        invalid = copy.deepcopy(self.sample)
        invalid["releases"]["mobile"] = {}
        with self.assertRaises(ManifestError):
            validate(invalid)

    def test_invalid_hash_rejected(self):
        invalid = copy.deepcopy(self.sample)
        invalid["generated_at"] = "2026-11-05T12:00:00Z"
        invalid["releases"]["pc-java-windows"] = {
            "version": "1.0.0", "url": "https://example.org/a.zip", "sha256": "bad", "size_bytes": 1234,
            "notes": "prueba", "minimum_updater_version": "0.1.0"
        }
        with self.assertRaises(ManifestError):
            validate(invalid)

    def test_authenticated_url_rejected(self):
        invalid = copy.deepcopy(self.sample)
        invalid["generated_at"] = "2026-11-05T12:00:00Z"
        invalid["releases"]["pc-java-windows"] = {
            "version": "1.0.0", "url": "https://user:password@example.org/a.zip", "sha256": "0" * 64,
            "size_bytes": 1234, "notes": "prueba", "minimum_updater_version": "0.1.0"
        }
        with self.assertRaises(ManifestError):
            validate(invalid)


if __name__ == "__main__":
    unittest.main()

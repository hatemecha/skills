import tempfile
import unittest
from pathlib import Path
from settings import load_settings, save_settings, update_settings


class SettingsTests(unittest.TestCase):
    def test_update_persists_and_preserves_prior_values(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "settings.json"
            save_settings(path, {"theme": "dark"})
            update_settings(path, {"locale": "es"})
            self.assertEqual(load_settings(path), {"theme": "dark", "locale": "es"})


if __name__ == "__main__":
    unittest.main()

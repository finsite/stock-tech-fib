import os
import unittest
from unittest.mock import patch

from app import config_shared


class TestConfigShared(unittest.TestCase):
    @patch.dict(os.environ, {}, clear=True)
    def test_get_config_value_default(self):
        result = config_shared.get_config_value("NON_EXISTENT_KEY", "default")
        self.assertEqual(result, "default")

    @patch.dict(os.environ, {"TEST_BOOL": "true"})
    def test_get_config_bool_true(self):
        self.assertTrue(config_shared.get_config_bool("TEST_BOOL", False))

    @patch.dict(os.environ, {"TEST_BOOL": "false"})
    def test_get_config_bool_false(self):
        self.assertFalse(config_shared.get_config_bool("TEST_BOOL", True))


if __name__ == "__main__":
    unittest.main()

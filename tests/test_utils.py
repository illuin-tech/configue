import os
import unittest

from illuin_config import load_config_from_dict, load_config_from_file, load_config_from_json_file, load_config_from_yaml_file


class MyObject:
    def __init__(self, my_key, my_other_key=None):
        self.my_key = my_key
        self.my_other_key = my_other_key


class TestUtils(unittest.TestCase):
    def test_load_config_from_dict(self):
        config_dict = {
            "my_object": {
                "()": "test_utils.MyObject",
                "my_key": "my_value",
                "my_other_key": {
                    "()": "test_utils.MyObject",
                    "my_key": "my_sub_value",
                },
            }
        }

        config = load_config_from_dict(config_dict)["my_object"]

        self.assertIsInstance(config, MyObject)
        self.assertEqual("my_value", config.my_key)
        self.assertIsInstance(config.my_other_key, MyObject)
        self.assertEqual("my_sub_value", config.my_other_key.my_key)

    def test_load_config_from_yaml_file(self):
        config_file_path = os.path.join(os.path.dirname(__file__), "config.yaml")

        config = load_config_from_yaml_file(config_file_path)["my_object"]

        self.assertIsInstance(config, MyObject)
        self.assertEqual("my_value", config.my_key)
        self.assertIsInstance(config.my_other_key, MyObject)
        self.assertEqual("my_sub_value", config.my_other_key.my_key)

    def test_load_config_from_json_file(self):
        config_file_path = os.path.join(os.path.dirname(__file__), "config.json")

        config = load_config_from_json_file(config_file_path)["my_object"]

        self.assertIsInstance(config, MyObject)
        self.assertEqual("my_value", config.my_key)
        self.assertIsInstance(config.my_other_key, MyObject)
        self.assertEqual("my_sub_value", config.my_other_key.my_key)

    def test_load_config_from_file_with_yaml(self):
        config_file_path = os.path.join(os.path.dirname(__file__), "config.yaml")

        config = load_config_from_file(config_file_path)["my_object"]

        self.assertIsInstance(config, MyObject)
        self.assertEqual("my_value", config.my_key)
        self.assertIsInstance(config.my_other_key, MyObject)
        self.assertEqual("my_sub_value", config.my_other_key.my_key)

    def test_load_config_from_file_with_json(self):
        config_file_path = os.path.join(os.path.dirname(__file__), "config.json")

        config = load_config_from_file(config_file_path)["my_object"]

        self.assertIsInstance(config, MyObject)
        self.assertEqual("my_value", config.my_key)
        self.assertIsInstance(config.my_other_key, MyObject)
        self.assertEqual("my_sub_value", config.my_other_key.my_key)

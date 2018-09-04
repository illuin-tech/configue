import os
import unittest

from illuin_config import load_config_from_dict, load_config_from_file, load_config_from_json_file, \
    load_config_from_yaml_file
from tests.external_module import MyObject


class TestUtils(unittest.TestCase):
    def test_load_config_from_dict(self):
        config_dict = {
            "my_object": {
                "()": "tests.external_module.MyObject",
                "my_key": "my_value",
                "my_other_key": {
                    "()": "tests.external_module.MyObject",
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

    def test_load_path_from_yaml_file(self):
        config_file_path = os.path.join(os.path.dirname(__file__), "config.yaml")

        my_object_keys = load_config_from_yaml_file(config_file_path)["my_object"].my_other_key.my_other_key

        self.assertEqual(os.path.join(os.path.dirname(__file__), "my_path.txt"), my_object_keys["test_path"])

    def test_load_env_from_yaml_file(self):
        os.environ["my_var"] = "my_value"
        config_file_path = os.path.join(os.path.dirname(__file__), "config.yaml")

        my_object_keys = load_config_from_yaml_file(config_file_path)["my_object"].my_other_key.my_other_key

        self.assertEqual("my_value", my_object_keys["test_env1"])
        self.assertEqual("my_value", my_object_keys["test_env2"])
        self.assertEqual("", my_object_keys["test_env3"])
        self.assertEqual("default_value", my_object_keys["test_env4"])
        self.assertEqual("premy_valuepost", my_object_keys["test_env5"])
        self.assertEqual("my_value", my_object_keys["test_env6"])

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

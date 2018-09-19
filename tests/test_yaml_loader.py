import os
import unittest
from unittest.mock import patch

from yaml.constructor import ConstructorError

from illuin_config.yaml_loader import YamlLoader, yaml


class TestYamlLoader(unittest.TestCase):
    def setUp(self):
        os.environ["my_var"] = "my_value"
        os.environ["my_int_var"] = "10"
        os.environ["my_bool_var"] = "false"
        os.environ["file_name"] = "list_config"

        yaml_file_path = os.path.join(os.path.dirname(__file__), "yaml_loader_config.yaml")
        self.yaml_loader = YamlLoader(yaml_file_path)

    def test_load_path_from_yaml_file(self):
        my_object_keys = self.yaml_loader.load()

        self.assertEqual(os.path.join(os.path.dirname(__file__), "my_path.txt"), my_object_keys["test_path1"])
        self.assertEqual(os.path.join(os.path.dirname(__file__), "my_path/my_value.txt"), my_object_keys["test_path2"])

    def test_load_env_from_yaml_file(self):
        my_object_keys = self.yaml_loader.load()

        self.assertEqual("my_value", my_object_keys["test_env1"])
        self.assertEqual("my_value", my_object_keys["test_env2"])
        self.assertIsNone(my_object_keys["test_env3"])
        self.assertEqual("default_value", my_object_keys["test_env4"])
        self.assertEqual("premy_valuepost", my_object_keys["test_env5"])
        self.assertEqual("10", my_object_keys["test_env6"])
        self.assertEqual(10, my_object_keys["test_env7"])
        self.assertFalse(my_object_keys["test_env8"])
        self.assertEqual("pre my_value and 10 post", my_object_keys["test_env9"])

    def test_load_import_from_yaml_file(self):
        my_object_keys = self.yaml_loader.load()

        self.assertEqual(["my_str_value", "my_value"], my_object_keys["test_import_1"])
        self.assertEqual(["my_str_value", "my_value"], my_object_keys["test_import_2"])

    def test_load_recursion_error(self):
        yaml_loader = YamlLoader(os.path.join(os.path.dirname(__file__), "simple_config.yaml"))
        with patch.object(yaml.Loader, "resolve", return_value="!env"), self.assertRaises(ConstructorError):
            yaml_loader.load()

import logging
import unittest

from illuin_config import ConfigLoader
from tests.external_module import MyObject


class TestConfigLoader(unittest.TestCase):
    def test_load_simple_dict(self):
        config_dict = {
            "my_key": "my_value",
            "my_other_key": 1,
            "my_complex_key": {
                "my_sub_key": "my_sub_value"
            },
            "my_list": ["my_first_value", {
                "my_sub_list_key": "my_sub_list_value",
            }],
        }

        config_loader = ConfigLoader(config_dict)
        config = config_loader.config

        self.assertEqual({
            "my_key": "my_value",
            "my_other_key": 1,
            "my_complex_key": {
                "my_sub_key": "my_sub_value"
            },
            "my_list": ["my_first_value", {
                "my_sub_list_key": "my_sub_list_value",
            }],
        }, config)

    def test_load_callable_dict(self):
        config_dict = {
            "my_object": {
                "()": "tests.external_module.MyObject",
                "my_key": "my_value",
                "my_other_key": 1,
            }
        }

        config_loader = ConfigLoader(config_dict)
        config_object = config_loader.config["my_object"]

        self.assertIsInstance(config_object, MyObject)
        self.assertEqual("my_value", config_object.my_key)
        self.assertEqual(1, config_object.my_other_key)

    def test_nested_callable_dict(self):
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

        config_loader = ConfigLoader(config_dict)
        config_object = config_loader.config["my_object"]

        self.assertIsInstance(config_object, MyObject)
        self.assertEqual("my_value", config_object.my_key)
        self.assertIsInstance(config_object.my_other_key, MyObject)
        self.assertEqual("my_sub_value", config_object.my_other_key.my_key)

    def test_escaped_callable_dict(self):
        config_dict = {
            "my_object": {
                "\\()": "tests.external_module.MyObject",
                "my_key": "my_value",
                "my_other_key": {
                    "()": "tests.external_module.MyObject",
                    "my_key": "my_sub_value",
                },
            }
        }

        config_loader = ConfigLoader(config_dict)
        config_object = config_loader.config["my_object"]

        self.assertEqual(config_object["()"], "tests.external_module.MyObject",)
        self.assertEqual("my_value", config_object["my_key"])
        self.assertIsInstance(config_object["my_other_key"], MyObject)
        self.assertEqual("my_sub_value", config_object["my_other_key"].my_key)

    def test_external_variable_loading(self):
        config_dict = {
            "my_key": "ext://logging.INFO"
        }

        config_loader = ConfigLoader(config_dict)

        self.assertEqual(logging.INFO, config_loader.config["my_key"])

    def test_internal_variable_loading(self):
        config_dict = {
            "my_object": {
                "()": "tests.external_module.MyObject",
                "my_key": "my_value",
                "my_other_key": {
                    "()": "tests.external_module.MyObject",
                    "my_key": "my_sub_value",
                },
            },
            "my_other_object": "cfg://my_object"
        }

        config_loader = ConfigLoader(config_dict)
        config_object = config_loader.config["my_other_object"]

        self.assertIsInstance(config_object, MyObject)
        self.assertEqual("my_value", config_object.my_key)
        self.assertIsInstance(config_object.my_other_key, MyObject)
        self.assertEqual("my_sub_value", config_object.my_other_key.my_key)

    def test_list_loading(self):
        config_dict = {
            "my_objects": [{
                "()": "tests.external_module.MyObject",
                "my_key": "my_value",
            }, {
                "()": "tests.external_module.MyObject",
                "my_key": "my_other_value",
            }]
        }

        config_loader = ConfigLoader(config_dict)
        config_objects = config_loader.config["my_objects"]

        self.assertIsInstance(config_objects, list)
        self.assertEqual(2, len(config_objects))
        self.assertIsInstance(config_objects[0], MyObject)
        self.assertIsInstance(config_objects[1], MyObject)
        self.assertEqual("my_value", config_objects[0].my_key)
        self.assertEqual("my_other_value", config_objects[1].my_key)

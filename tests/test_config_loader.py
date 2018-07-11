import logging
import unittest

from illuin_config.config_loader import ConfigLoader


class MyObject:
    def __init__(self, my_key, my_other_key=None):
        self.my_key = my_key
        self.my_other_key = my_other_key


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
                "()": "test_config_loader.MyObject",
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
                "()": "test_config_loader.MyObject",
                "my_key": "my_value",
                "my_other_key": {
                    "()": "test_config_loader.MyObject",
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

    def test_external_variable_loading(self):
        config_dict = {
            "my_key": "ext://logging.INFO"
        }

        config_loader = ConfigLoader(config_dict)

        self.assertEqual(logging.INFO, config_loader.config["my_key"])

    def test_internal_variable_loading(self):
        config_dict = {
            "my_object": {
                "()": "test_config_loader.MyObject",
                "my_key": "my_value",
                "my_other_key": {
                    "()": "test_config_loader.MyObject",
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

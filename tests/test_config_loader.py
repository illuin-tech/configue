import logging
import unittest
from unittest.mock import ANY, patch

from configue import ConfigLoader
from tests.external_module import MyObject, MyObjectMock


class TestConfigLoader(unittest.TestCase):
    def setUp(self) -> None:
        MyObjectMock.reset_mock()

    def tearDown(self) -> None:
        MyObjectMock.reset_mock()

    def test_load_simple_dict(self):
        config_dict = {
            "my_key": "my_value",
            "my_other_key": 1,
            "my_complex_key": {"my_sub_key": "my_sub_value"},
            "my_list": [
                "my_first_value",
                {
                    "my_sub_list_key": "my_sub_list_value",
                },
            ],
        }

        config_loader = ConfigLoader(config_dict)
        config = config_loader.config

        self.assertEqual(
            {
                "my_key": "my_value",
                "my_other_key": 1,
                "my_complex_key": {"my_sub_key": "my_sub_value"},
                "my_list": [
                    "my_first_value",
                    {
                        "my_sub_list_key": "my_sub_list_value",
                    },
                ],
            },
            config,
        )

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

    def test_external_variable_loading(self):
        config_dict = {"my_key": "ext://logging.INFO"}

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
            "my_other_object": "cfg://my_object",
        }

        config_loader = ConfigLoader(config_dict)
        config_object = config_loader.config["my_other_object"]

        self.assertIsInstance(config_object, MyObject)
        self.assertEqual("my_value", config_object.my_key)
        self.assertIsInstance(config_object.my_other_key, MyObject)
        self.assertEqual("my_sub_value", config_object.my_other_key.my_key)

    def test_list_loading(self):
        config_dict = {
            "my_objects": [
                {
                    "()": "tests.external_module.MyObject",
                    "my_key": "my_value",
                },
                {
                    "()": "tests.external_module.MyObject",
                    "my_key": "my_other_value",
                },
            ]
        }

        config_loader = ConfigLoader(config_dict)
        config_objects = config_loader.config["my_objects"]

        self.assertIsInstance(config_objects, list)
        self.assertEqual(2, len(config_objects))
        for item in config_objects:
            self.assertIsInstance(item, MyObject)
        self.assertEqual("my_value", config_objects[0].my_key)
        self.assertEqual("my_other_value", config_objects[1].my_key)

    def test_tuple_loading(self):
        config_dict = {
            "my_objects": (
                {
                    "()": "tests.external_module.MyObject",
                    "my_key": "my_value",
                },
                {
                    "()": "tests.external_module.MyObject",
                    "my_key": "my_other_value",
                },
            )
        }

        config_loader = ConfigLoader(config_dict)
        config_objects = config_loader.config["my_objects"]

        self.assertIsInstance(config_objects, tuple)
        self.assertEqual(2, len(config_objects))
        for item in config_objects:
            self.assertIsInstance(item, MyObject)
        self.assertEqual("my_value", config_objects[0].my_key)
        self.assertEqual("my_other_value", config_objects[1].my_key)

    def test_cfg_convert_get_attribute(self):
        config_dict = {
            "my_object": {
                "()": "tests.external_module.MyObject",
                "my_key": "my_value",
            },
            "my_key": "cfg://my_object.my_key",
        }

        config_loader = ConfigLoader(config_dict)

        self.assertEqual("my_value", config_loader.config["my_key"])

    def test_cfg_convert_get_key(self):
        config_dict = {
            "my_dict": {
                "my_key": "my_value",
            },
            "my_key": "cfg://my_dict.my_key",
        }

        config_loader = ConfigLoader(config_dict)

        self.assertEqual("my_value", config_loader.config["my_key"])

    def test_cfg_convert_get_key_with_index(self):
        config_dict = {
            "my_dict": {
                "my_key": "my_value",
            },
            "my_key": "cfg://my_dict[my_key]",
        }

        config_loader = ConfigLoader(config_dict)

        self.assertEqual("my_value", config_loader.config["my_key"])

    def test_cfg_convert_get_index(self):
        config_dict = {
            "my_list": ["my_value"],
            "my_key": "cfg://my_list[0]",
        }

        config_loader = ConfigLoader(config_dict)

        self.assertEqual("my_value", config_loader.config["my_key"])

    def test_cfg_convert_invalid_pointer_raises_value_error(self):
        config_dict = {
            "my_key": "cfg://",
        }

        config_loader = ConfigLoader(config_dict)

        with self.assertRaises(ValueError):
            _ = config_loader.config["my_key"]

    def test_cfg_convert_invalid_subpointer_raises_value_error(self):
        config_dict = {
            "my_other_key": "123",
            "my_key": "cfg://my_other_key.",
        }

        config_loader = ConfigLoader(config_dict)

        with self.assertRaises(ValueError):
            _ = config_loader.config["my_key"]

    def test_load_dict_with_kwargs(self):
        config_dict = {
            "my_dict": {
                "my_key": "cfg://my_value",
            },
            "my_value": 1,
        }

        config_loader = ConfigLoader(config_dict)
        new_dict = {**config_loader.config["my_dict"]}
        self.assertEqual(1, new_dict["my_key"])

    def test_load_config_loop_works(self):
        config_dict = {
            "my_dict": {
                "my_key": "cfg://my_dict.my_value",
                "my_value": 1,
            },
        }

        config_loader = ConfigLoader(config_dict)
        self.assertEqual(1, config_loader.config["my_dict"]["my_key"])

    @patch("logging.Logger.error")
    def test_init_exception_logs_error(self, mock_error):
        config_dict = {
            "my_object": {
                "()": "unknown_class",
            },
        }
        config_loader = ConfigLoader(config_dict)

        with self.assertRaises(ValueError):
            _ = config_loader.config["my_object"]

        mock_error.assert_called_with(ANY)
        self.assertTrue(mock_error.call_args[0][0].startswith("Could not instantiate unknown_class: ValueError"))

    def test_lazy_loading(self):
        config_dict = {
            "my_object": {
                "()": "tests.external_module.MyObjectMock",
                "my_key": "my_value",
                "my_other_key": 1,
            }
        }

        config_loader = ConfigLoader(config_dict)
        config_object = config_loader.config

        MyObjectMock.assert_not_called()
        my_object = config_object["my_object"]
        MyObjectMock.assert_called_once_with(my_key="my_value", my_other_key=1)
        self.assertIs(my_object, MyObjectMock.return_value)

import unittest
from logging.config import ConvertingDict
from unittest.mock import create_autospec

from illuin_config import ConfigLoader
from illuin_config.converting_mapping import ConvertingMapping


class TestConvertingMapping(unittest.TestCase):
    def setUp(self):
        self.converting_dict = ConvertingDict({"my_key": "my_value"})
        self.configurator = create_autospec(ConfigLoader, spec_set=True)
        self.configurator.convert.return_value = "converted_value"
        self.converting_dict.configurator = self.configurator
        self.converting_mapping = ConvertingMapping(self.converting_dict)

    def test_keys(self):
        self.assertCountEqual(["my_key"], self.converting_mapping.keys())

    def test_values(self):
        self.assertCountEqual(["converted_value"], self.converting_mapping.values())
        self.configurator.convert.assert_called_with("my_value")

    def test_items(self):
        self.assertCountEqual([("my_key", "converted_value")], self.converting_mapping.items())
        self.configurator.convert.assert_called_with("my_value")

    def test_get(self):
        self.assertEqual("converted_value", self.converting_mapping.get("my_key"))
        self.configurator.convert.assert_called_with("my_value")
        self.assertEqual("converted_value", self.converting_mapping.get("unknown_key"))
        self.configurator.convert.assert_called_with(None)

    def test_pop(self):
        self.assertEqual("converted_value", self.converting_mapping.pop("my_key"))
        self.configurator.convert.assert_called_with("my_value")
        self.converting_mapping.pop("my_key")
        self.configurator.convert.assert_called_with(None)

    def test_magic_methods(self):
        self.converting_mapping["my_new_key"] = "my_new_value"
        self.assertEqual("converted_value", self.converting_mapping["my_new_key"])
        self.configurator.convert.assert_called_with("my_new_value")
        with self.assertRaises(KeyError):
            _ = self.converting_mapping["my_unknown_key"]

    def test_iter(self):
        self.assertCountEqual(["my_key"], [key for key in self.converting_mapping])

    def test_contains(self):
        self.assertTrue("my_key" in self.converting_mapping)
        self.assertFalse("my_unknown_key" in self.converting_mapping)

    def test_del(self):
        del self.converting_mapping["my_key"]
        with self.assertRaises(KeyError):
            _ = self.converting_mapping["my_key"]

    def test_eq(self):
        self.assertEqual(ConvertingMapping(self.converting_dict), self.converting_mapping)
        self.assertNotEqual(ConvertingDict(), self.converting_mapping)

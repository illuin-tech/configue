import logging
import os
from unittest import TestCase

import configue
from configue.exceptions import NonCallableError, SubPathNotFound
from tests.external_module import CONSTANT, MyObject


class TestConfigue(TestCase):
    def test_load_file_shares_object_instances(self):
        result = configue.load(self._get_path("test_file_1.yml"), "key1")
        self.assertIs(result["subkey1"], result["subkey4"]["subkey5"])
        self.assertIsInstance(result["subkey1"], dict)
        self.assertIs(result["subkey1"], result["subkey4"]["subkey6"])
        self.assertIs(result["subkey2"], result["subkey4"]["subkey7"])
        self.assertIs(result["subkey2"], result["subkey4"]["subkey8"])
        self.assertIsInstance(result["subkey2"], MyObject)
        self.assertIs(result["subkey3"], result["subkey4"]["subkey9"])
        self.assertIs(result["subkey3"], result["subkey4"]["subkey10"])
        self.assertIsInstance(result["subkey3"], list)

    def test_load_deep_path(self):
        result = configue.load(self._get_path("test_file_1.yml"), "key1.subkey3.1")
        self.assertEqual("item2", result)

    def test_load_list_path(self):
        result = configue.load(self._get_path("test_file_1.yml"), ["key1", "sub.key.5"])
        self.assertEqual("final_value", result)

    def test_load_with_env_vars(self):
        result = configue.load(self._get_path("test_file_1.yml"), "env")
        self.assertEqual(
            {
                "env_key1": None,
                "env_key2": None,
                "env_key3": "",
                "env_key4": None,
                "env_key5": "default-value",
                "env_key6": 123,
                "env_key7": "123",
                "env_key8": "prepost",
                "env_key9": None,
                "env_key10": None,
            },
            result,
        )
        os.environ["ENV_VAR"] = "my_value"
        result = configue.load(self._get_path("test_file_1.yml"), "env")
        self.assertEqual(
            {
                "env_key1": "my_value",
                "env_key2": "my_value",
                "env_key3": "my_value",
                "env_key4": "my_value",
                "env_key5": "my_value",
                "env_key6": "my_value",
                "env_key7": "my_value",
                "env_key8": "premy_valuepost",
                "env_key9": "my_value",
                "env_key10": "my_value",
            },
            result,
        )
        os.environ["ENV_VAR"] = "321"
        result = configue.load(self._get_path("test_file_1.yml"), "env")
        self.assertEqual(
            {
                "env_key1": 321,
                "env_key2": 321,
                "env_key3": "321",
                "env_key4": 321,
                "env_key5": 321,
                "env_key6": 321,
                "env_key7": "321",
                "env_key8": "pre321post",
                "env_key9": 321,
                "env_key10": 321,
            },
            result,
        )

    def test_load_with_imports(self):
        os.environ["ENV_VAR"] = "test_file_1"
        result = configue.load(self._get_path("test_file_2.yml"), "key1")
        self.assertIs(result["value1"], result["value2"])
        self.assertIs(result["value1"], result["value3"])
        self.assertEqual("other_value", result["value1"]["key1"]["subkey1"]["other_key"])
        self.assertEqual("other_value", result["value4"]["other_key"])

    def test_load_without_path(self):
        result = configue.load(self._get_path("test_file_1.yml"))
        self.assertCountEqual(["key1", "key2", "env"], result.keys())

    def test_load_with_invalid_class_raises_exception(self):
        with self.assertRaises(NonCallableError):
            configue.load(self._get_path("test_file_2.yml"), "invalid_class")

    def test_load_invalid_subpath_raises_exception(self):
        with self.assertRaises(SubPathNotFound):
            configue.load(self._get_path("test_file_1.yml"), "key1.subkey1.other_key.unknown_key")

        with self.assertRaises(SubPathNotFound):
            configue.load(self._get_path("test_file_1.yml"), "key1.subkey1.unknown_key")

        with self.assertRaises(SubPathNotFound):
            configue.load(self._get_path("test_file_1.yml"), "key1.subkey3.3")

        with self.assertRaises(SubPathNotFound):
            configue.load(self._get_path("test_file_1.yml"), "key1.subkey3.unknown_key")

    def test_load_invalid_import_raises_exception(self):
        with self.assertRaises(SubPathNotFound):
            configue.load(self._get_path("test_file_2.yml"), "invalid_import")

    def test_load_external_value(self):
        result = configue.load(self._get_path("test_file_2.yml"), "const")
        self.assertEqual(CONSTANT, result)

    def test_null_path(self):
        result = configue.load(self._get_path("test_file_2.yml"), "paths")
        self.assertIsNone(result["path"])
        self.assertEqual(os.path.expanduser("~"), result["path2"])
        self.assertIsNone(result["path3"])

    def test_logging_config(self):
        configue.load(self._get_path("test_file_2.yml"), "const", logging_config_path="logging_config")
        logger = logging.getLogger("test.path")
        self.assertEqual(logging.DEBUG, logger.handlers[0].level)
        self.assertEqual(logging.ERROR, logger.handlers[1].level)

    @staticmethod
    def _get_path(file_name: str) -> str:
        return os.path.join(os.path.dirname(__file__), file_name)

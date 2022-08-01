from typing import Any, List, Union

from .root_loader import RootLoader


def load(file_path: str, sub_path: Union[str, List[str]] = "", *, logging_config_path: str = None) -> Any:
    """Load configuration from a YAML file.

    :param file_path: Absolute path to the YAML file containing the configuration
    :param sub_path: path inside the YAML file to load. List elements are noted as 0-based indexes.
    :param logging_config_path: path inside the YAML file that contains the logging configuration.
    The format is the same as logging.dictConfig():
    https://docs.python.org/3/library/logging.config.html#logging-config-dictschema
    :return: the converting dict corresponding to the file.

    Taking this file as an example:

    top_level_key:
      first_level: some_value
      other_key: 123
      some.dotted.key: dotted.value
      some_list:
        - item_key: item_value
          other_item_key: false
        - second_key: ~


    Loading the default sub_path (empty string) will return the whole object
    {
        "top_level_key": {
            "first_level": "some_value",
            "other_key": 123,
            "some.dotted.key": "dotted.value",
            "some_list": [{
                "item_key": "item_value",
                "other_item_key": False,
            }, {
                "second_key": None,
            }]
        }
    }

    Loading the sub_path "top_level_key.first_level" will return "some_value".
    Loading the sub_path "top_level_key.some_list.0" will return
    {
        "item_key": "item_value",
        "other_item_key": False,
    }
    Loading the sub_path ["top_level_key", "some.dotted.key"] will return "dotted.value"
    """

    return RootLoader(file_path).load_root_file(sub_path, logging_config_path)

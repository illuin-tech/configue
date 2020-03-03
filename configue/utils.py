from typing import Any, Dict

from configue.yaml_loader import YamlLoader
from .config_loader import ConfigLoader


def load_config_from_dict(config_dict: Dict) -> Any:
    """Load configuration from a dictionary.

    :param config_dict: the dictionary to parse
    :return: the converting dict corresponding to config_dict.
    """

    return ConfigLoader(config_dict).config


def load_config_from_file(file_path: str) -> Any:
    """Load configuration from a YAML file.

    :param file_path: Absolute path to the YAML file containing the configuration
    :return: the converting dict corresponding to the file.
    """

    config = YamlLoader(file_path).load()
    return load_config_from_dict(config)

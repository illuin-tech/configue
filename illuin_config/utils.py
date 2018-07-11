import json
from logging.config import ConvertingDict
from typing import Dict

import yaml

from illuin_config.config_loader import ConfigLoader


def load_config_from_dict(config_dict: Dict) -> ConvertingDict:
    """Load configuration from a dictionary.

    :param config_dict: the dictionary to parse
    :return: the converting dict corresponding to config_dict.
    """

    return ConfigLoader(config_dict).config


def load_config_from_yaml_file(file_path: str) -> ConvertingDict:
    """Load configuration from a YAML file.

    :param file_path: Absolute path to the YAML file containing the configuration
    :return: the converting dict corresponding to the file.
    """

    with open(file_path, "r", encoding="utf-8") as config_file:
        config_dict = yaml.load(config_file)

    return load_config_from_dict(config_dict)


def load_config_from_json_file(file_path: str) -> ConvertingDict:
    """Load configuration from a JSON file.

    :param file_path: Absolute path to the JSON file containing the configuration
    :return: the converting dict corresponding to the file.
    """
    with open(file_path, "r", encoding="utf-8") as config_file:
        config_dict = json.load(config_file)

    return load_config_from_dict(config_dict)


def load_config_from_file(file_path: str) -> ConvertingDict:
    """Load configuration from a YAML or a JSON file.

    The file must have a '.json' or a '.yaml' extension.

    :param file_path: Absolute path to the file containing the configuration
    :return: the converting dict corresponding to the file.
    """
    if file_path.endswith(".json"):
        return load_config_from_json_file(file_path)
    return load_config_from_yaml_file(file_path)

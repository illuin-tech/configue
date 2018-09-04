import json
import os
import re
import warnings
from logging.config import ConvertingDict
from typing import Dict

import yaml

from .config_loader import ConfigLoader


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
    # Matches "prefix${myvar-default}suffix" -> "prefix", "myvar", "default", "suffix"
    # or "${myvar}" -> "", "myvar", "", ""

    _env_pattern_regex = re.compile(r"^([^$]*)\${([^-}]*)-?([^}]*)}(.*)$")

    def yaml_env_constructor(loader: yaml.Loader, node: yaml.Node) -> str:
        value: str = loader.construct_scalar(node)
        prefix, env_var_name, default_value, suffix = _env_pattern_regex.match(value).group(1, 2, 3, 4)
        return f"{prefix}{os.environ.get(env_var_name, default_value)}{suffix}"

    yaml.add_implicit_resolver("!env", _env_pattern_regex)
    yaml.add_constructor("!env", yaml_env_constructor)

    def yaml_path_constructor(loader: yaml.Loader, node: yaml.Node) -> str:
        value = loader.construct_scalar(node)
        return os.path.join(os.path.dirname(file_path), value)

    yaml.add_constructor("!path", yaml_path_constructor)

    with open(file_path, "r", encoding="utf-8") as config_file:
        config_dict = yaml.load(config_file)

    return load_config_from_dict(config_dict)


def load_config_from_json_file(file_path: str) -> ConvertingDict:
    """(Deprecated) Load configuration from a JSON file.

    :param file_path: Absolute path to the JSON file containing the configuration
    :return: the converting dict corresponding to the file.
    """
    warnings.warn("Loading configuration from a JSON file is deprecated, use a YAML file instead", DeprecationWarning)

    with open(file_path, "r", encoding="utf-8") as config_file:
        config_dict = json.load(config_file)

    return load_config_from_dict(config_dict)


def load_config_from_file(file_path: str) -> ConvertingDict:
    """Load configuration from a YAML or a JSON (deprecated) file.

    The file must have a '.json' or a '.yml' extension.

    :param file_path: Absolute path to the file containing the configuration
    :return: the converting dict corresponding to the file.
    """
    if file_path.endswith(".json"):
        return load_config_from_json_file(file_path)
    return load_config_from_yaml_file(file_path)

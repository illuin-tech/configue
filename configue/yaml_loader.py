import logging
import os
import re
from typing import Any

import yaml


class YamlLoader:
    logger = logging.getLogger(__name__)

    def __init__(self, file_path: str) -> None:
        self._file_path = file_path
        # Matches "${myvar-default}" -> "${", "myvar", "-", "default", "}"
        # or "${myvar}" -> "${", "myvar", "", "", "}"
        self._env_pattern_regex = re.compile(r"(?:(?!\${[^-}]+}).)*(\${)([^-}]+)(-?)([^}]*)(})")
        # Custom loader to bind our constructors without impacting the yaml class or the other instances of YamlLoader
        self._loader = type("Loader", (yaml.FullLoader,), {})

    def load(self) -> Any:
        yaml.add_implicit_resolver("!env", self._env_pattern_regex, Loader=self._loader)
        yaml.add_constructor("!env", self._env_constructor, Loader=self._loader)
        yaml.add_constructor("!path", self._path_constructor, Loader=self._loader)
        yaml.add_constructor("!import", self._import_constructor, Loader=self._loader)
        yaml.add_constructor("!list", self._list_constructor, Loader=self._loader)

        with open(self._file_path, encoding="utf-8") as config_file:
            return yaml.load(config_file, self._loader)

    def _env_constructor(self, loader: yaml.Loader, node: yaml.ScalarNode) -> Any:
        raw_value: str = loader.construct_scalar(node)
        replaced_str = ""
        end_pos = 0
        for match in self._env_pattern_regex.finditer(raw_value):
            env_var_name, has_default, default_value = match.group(2, 3, 4)
            start_pos = match.start(1)
            if env_var_name not in os.environ and not has_default:
                self.logger.warning(f"Missing environment var: '{env_var_name}', no default is set")
            replaced_str += f"{raw_value[end_pos:start_pos]}{os.environ.get(env_var_name, default_value)}"
            end_pos = match.end(5)
        replaced_str += raw_value[end_pos:]
        # Put back quotes
        if node.style == "\"":
            replaced_str = f"\"{replaced_str}\""
        # reload node to cast the value
        return self._get_reloaded_value(replaced_str)

    def _path_constructor(self, loader: yaml.Loader, node: yaml.ScalarNode) -> Any:
        raw_value = loader.construct_scalar(node)
        # reload node to eval environment variables
        new_value = str(self._get_reloaded_value(raw_value))
        expanded_new_value = os.path.expanduser(new_value)
        full_path = os.path.join(os.path.dirname(self._file_path), expanded_new_value)
        return full_path

    def _import_constructor(self, loader: yaml.Loader, node: yaml.ScalarNode) -> Any:
        raw_value = loader.construct_scalar(node)
        # reload node to eval environment variables
        templated_value = str(self._get_reloaded_value(raw_value))
        imported_path = os.path.join(os.path.dirname(self._file_path), templated_value)
        loader = YamlLoader(imported_path)
        return loader.load()

    def _list_constructor(self, loader: yaml.Loader, node: yaml.ScalarNode) -> Any:
        raw_value = loader.construct_scalar(node)
        # reload node to eval environment variables
        new_value = str(self._get_reloaded_value(raw_value))
        split_value = new_value.split(",")
        return split_value

    def _get_reloaded_value(self, str_value: str) -> Any:
        # Reload the value
        return yaml.load(str_value, Loader=self._loader)

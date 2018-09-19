import os
import re
from collections import defaultdict
from typing import Any

import yaml
from yaml.constructor import ConstructorError


class YamlLoader:
    def __init__(self, file_path: str) -> None:
        self._file_path = file_path
        # Matches "${myvar-default}" -> "${", "myvar", "default", "}"
        # or "${myvar}" -> "${", "myvar", "", "}"
        self._env_pattern_regex = re.compile(r"(?:(?!\${[^-}]+}).)*(\${)([^-}]+)-?([^}]*)(})")

    def load(self) -> Any:
        yaml.add_implicit_resolver("!env", self._env_pattern_regex)
        yaml.add_constructor("!env", self._yaml_env_constructor)
        yaml.add_constructor("!path", self._yaml_path_constructor)
        yaml.add_constructor("!import", self._yaml_import_constructor)

        with open(self._file_path) as config_file:
            return yaml.load(config_file)

    def _yaml_env_constructor(self, loader: yaml.Loader, node: yaml.ScalarNode) -> Any:
        raw_value: str = loader.construct_scalar(node)
        replaced_str = ""
        end_pos = 0
        for match in self._env_pattern_regex.finditer(raw_value):
            env_var_name, default_value = match.group(2, 3)
            start_pos = match.start(1)
            replaced_str += f"{raw_value[end_pos:start_pos]}{os.environ.get(env_var_name, default_value)}"
            end_pos = match.end(4)
        replaced_str += raw_value[end_pos:]
        # reload node to cast the value
        return self._get_reloaded_node(loader, replaced_str, node, "env")

    def _yaml_path_constructor(self, loader: yaml.Loader, node: yaml.ScalarNode) -> Any:
        raw_value = loader.construct_scalar(node)
        str_value = os.path.join(os.path.dirname(self._file_path), raw_value)
        # reload node to eval environment variables
        return self._get_reloaded_node(loader, str_value, node, "path")

    def _yaml_import_constructor(self, loader: yaml.Loader, node: yaml.ScalarNode) -> Any:
        raw_value = loader.construct_scalar(node)
        templated_value = str(self._get_reloaded_node(loader, raw_value, node, "import"))
        imported_path = os.path.join(os.path.dirname(self._file_path), templated_value)
        loader = YamlLoader(imported_path)
        return loader.load()

    @staticmethod
    def _get_reloaded_node(loader: yaml.Loader, str_value: str, node: yaml.ScalarNode, constructor_type: str) -> Any:
        # Put back quotes
        quoted_value = str_value
        if node.style == "\"":
            quoted_value = f"\"{str_value}\""
        # Parse the node again to get its tag
        node.tag = loader.resolve(yaml.ScalarNode, quoted_value, implicit=(True, False))
        node.value = str_value

        if not hasattr(loader, "recursive_objects_custom"):
            loader.recursive_objects_custom = defaultdict(set)
        elif constructor_type in loader.recursive_objects_custom[node]:
            raise ConstructorError(None, None, "found unconstructable recursive node", node.start_mark)

        loader.recursive_objects.pop(node)
        loader.recursive_objects_custom[node].add(constructor_type)
        node_value = loader.construct_object(node)
        loader.recursive_objects[node] = None
        loader.recursive_objects_custom[node] = set()
        return node_value

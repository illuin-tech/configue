import logging
import os
import re
from collections.abc import Hashable
from typing import Any, List, Mapping, Union

import yaml
from yaml.constructor import ConstructorError

from configue.exceptions import NonCallableError, NotFoundError

# Matches "${myvar-default}" -> "${", "myvar", "-", "default", "}"
# or "${myvar}" -> "${", "myvar", "", "", "}"
ENV_PATTERN_REGEX = re.compile(r"(\${)(\w+)(-?)((?:(?![^}]*\${)[^}])*)(})")
CONSTRUCTOR_KEY = "()"
ESCAPED_CONSTRUCTOR_KEY = "\\()"


class ConfigueLoader(yaml.FullLoader):  # pylint: disable=too-many-ancestors
    logger = logging.getLogger(__name__)

    def construct_yaml_map(self, node: yaml.MappingNode) -> Any:
        mapping: Mapping[Hashable, Any] = self.construct_mapping(node)
        if isinstance(mapping, dict) and CONSTRUCTOR_KEY in mapping:
            path = mapping.pop(CONSTRUCTOR_KEY)
            object_path_elements = path.split(".")
            remaining_path_elements: List[str] = []
            while object_path_elements:
                try:
                    cls = self.find_python_name(
                        ".".join(object_path_elements),
                        node.start_mark,
                        unsafe=True,
                    )
                    break
                except ConstructorError:
                    remaining_path_elements.insert(0, object_path_elements.pop(-1))
            else:
                raise NotFoundError(f"Could not load element {path} {node.start_mark}")
            for path_element in remaining_path_elements:
                cls = getattr(cls, path_element)

            if not callable(cls):
                raise NonCallableError(
                    f"Error while constructing a Python instance {node.start_mark}, "
                    f"expected a callable but found {type(cls)}"
                )
            return cls(**mapping)
        if isinstance(mapping, dict) and ESCAPED_CONSTRUCTOR_KEY in mapping:
            mapping[CONSTRUCTOR_KEY] = mapping.pop(ESCAPED_CONSTRUCTOR_KEY)
        return mapping

    def construct_scalar(self, node: Union[yaml.ScalarNode, yaml.MappingNode]) -> Any:
        scalar = yaml.FullLoader.construct_scalar(self, node)
        if isinstance(node, yaml.MappingNode):  # pragma: nocover
            return scalar
        replaced_value = ""
        end_pos = 0
        for match in ENV_PATTERN_REGEX.finditer(scalar):
            env_var_name, has_default, default_value = match.group(2, 3, 4)
            start_pos = match.start(1)
            if env_var_name not in os.environ and not has_default:
                self.logger.warning(f"Missing environment var: '{env_var_name}', no default is set")
            replaced_value += f"{scalar[end_pos:start_pos]}{os.environ.get(env_var_name, default_value)}"
            end_pos = match.end(5)
        replaced_value += scalar[end_pos:]
        if replaced_value == node.value:
            return scalar
        if node.style in ["'", '"']:
            replaced_value = f"{node.style}{replaced_value}{node.style}"
        # A variable has been replaced, reload to convert string to number if needed or replace again
        return yaml.load(replaced_value, Loader=self.__class__)

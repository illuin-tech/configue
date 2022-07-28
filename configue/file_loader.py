import logging
import os
from typing import Any, List, Optional, TYPE_CHECKING, Type, Union, cast

from yaml import Loader, MappingNode, Node, ScalarNode, SequenceNode

from .configue_loader import ConfigueLoader
from .exceptions import SubPathNotFound

if TYPE_CHECKING:
    from .root_loader import RootLoader


class FileLoader:
    logger = logging.getLogger(__name__)

    def __init__(self, file_path: str, root_loader: "RootLoader") -> None:
        self._file_path = file_path
        self._root_loader = root_loader

        loader_cls: Type[Loader] = cast(
            Type[Loader],
            type("CustomLoader", (ConfigueLoader,), {"yaml_loader": self}),
        )

        loader_cls.add_multi_constructor("!import", self._load_import)
        loader_cls.add_constructor("!path", self._load_path)
        loader_cls.add_constructor("!cfg", self._load_cfg)
        loader_cls.add_constructor("!ext", self._load_ext)
        loader_cls.add_constructor("tag:yaml.org,2002:map", loader_cls.construct_yaml_map)

        with open(self._file_path, encoding="utf-8") as config_file:
            self._loader = loader_cls(config_file)
            self._root_node = self._loader.get_single_node()
        self._loader.dispose()

    def load(self, path: Union[str, List[str]]) -> Any:
        if isinstance(path, str):
            path = path.split(".")

        current_node = self._root_node
        for sub_path in path:
            if not sub_path:
                continue
            current_node = self._get_node_at_sub_path(sub_path, current_node)
        return self._loader.construct_object(current_node, deep=True)

    @staticmethod
    def _get_node_at_sub_path(sub_path: str, current_node: Node) -> Node:
        if isinstance(current_node, SequenceNode):
            try:
                sub_path = int(sub_path)
            except ValueError:
                raise SubPathNotFound(
                    f"Could not convert sub_path element {sub_path} to list index {current_node.start_mark}"
                ) from None
            try:
                return current_node.value[sub_path]
            except IndexError:
                raise SubPathNotFound(
                    f"Could not find sub_path element {sub_path} in list {current_node.start_mark}"
                ) from None
        elif isinstance(current_node, MappingNode):
            for node_key, node_value in current_node.value:
                if isinstance(node_key, ScalarNode) and str(node_key.value) == sub_path:
                    return node_value
            raise SubPathNotFound(f"Could not find sub_path {sub_path} {current_node.start_mark}")
        raise SubPathNotFound(f"Could not find sub_path element {sub_path} {current_node.start_mark}")

    def _load_import(self, loader: ConfigueLoader, tag_suffix: str, node: ScalarNode) -> Any:
        path = self._load_path(loader, node)
        return self._root_loader.load_file(path, tag_suffix[1:])

    def _load_path(self, loader: ConfigueLoader, node: ScalarNode) -> Optional[str]:
        raw_path = loader.construct_scalar(node)
        if raw_path is None:
            return None
        path = os.path.expanduser(raw_path)
        return os.path.join(os.path.dirname(self._file_path), path)

    def _load_cfg(self, loader: ConfigueLoader, node: ScalarNode) -> Any:
        path = loader.construct_scalar(node)
        return self.load(path)

    @staticmethod
    def _load_ext(loader: ConfigueLoader, node: ScalarNode) -> Any:
        path = loader.construct_scalar(node)
        return loader.find_python_name(path, node.start_mark, unsafe=True)

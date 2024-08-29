import logging
import os
from typing import Any, List, Optional, TYPE_CHECKING, Type, Union, cast

from yaml import Loader, MappingNode, Node, ScalarNode, SequenceNode
from yaml.constructor import ConstructorError

from .configue_loader import ConfigueLoader
from .exceptions import SubPathNotFound, InvalidNodeType, NotFoundError

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

        loader_cls.add_multi_constructor("!import", self._load_import)  # type: ignore[no-untyped-call]
        loader_cls.add_constructor("!path", self._load_path)
        loader_cls.add_constructor("!cfg", self._load_cfg)
        loader_cls.add_constructor("!ext", self._load_ext)
        loader_cls.add_constructor("tag:yaml.org,2002:map", loader_cls.construct_yaml_map)  # type: ignore[type-var]

        with open(self._file_path, encoding="utf-8") as config_file:
            self._loader = loader_cls(config_file)
            self._root_node = self._loader.get_single_node()
        self._loader.dispose()  # type: ignore[no-untyped-call]

    def load(self, path: Union[str, List[str]]) -> Any:
        if self._root_node is None:
            return None

        if isinstance(path, str):
            path = path.split(".")

        current_node = self._root_node
        is_current_node_loaded = False
        for sub_path in path:
            if not sub_path:
                continue
            if not is_current_node_loaded:
                try:
                    current_node = self._get_node_at_sub_path(sub_path, current_node)
                except InvalidNodeType:
                    current_node = self._loader.construct_object(  # type: ignore[no-untyped-call]
                        current_node,
                        deep=True,
                    )
                    is_current_node_loaded = True
            if is_current_node_loaded:
                current_node = self._get_element_at_sub_path(sub_path, current_node)
        if is_current_node_loaded:
            return current_node
        return self._loader.construct_object(current_node, deep=True)  # type: ignore[no-untyped-call]

    @staticmethod
    def _get_node_at_sub_path(sub_path: str, current_node: Node) -> Node:
        if isinstance(current_node, SequenceNode):
            try:
                sub_path_index = int(sub_path)
            except ValueError:
                raise SubPathNotFound(
                    f"Could not convert sub_path element {sub_path} to list index {current_node.start_mark}"
                ) from None
            try:
                return cast(Node, current_node.value[sub_path_index])
            except IndexError:
                raise SubPathNotFound(
                    f"Could not find sub_path element {sub_path_index} in list {current_node.start_mark}"
                ) from None
        elif isinstance(current_node, MappingNode):
            for node_key, node_value in current_node.value:
                if isinstance(node_key, ScalarNode) and str(node_key.value) == sub_path:
                    return cast(Node, node_value)
            raise SubPathNotFound(f"Could not find sub_path {sub_path} {current_node.start_mark}")
        raise InvalidNodeType()

    @staticmethod
    def _get_element_at_sub_path(sub_path: str, current_element: Any) -> Any:
        try:
            sub_path_index: Union[str, int] = int(sub_path)
        except ValueError:
            sub_path_index = sub_path
        try:
            return current_element[sub_path_index]
        except TypeError:
            pass
        try:
            return getattr(current_element, sub_path)
        except AttributeError:
            raise SubPathNotFound(f"Could not find sub_path {sub_path} in {current_element}") from None

    def _load_import(self, loader: ConfigueLoader, tag_suffix: str, node: ScalarNode) -> Any:
        path = self._load_path(loader, node)
        if path is None:
            return None
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

    def _load_ext(self, loader: ConfigueLoader, node: ScalarNode) -> Any:
        path = loader.construct_scalar(node)
        object_path_elements = path.split(".")
        remaining_path_elements: List[str] = []
        while object_path_elements:
            try:
                loaded_object = loader.find_python_name(
                    ".".join(object_path_elements),
                    node.start_mark,
                    unsafe=True,
                )
                break
            except ConstructorError:
                remaining_path_elements.insert(0, object_path_elements.pop(-1))
        else:
            raise NotFoundError(f"Could not load element {path} {node.start_mark}")
        remaining_path = ".".join(remaining_path_elements)
        if remaining_path:
            return self._get_element_at_sub_path(remaining_path, loaded_object)
        return loaded_object

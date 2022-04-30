import logging
from typing import Any, Dict, List, Union

from .file_loader import FileLoader


class RootLoader:
    logger = logging.getLogger(__name__)

    def __init__(self, file_path: str) -> None:
        self._root_file = file_path
        self._file_loaders_by_file: Dict[str, FileLoader] = {}

    def load_root_file(self, sub_path: Union[str, List[str]]) -> Any:
        return self.load_file(self._root_file, sub_path)

    def load_file(self, file_path: str, sub_path: Union[str, List[str]]) -> Any:
        if file_path not in self._file_loaders_by_file:
            self._file_loaders_by_file[file_path] = FileLoader(file_path, self)
        return self._file_loaders_by_file[file_path].load(sub_path)

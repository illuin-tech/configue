import logging
import logging.config
from typing import Any, Dict, List, Optional, Union

from .file_loader import FileLoader


class RootLoader:
    logger = logging.getLogger(__name__)

    def __init__(self, file_path: str) -> None:
        self._root_file = file_path
        self._file_loaders_by_file: Dict[str, FileLoader] = {}

    def load_root_file(self, sub_path: Union[str, List[str]], logging_config_path: Optional[str]) -> Any:
        if logging_config_path is not None:
            self._load_logging_config(logging_config_path)
        return self.load_file(self._root_file, sub_path)

    def _load_logging_config(self, logging_config_path: str) -> None:
        logging.captureWarnings(True)
        logging_config = self.load_file(self._root_file, logging_config_path)
        logging.config.dictConfig(logging_config)

    def load_file(self, file_path: str, sub_path: Union[str, List[str]]) -> Any:
        if file_path not in self._file_loaders_by_file:
            self._file_loaders_by_file[file_path] = FileLoader(file_path, self)
        return self._file_loaders_by_file[file_path].load(sub_path)

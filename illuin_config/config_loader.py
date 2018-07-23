from logging.config import BaseConfigurator, ConvertingDict, ConvertingList
from typing import Any, Dict


class ConfigLoader(BaseConfigurator):
    """A configurator based on logging.config.

    Can instantiate classes from a configuration dictionary.
    The instantiation happens when the object is fetched from the configuration.

    :ivar config: The parsed configuration.
    """

    def __init__(self, config_dict: Dict) -> None:
        self._config: ConvertingDict = None
        BaseConfigurator.__init__(self, config_dict)

    @property
    def config(self) -> ConvertingDict:
        return self._config

    @config.setter
    def config(self, config: ConvertingDict) -> None:
        self._config = config

    def convert(self, value: Any) -> Any:
        value = BaseConfigurator.convert(self, value)
        if isinstance(value, ConvertingDict):
            if "()" in value:
                return self.configure_custom(value)
            if "\\()" in value:
                value["()"] = value.pop("\\()")
        if isinstance(value, ConvertingList):
            value = list(map(self.convert, value))
        return value

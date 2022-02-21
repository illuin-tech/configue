import logging
from logging.config import BaseConfigurator, ConvertingDict, ConvertingList, ConvertingTuple
from typing import Any, Dict, Tuple, Optional

from configue.converting_mapping import ConvertingMapping


class ConfigLoader(BaseConfigurator):
    """A configurator based on logging.config.

    Can instantiate classes from a configuration dictionary.
    The instantiation happens when the object is fetched from the configuration.

    :ivar config: The parsed configuration.
    """

    logger = logging.getLogger(__name__)

    def __init__(self, config_dict: Dict) -> None:
        self._config: Optional[ConvertingDict] = None
        BaseConfigurator.__init__(self, config_dict)
        self.config = self.convert(self.config)

    @property
    def config(self) -> Any:
        return self._config

    @config.setter
    def config(self, config: ConvertingDict) -> None:
        self._config = config

    def convert(self, value: Any) -> Any:
        value = BaseConfigurator.convert(self, value)
        if isinstance(value, ConvertingDict):
            value = ConvertingMapping(value)
            if "()" in value:
                cls_path = value["()"]
                try:
                    return self.configure_custom(value)
                except Exception as error:
                    self.logger.error(f"Could not instantiate {cls_path}: {error!r}")
                    raise
        elif isinstance(value, ConvertingList):
            value = list(map(self.convert, value))
        elif isinstance(value, ConvertingTuple):
            value = tuple(map(self.convert, value))
        return value

    def cfg_convert(self, value: str) -> Any:
        """Default converter for the cfg:// protocol."""

        str_to_parse = value
        match = self.WORD_PATTERN.match(str_to_parse)
        if match is None:
            raise ValueError(f"Unable to convert {value!r}")
        str_to_parse = str_to_parse[match.end() :]
        parsed_object = self.config[match.groups()[0]]
        while str_to_parse:
            parsed_object, str_to_parse = self._parse_next_cfg_level(parsed_object, str_to_parse)
        return parsed_object

    def _parse_next_cfg_level(self, parsed_object: Any, str_to_parse: str) -> Tuple[Any, str]:
        match = self.DOT_PATTERN.match(str_to_parse)  # parsed_object.property
        if match:
            remaining_str: str = str_to_parse[match.end() :]
            if not isinstance(parsed_object, (dict, ConvertingMapping)):
                return getattr(parsed_object, match.groups()[0]), remaining_str
            return parsed_object[match.groups()[0]], remaining_str
        match = self.INDEX_PATTERN.match(str_to_parse)  # parsed_object[property]
        if not match:
            raise ValueError(f"Unable to convert {str_to_parse!r}")
        remaining_str = str_to_parse[match.end() :]
        idx = match.groups()[0]
        if not self.DIGIT_PATTERN.match(idx):  # parsed_object["property"]
            return parsed_object[idx], remaining_str
        return parsed_object[int(idx)], remaining_str  # parsed_object[0]

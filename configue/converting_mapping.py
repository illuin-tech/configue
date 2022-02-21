from collections.abc import MutableMapping
from logging.config import ConvertingDict, ConvertingMixin
from typing import Any, ItemsView, Iterator, Optional, ValuesView


class ConvertingMapping(MutableMapping, ConvertingMixin):
    """Similar to ConvertingDict without inheriting from dict, to allow **kwargs unpacking override.

    When using **kwargs, __getitem__ is called on the unpacked object unless it is a dict instance, due to an internal
    optimization.
    To convert the dict values on keyword unpacking, we have to use a class that does not inherit from dict.
    Copies all ConvertingDict methods to be able to replace it seamlessly in functions that expect ConvertingDict
    instances.
    """

    def __init__(self, converting_dict: ConvertingDict):
        self._dict = converting_dict

    __doc__ = dict.__doc__

    __hash__ = dict.__hash__

    def __getattr__(self, item: Any) -> Any:
        """Access methods from ConvertingDict such as update(), keys(), convert()..."""

        return getattr(self._dict, item)

    def get(self, key: Any, default: Any = None) -> Optional[Any]:
        return self._dict.get(key, default)

    def pop(self, key: Any, default: Any = None) -> Any:
        return self._dict.pop(key, default)

    def values(self) -> ValuesView[Any]:
        for key, value in self._dict.items():
            self.convert_with_key(key, value)
        return self._dict.values()

    def items(self) -> ItemsView[Any, Any]:
        for key, value in self._dict.items():
            self.convert_with_key(key, value)
        return self._dict.items()

    def __getitem__(self, key: Any) -> Any:
        return self._dict.__getitem__(key)

    def __setitem__(self, key: Any, value: Any) -> None:
        return self._dict.__setitem__(key, value)

    def __delitem__(self, key: Any) -> None:
        return self._dict.__delitem__(key)

    def __eq__(self, other: Any) -> bool:
        return self._dict == other

    def __ne__(self, other: Any) -> bool:
        return self._dict != other

    def __iter__(self) -> Iterator[Any]:
        return self._dict.__iter__()

    def __len__(self) -> int:
        return self._dict.__len__()

    def __contains__(self, item: Any) -> bool:
        return self._dict.__contains__(item)

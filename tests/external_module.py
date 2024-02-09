from enum import Enum
from logging import Handler, LogRecord


class MyObject:
    def __init__(self, my_key, my_other_key=None):
        self.my_key = my_key
        self.my_other_key = my_other_key


class CustomHandler(Handler):
    def __init__(self, arg):
        Handler.__init__(self)
        self.arg = arg

    def emit(self, record: LogRecord) -> None:
        pass


CONSTANT = "constant"


class Color(Enum):
    RED = "red"
    BLUE = "blue"


class Static:
    @staticmethod
    def get_static_value():
        return "foo"

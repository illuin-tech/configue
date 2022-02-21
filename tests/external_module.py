from unittest.mock import create_autospec


class MyObject:
    def __init__(self, my_key, my_other_key=None):
        self.my_key = my_key
        self.my_other_key = my_other_key


MyObjectMock = create_autospec(MyObject, spec_set=True)

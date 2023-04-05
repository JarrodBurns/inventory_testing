
from enum import Enum
from typing import Dict


class AccessWrapper:

    """
    Allows dictionary and attribute style access for the provided dict and enum.

    Instantiate as a class attribute so extend access to that class. for example:

    d = {"test": object}
    class Foo:
        Sample = AccessWrapper(d, enum)
    print(Foo.Sample.test)
    """

    def __init__(self, objects: Dict[Enum, object], keys: Enum):
        self.objects = objects
        self.keys = keys

    def __getattr__(self, item_name: Enum) -> object:
        try:
            return self.objects[getattr(self.keys, item_name)]

        except KeyError:
            raise AttributeError(f"'{item_name}' is not a valid attribute")

    def __getitem__(self, key: Enum) -> object:
        try:
            return self.objects[key]

        except KeyError:
            raise KeyError(f"{key} not found")

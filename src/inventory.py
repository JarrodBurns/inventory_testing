
from collections import defaultdict
from typing import Dict, List, Union

from access_wrapper import AccessWrapper
from currency import Currency
from item import ItemName
from material import Material, MaterialType


class Inventory:

    def __init__(self):
        self.items      : defaultdict[ItemName, int] = defaultdict(int)
        self.currency   : Currency = Currency()
        self.materials  : Dict[MaterialType, Material] = {}

        self.Items      : AccessWrapper = AccessWrapper(self.items, ItemName)
        self.Materials  : AccessWrapper = AccessWrapper(self.materials, MaterialType)

    def __iadd__(self, other: "Inventory") -> "Inventory":

        if isinstance(other, Inventory):

            for k, v in other.items.items():
                self.items[k] += v

            self.currency += other.currency
            self.add_materials(other.materials.values())

        return self

    def __str__(self) -> str:
        return f"Inventory(items={self.items}, currency={self.currency}, materials={self.materials})"

    def get_all_items(self) -> List[ItemName]:
        return [item for item, count in self.items.items() if count for _ in range(count)]

    def add_item(self, item: Union[ItemName, List[ItemName]]) -> "Inventory":
        if isinstance(item, ItemName):
            self.items[item] += 1

        elif isinstance(item, list):
            for i in item:
                self.items[i] += 1

        return self

    def remove_item(self, item: ItemName) -> "Inventory":

        if not self.items.get(item):
            raise KeyError("Item not found.")

        if self.items[item] - 1 < 0:
            raise ValueError("Insufficient items.")

        if self.items[item] - 1 == 0:
            del self.items[item]

        else:
            self.items[item] -= 1

        return self

    def add_currency(self, amt: int) -> "Inventory":
        self.currency += amt
        return self

    def remove_currency(self, amt: int) -> "Inventory":
        self.currency -= amt
        return self

    def add_materials(self, mat: List[Material]) -> "Inventory":

        for m in mat:
            if self.materials.get(m.name):
                self.materials[m.name] += m

            else:
                self.materials[m.name] = m

        return self

    def remove_materials(self, mat: List[Material]) -> "Inventory":

        for m in mat:

            if not self.materials.get(m.name):
                raise ValueError("Insufficient material.")

            self.materials[m.name] -= m

            if self.materials[m.name].quantity == 0:
                del self.materials[m.name]

        return self


if __name__ == '__main__':

    # For tests see test_inventory.py

    from quality import Quality
    from material import MaterialType

    # Demo of usage
    i = Inventory()
    item = ItemName.RUNED_STONE
    material = [Material(MaterialType.PAPER, Quality.COMMON, 5)]

    i.add_item(item)
    # i.remove_item(item)

    i.currency += 5
    i.currency += Currency(5)

    i.currency -= 5
    i.currency -= Currency(5)

    i.add_materials(material)
    i.remove_materials(material)

    i += i

    # print(i.Materials.PAPER)
    # print(i.Items.RUNED_STONE)

    print(i.get_all_items())

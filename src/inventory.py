
from typing import List, Dict
from collections import defaultdict

from wallet import Wallet
from material import Material
from item import ItemName, ITEMS


class Inventory:

    def __init__(self):
        self.items      : defaultdict[ItemName, int] = defaultdict(int)
        self.wallet     : Wallet = Wallet(0)
        self.materials  : Dict[MaterialType, Material] = {}

    def __iadd__(self, other: "Inventory") -> "Inventory":
        print("fsdhfjksdhfkuds", other.items)
        if isinstance(other, Inventory):

            while other.items:
                for i in other.items:
                    self.add_item(i)
                    other.remove_item(i)

            self.wallet += other.wallet
            self.add_materials(other.materials.values())

        return self

    def __str__(self):
        return f"Inventory(items={self.items}, wallet={self.wallet}, materials={self.materials})"

    def add_item(self, item: ItemName) -> None:
        self.items[item] += 1

    def remove_item(self, item: ItemName) -> None:

        if not self.items.get(item):
            raise KeyError("Item not found.")

        if self.items[item] - 1 < 0:
            raise ValueError("Insufficient items.")

        if self.items[item] - 1 == 0:
            del self.items[item]

        else:
            self.items[item] -= 1

    def add_materials(self, mat: List[Material]) -> None:

        for m in mat:
            if self.materials.get(m.name):
                self.materials[m.name] += m

            else:
                self.materials[m.name] = m

    def remove_materials(self, mat: List[Material]) -> None:

        for m in mat:

            if not self.materials.get(m.name):
                raise KeyError("Insufficient material.")

            self.materials[m.name] -= m

            if self.materials[m.name].quantity == 0:
                del self.materials[m.name]


if __name__ == '__main__':

    i = Inventory()

    print("Add Items")
    item = ItemName.RUNED_STONE
    i.add_item(item)
    i.add_item(item)
    print(f"{i.items}")

    print("Sub Items")
    i.remove_item(item)
    # i.remove_item(item)
    # i.remove_item(item)
    print(f"{i.items=}")

    print("Add Wallet")
    w = Wallet(5)
    i.wallet += w
    i.wallet += 5
    print(f"{i.wallet=}")

    print("Sub Wallet")
    i.wallet -= 1
    print(f"{i.wallet=}")

    print("Add Material")
    scrap = ITEMS[ItemName.TRASH].scrap
    print(f"{scrap[0].quantity=}")
    i.add_materials(scrap)
    i.add_materials(scrap)
    print(f"{i.materials=}")

    print("Sub Material")
    a = ITEMS[ItemName.HAMMER].scrap
    b = ITEMS[ItemName.SAW].scrap
    i.add_materials(a)
    i.add_materials(b)
    print(f"{i.materials=}")
    i.remove_materials(b)
    print(f"{i.materials=}")

    i.add_item(item)
    i.add_item(item)
    print()
    print(i)
    i += i
    print()
    print(i)

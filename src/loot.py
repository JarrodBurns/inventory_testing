
from dataclasses import dataclass, field
from typing import List
import random

from enums import ItemName, Monster, Tag
from inventory import Inventory
from item_manager import ItemManager


@dataclass(frozen=True)
class LootTable:
    creature    : Monster
    weights     : List[int] = field(default_factory=list)
    all_loot    : List[ItemName] = field(default_factory=list)

    def __post_init__(self):
        if len(self.weights) != len(self.all_loot):
            raise ValueError("Lengths of weights and all_loot must be the same.")

        if sum(self.weights) != 100:
            raise ValueError("Weights must add up to 100.")

    @property
    def loot(self) -> ItemName:

        choice = random.choices(self.all_loot, weights=self.weights)[0]

        if isinstance(choice, Tag):
            return ItemManager.get_fm_tag_random(choice).name

        if isinstance(choice, ItemName):
            return choice

    @property
    def creature_value(self) -> int:

        value = 0
        for loot in self.all_loot:

            if isinstance(loot, Tag):
                value += ItemManager.get_fm_tag_random(loot).value

            if isinstance(loot, ItemName):
                value += ItemManager.Item.get_fm_name(loot).value

        return value // 1000

    @property
    def inventory(self) -> Inventory:
        return Inventory().add_item(self.loot).add_currency(self.creature_value)

    def encounter_by_level(self, level: int = 1) -> Inventory:

        if level < 1:
            raise ValueError(f"Level '{level}' must be a positive integer")

        _inventory = Inventory()

        for _ in range(level):
            _inventory += self.inventory

        return _inventory


if __name__ == '__main__':
    ...

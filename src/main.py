
from dataclasses import dataclass, field
from typing import List, Union
import random

from loot import Monster, LOOT_TABLES
from item import Item, ItemName
from material import Material


@dataclass
class Currency:
    ...


@dataclass
class Character:
    name: str
    health: int
    level: int
    attack: int
    defense: int
    is_player: bool
    inventory: List[Union[Item, Material, Currency]] = field(default_factory=list)

    def is_alive(self) -> bool:
        return self.health > 0

    def add_to_inventory(self, item: Union[Item, Material, Currency]) -> None:
        self.inventory.append(item)

    def remove_from_inventory(self, item: Union[Item, Material, Currency]) -> None:
        if item in self.inventory:
            self.inventory.remove(item)


if __name__ == '__main__':

    from pprint import pprint as pprint

    # pprint(ITEMS[ItemName.PENCIL])
    # pprint(f"{ITEMS[ItemName.PENCIL].scrap=}")
    # print(ITEMS[ItemName.PENCIL].scrap[0].material.name)
    # print(ITEMS[ItemName.PENCIL].quality)

    # Sell all treasures, scrap all junk
    # Have a set of tools which help you craft stuff, pliers, hammer, saw, toolbox

    def get_random_item() -> Item:
        return ITEMS[random.choice(list(ItemName))]

    def loot_for_level(creature: Monster, level: int) -> List[ItemName]:
        return [LOOT_TABLES[creature].loot for _ in range(level)]

    # Level 1 Monster
    random_monster_one = random.choice(list(Monster))
    print(f"You encounter a level (1) {random_monster_one}!")
    print(f"You defeat the creature and loot: {LOOT_TABLES[random_monster_one].loot}")

    # Level 1+ Monster
    random_monster_two = random.choice(list(Monster))
    print(f"You encounter a level (2) {random_monster_two}!")
    print(f"You defeat the creature and loot: {', '.join(loot_for_level(random_monster_two, 2))}")

    # j = get_random_item().scrap
    # print(j[0])

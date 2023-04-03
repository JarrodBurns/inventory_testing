
from dataclasses import dataclass, field
from typing import List, Optional, Union
import random

from item import Item, ItemName, ITEMS
from loot import Monster, LOOT_TABLES
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

    def get_random_item() -> Item:
        return ITEMS[random.choice(list(ItemName))]

    def loot_for_level(creature: Monster, level: int) -> List[ItemName]:
        return [LOOT_TABLES[creature].loot for _ in range(level)]

    def random_encounter(level: int, besdiary: Optional[List[Monster]] = list(Monster)) -> None:

        if level == 1:
            random_monster_one = random.choice(besdiary)
            loot_monster_one = LOOT_TABLES[random_monster_one].loot
            print(f"You encounter a level (1) {random_monster_one.value}!")
            print(f"You defeat the creature and loot: {loot_monster_one}")

            print(ITEMS[loot_monster_one].ascii_art())
            print()
            return

        random_monster_two = random.choice(besdiary)
        loot_monster_two = loot_for_level(random_monster_two, level)
        print(f"You encounter a level ({level}) {random_monster_two.value}!")
        print(f"You defeat the creature and loot: {', '.join(loot_monster_two)}")

        for i in loot_monster_two:
            print(ITEMS[i].ascii_art())
        print()

    def random_encounters(
        encounter_max: int,
        mob_level_max: int,
        encounter_min: int = 1,
        mob_level_min: int = 1
    ) -> None:
        for _ in range(random.randint(encounter_min, encounter_max)):
            random_encounter(level=random.randint(mob_level_min, mob_level_max))

    # Output Testing

    # from pprint import pprint as pprint
    # pprint(ITEMS[ItemName.PENCIL])
    # pprint(f"{ITEMS[ItemName.PENCIL].scrap=}")
    # print(ITEMS[ItemName.PENCIL].scrap[0].material.name)
    # print(ITEMS[ItemName.PENCIL].quality)

    # Break an item down into Scrap Material
    # print(get_random_item().scrap)

    # Detailed cards for individual view
    # print(get_random_item().ascii_art())

    # Simulate a few fights and print their loot cards
    random_encounters(encounter_max=3, mob_level_max=3)


from dataclasses import dataclass
from typing import List, Optional
import random

from currency import Currency
from inventory import Inventory
from item import ItemManager, ItemName
from loot import LootManager, Monster


@dataclass
class Character:
    name: str
    health: int
    level: int
    attack: int
    defense: int
    is_player: bool
    inventory: Inventory = Inventory()

    def is_alive(self) -> bool:
        return self.health > 0


def print_encounter_start(level: int, creature: Monster) -> None:
    print(f"You encounter a level ({level}) {creature}!")


def print_encounter_success(creature_inventory: Inventory) -> None:
    print(f"You defeat the creature!")
    print(f"loot[ITEM]: {', '.join(creature_inventory.items)}")
    print(f"loot[COIN]: {creature_inventory.currency.wallet}")
    print()


def random_encounter(level: int, player_inventory: Inventory, besdiary: Optional[List[Monster]] = list(Monster)) -> None:

    # Combat setup
    creature = random.choice(besdiary)
    creature_inventory = LootManager.Tables[creature].encounter_by_level(5)

    print_encounter_start(level, creature)

    # Combat ...

    # Combat success!
    player_inventory += creature_inventory
    print_encounter_success(creature_inventory)


def random_encounters(
    player_inventory    : Inventory,
    encounter_max       : int,
    mob_level_max       : int,
    encounter_min       : int = 1,
    mob_level_min       : int = 1
) -> None:
    for _ in range(random.randint(encounter_min, encounter_max)):
        random_encounter(level=random.randint(mob_level_min, mob_level_max), player_inventory=player_inventory)


if __name__ == '__main__':

    # testing
    player_inventory = Inventory()

    # Simulate a few fights and print their loot cards
    random_encounters(player_inventory=player_inventory, encounter_max=3, mob_level_max=3)

    # Display the contents of the players inventory.
    print(player_inventory)
    for item in player_inventory.get_all_items():
        print(ItemManager.get_item_fm_name(item).ascii_art())

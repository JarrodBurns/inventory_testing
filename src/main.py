
from dataclasses import dataclass
from typing import List, Optional
import random

from inventory import Inventory
from item import ItemManager, ItemName
from loot import LootManager, LootTable, Monster
from wallet import Wallet


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


if __name__ == '__main__':

    def loot_for_level(creature: Monster, level: int) -> List[ItemName]:
        return [LootManager.get_loot_table_fm_monster_name(creature).loot for _ in range(level)]

    def random_encounter(level: int, inventory: Inventory, besdiary: Optional[List[Monster]] = list(Monster)) -> None:

        def _print_helper_encounter(level: int, creature: Monster, items: List[ItemName], wallet: Wallet) -> None:
            print(f"You encounter a level ({level}) {creature}!")
            print(f"You defeat the creature!")
            print(f"loot[ITEM]: {', '.join(items)}")
            print(f"loot[COIN]: {wallet.balance} copper.")
            print()

        _loot_collected = []
        _money_collected = Wallet(0)
        mob = random.choice(besdiary)

        for _ in range(level):
            loot_table = LootManager.get_loot_table_fm_monster_name(mob)
            loot_inv = loot_table.inventory
            inventory += loot_inv
            _loot_collected.extend(loot_inv.get_all_items())
            _money_collected += loot_inv.wallet

        _print_helper_encounter(level, mob, _loot_collected, _money_collected)

    def random_encounters(
        inventory    : Inventory,
        encounter_max: int,
        mob_level_max: int,
        encounter_min: int = 1,
        mob_level_min: int = 1
    ) -> None:
        for _ in range(random.randint(encounter_min, encounter_max)):
            random_encounter(level=random.randint(mob_level_min, mob_level_max), inventory=inventory)

    # testing
    inventory = Inventory()

    # Simulate a few fights and print their loot cards
    random_encounters(inventory=inventory, encounter_max=3, mob_level_max=3)

    # Display the contents of the players inventory.
    print(inventory)
    for item in inventory.get_all_items():
        print(ItemManager.get_item_fm_name(item).ascii_art())

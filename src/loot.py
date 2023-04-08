
from dataclasses import dataclass, field
from typing import Dict, List
import random

from access_wrapper import AccessWrapper
from enums import ItemName, Monster, Tag
from inventory import Inventory
from item import ItemManager


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

        random_item = random.choices(self.all_loot, weights=self.weights)[0]

        if isinstance(random_item, Tag):
            return ItemManager.get_random_item_name_fm_tag(random_item)

        if isinstance(random_item, ItemName):
            return random_item

    @property
    def creature_value(self) -> int:

        value = 0
        for loot in self.all_loot:

            if isinstance(loot, Tag):
                value += ItemManager.get_random_item_fm_tag(loot).value

            if isinstance(loot, ItemName):
                value += ItemManager.get_item_fm_name(loot).value

        return value // 100

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


LOOT_TABLES = {
    Monster.GOBLIN: LootTable(
        creature=Monster.GOBLIN,
        weights=[1, 2, 7, 15, 15, 60],
        all_loot=[
            ItemName.TOOLBOX,
            Tag.TREASURE,
            Tag.TOOL,
            Tag.DECORATION,
            Tag.CLOTHING,
            Tag.JUNK
        ]
    ),
    Monster.TROLL: LootTable(
        creature=Monster.TROLL,
        weights=[4, 10, 15, 15, 20, 36],
        all_loot=[
            Tag.TREASURE,
            ItemName.TOOLBOX,
            Tag.DECORATION,
            Tag.CLOTHING,
            Tag.TOOL,
            Tag.JUNK
        ]
    ),
    Monster.OGRE: LootTable(
        creature=Monster.OGRE,
        weights=[2, 8, 15, 20, 30, 25],
        all_loot=[
            Tag.TREASURE,
            Tag.TOOL,
            Tag.CLOTHING,
            Tag.DECORATION,
            Tag.JUNK,
            Tag.FOOD,
        ]
    ),
    Monster.GIANT_SPIDER: LootTable(
        creature=Monster.GIANT_SPIDER,
        weights=[2, 10, 20, 25, 30, 13],
        all_loot=[
            Tag.TREASURE,
            Tag.WEAVING,
            Tag.CLOTHING,
            Tag.DECORATION,
            Tag.JUNK,
            Tag.POISON,
        ]
    ),
    Monster.GOBLIN_SHAMAN: LootTable(
        creature=Monster.GOBLIN_SHAMAN,
        weights=[5, 10, 20, 25, 25, 15],
        all_loot=[
            Tag.TREASURE,
            Tag.CLOTHING,
            Tag.MAGIC,
            Tag.DECORATION,
            Tag.TOOL,
            Tag.JUNK,
        ]
    ),
}


class LootManager:
    LOOT_TABLES: Dict[Monster, LootTable] = LOOT_TABLES
    Tables: AccessWrapper = AccessWrapper(LOOT_TABLES, Monster)

    @classmethod
    def get_loot_table_fm_monster_name(cls, creature: Monster) -> LootTable:
        return cls.LOOT_TABLES[creature]

    @classmethod
    def get_random_loot_table(cls) -> LootTable:
        return cls.LOOT_TABLES[random.choice(list(Monster))]

    @classmethod
    def get_random_loot_table_fm_tag(cls) -> LootTable:
        raise NotImplementedError("Functionality not yet implemented")


if __name__ == '__main__':
    pass

    # lt = LOOT_TABLES[Monster.GOBLIN]
    # print(lt.creature_value)
    # print(lt.all_loot)
    # lt.loot

    # print(LootManager.get_loot_table_fm_monster_name(Monster.GOBLIN))
    # print(LootManager.get_random_loot_table())
    # i = lt.encounter_by_level(5)

    print(LootManager.Tables[Monster.GOBLIN].encounter_by_level(5))

    # Monster.TROLL: LootTable(
    #     creature=Monster.TROLL,
    #     weights=[4, 10, 15, 15, 20, 36],
    #     all_loot=[
    #         Tag.TREASURE,
    #         ItemName.TOOLBOX,
    #         Tag.DECORATION,
    #         Tag.CLOTHING,
    #         Tag.TOOL,
    #         Tag.JUNK
    #     ]
    # ),

    # print(ItemManager.get_random_item_name_fm_tag(Tag.))

    junk = ItemManager.TagIndex.JUNK
    print(random.choice(junk))

    all_loot = [ItemName.TOOLBOX, *junk]

    print(all_loot)

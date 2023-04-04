
from dataclasses import dataclass, field
from enum import Enum
from typing import List
import random

from item import ItemName, random_fm_tag
from tag import Tag


class Monster(str, Enum):
    GIANT_SPIDER    = "Giant Spider"
    GOBLIN          = "Goblin"
    GOBLIN_SHAMAN   = "Goblin Shaman"
    OGRE            = "Ogre"
    TROLL           = "Troll"


@dataclass
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
            return random_fm_tag(random_item)

        return random_item


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
            Tag.JUNK,
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
            Tag.JUNK,
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

if __name__ == '__main__':
    pass

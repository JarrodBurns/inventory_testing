
from dataclasses import dataclass, field
from enum import Enum
from typing import List
import random

from item import ItemName, random_fm_tag
from tag import Tag


class Monster(str, Enum):
    GOBLIN      = "Goblin"
    TROLL       = "Troll"


@dataclass
class LootTable:
    creature: Monster
    weights: List[int] = field(default_factory=list)
    all_loot: List[ItemName] = field(default_factory=list)

    def __post_init__(self):
        if len(self.weights) != len(self.all_loot):
            raise ValueError("Lengths of weights and all_loot must be the same.")

        if sum(self.weights) != 100:
            raise ValueError("Weights must add up to 100.")

    @property
    def loot(self) -> ItemName:
        return random.choices(self.all_loot, weights=self.weights)[0]


LOOT_TABLES = {
    Monster.GOBLIN: LootTable(
        creature=Monster.GOBLIN,
        weights=[1, 9, 15, 15, 60],
        all_loot=[
            ItemName.TOOLBOX,
            random_fm_tag(Tag.TOOL),
            random_fm_tag(Tag.DECORATION),
            random_fm_tag(Tag.CLOTHING),
            random_fm_tag(Tag.POCKET_LITTER),
        ]
    ),
    Monster.TROLL: LootTable(
        creature=Monster.TROLL,
        weights=[10, 15, 15, 20, 40],
        all_loot=[
            ItemName.TOOLBOX,
            random_fm_tag(Tag.DECORATION),
            random_fm_tag(Tag.CLOTHING),
            random_fm_tag(Tag.TOOL),
            random_fm_tag(Tag.POCKET_LITTER),
        ]
    )
}

if __name__ == '__main__':
    pass

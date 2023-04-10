
from typing import Generic, List, TypeVar, Union
import json

from _db_access_wrapper import AccessWrapper
from _db_models import ModelBase, QueryBase, LootTableModel
from enums import ItemName, Monster, Tag
from loot import LootTable

ModelType = TypeVar('ModelType', bound=ModelBase)
QueryType = TypeVar('QueryType', bound=QueryBase)


def _item_or_tag_helper(all_loot: List[str]) -> List[Union[ItemName, Tag]]:
    all_out = []

    for loot in all_loot:
        try:
            out = ItemName(loot)
        except ValueError:
            out = Tag(loot)
        all_out.append(out)

    return all_out


def as_loottable(query):
    return LootTable(
        creature=Monster(query.monster.name),
        weights=json.loads(query.weights),
        all_loot=_item_or_tag_helper(json.loads(query.all_loot))
    )


class LootManager:
    _model      : Generic[ModelType, QueryType] = LootTableModel
    Tables      : AccessWrapper = AccessWrapper(Monster, _model, as_loottable)


if __name__ == '__main__':

    print(LootManager.Tables[Monster.GOBLIN])
    print(LootManager.Tables.fm_name(Monster.GOBLIN))

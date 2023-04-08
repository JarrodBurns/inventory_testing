
import json
from typing import Callable, List, TypeVar, Union

from sqlalchemy import func
from sqlalchemy.orm import selectinload

from _db_utils import session_scope
from enums import ItemName, MaterialType, Monster, Quality, Tag
from loot import LootTable
from material import Material
from item import Item
import _db_models as _db

T = TypeVar("T")


def x_query(query: callable, result_converter: Callable[[T], T]) -> T:
    with session_scope() as session:
        result = query(session)
        return result_converter(result)


def _item_or_tag_helper(all_loot: List[str]) -> List[Union[ItemName, Tag]]:
    all_out = []

    for loot in all_loot:
        try:
            out = ItemName(loot)
        except ValueError:
            out = Tag(loot)
        all_out.append(out)

    return all_out


def get_loottable_fm_monster(name: Monster) -> LootTable:

    return x_query(
        lambda session: session.query(_db.MonsterModel)
        .filter_by(name=name)
        .first()
        .loot_table,
        lambda loot_table: LootTable(
            creature=Monster(loot_table.monster.name),
            weights=json.loads(loot_table.weights),
            all_loot=_item_or_tag_helper(json.loads(loot_table.all_loot))
        ))


def get_itemnames_fm_quality(quality: Quality) -> List[ItemName]:
    return x_query(
        lambda session: session.query(_db.ItemModel)
        .filter(_db.ItemModel.quality.has(name=quality))
        .options(selectinload(_db.ItemModel.quality))
        .all(),
        lambda items_name: [ItemName(item.name) for item in items_name]
    )


def get_itemname_fm_quality_random(quality: Quality) -> ItemName:
    return x_query(
        lambda session: session.query(_db.ItemModel)
        .filter(_db.ItemModel.quality.has(name=quality))
        .options(selectinload(_db.ItemModel.quality))
        .order_by(func.random())
        .limit(1),
        lambda item_name: ItemName(item_name.first().name)
    )


def get_itemnames_fm_tag(tag: Tag) -> List[ItemName]:

    return x_query(
        lambda session: session.query(_db.ItemModel)
        .filter(_db.ItemModel.tags.any(name=tag))
        .options(selectinload(_db.ItemModel.tags))
        .all(),
        lambda item_names: [ItemName(item.name) for item in item_names]
    )


def get_itemname_fm_tag_random(tag: Tag) -> ItemName:
    return x_query(
        lambda session: session.query(_db.ItemModel)
        .filter(_db.ItemModel.tags.any(name=tag))
        .options(selectinload(_db.ItemModel.tags))
        .order_by(func.random())
        .limit(1),
        lambda item_name: ItemName(item_name.first().name)
    )


def get_itemnames_fm_materialtype(material_type: MaterialType) -> List[ItemName]:
    return x_query(
        lambda session: session.query(_db.ItemModel)
        .filter(_db.ItemModel.materials.any(name=material_type))
        .options(selectinload(_db.ItemModel.materials))
        .all(),
        lambda item_names: [ItemName(item.name) for item in item_names]
    )


def get_itemname_fm_materialtype_random(material_type: MaterialType) -> ItemName:
    return x_query(
        lambda session: session.query(_db.ItemModel)
        .filter(_db.ItemModel.materials.any(name=material_type))
        .options(selectinload(_db.ItemModel.materials))
        .order_by(func.random())
        .limit(1),
        lambda item_name: ItemName(item_name.first().name)
    )


def get_item_fm_itemname(item_name: ItemName) -> Item:
    return x_query(
        lambda session: session.query(_db.ItemModel)
        .filter_by(name=item_name)
        .first(),
        lambda item: Item(
            name=ItemName(item.name),
            weight=item.weight,
            value=item.value,
            description=item.description,
            quality=Quality(item.quality.name),
            craftable=item.craftable,
            composition=[Material(MaterialType(m.name), Quality(m.quality.name)) for m in item.materials],
            tags=[Tag(t.name) for t in item.tags],
            flavor_text=item.flavor_text
        )
    )


def get_items_fm_quality(quality: Quality) -> List[Item]:
    raise NotImplementedError("Functionality not yet implemented")


def get_item_fm_quality_random(quality: Quality) -> Item:
    raise NotImplementedError("Functionality not yet implemented")


def get_items_fm_tag(tag: Tag) -> List[Item]:
    raise NotImplementedError("Functionality not yet implemented")


def get_item_fm_tag_random(tag: Tag) -> Item:
    raise NotImplementedError("Functionality not yet implemented")


def get_items_fm_materialtype(material_type: MaterialType) -> Item:
    raise NotImplementedError("Functionality not yet implemented")


def get_item_fm_materialtype_random(material_type: MaterialType) -> Item:
    raise NotImplementedError("Functionality not yet implemented")


if __name__ == '__main__':

    # The prints live here =======================================================================
    print(get_loottable_fm_monster(Monster.GOBLIN))
    # print(*get_itemnames_fm_quality(Quality.UNCOMMON), sep='\n')
    # print(get_itemname_fm_quality_random(Quality.POOR))
    # print(*get_itemnames_fm_tag(Tag.JUNK), sep='\n')
    # print(get_itemname_fm_tag_random(Tag.JUNK))
    # print(get_itemnames_fm_materialtype(MaterialType.WOOD))
    # print(get_itemname_fm_materialtype_random(MaterialType.WOOD))
    # print(get_item_fm_itemname(ItemName.TRASH).ascii_art())

    # [X] LootTable from Monster
    # [X] ItemNames(s) from Tag
    # [X] ItemNames(s) from Material
    # [X] ItemNames(s) from Quality
    # [X] Item from name
    # [ ] Item Random
    # [ ] LootTable Random

    # [ ] Items with tags and materials

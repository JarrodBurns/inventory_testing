
from typing import Generic, List, TypeVar

from _db_access_wrapper import AccessWrapper
from _db_models import ModelBase, QueryBase, ItemModel
from _db_utils import session_scope
from material import Material
from enums import ItemName, MaterialType, Quality, Tag
from item import Item


ModelType = TypeVar('ModelType', bound=ModelBase)
QueryType = TypeVar('QueryType', bound=QueryBase)


def as_item(query):
    return Item(
        name=ItemName(query.name),
        weight=query.weight,
        value=query.value,
        description=query.description,
        quality=Quality(query.quality.name),
        craftable=query.craftable,
        composition=[Material(MaterialType(m.name), Quality(m.quality.name)) for m in query.materials],
        tags=[Tag(t.name) for t in query.tags],
        flavor_text=query.flavor_text
    )


class ItemManager:
    _model      : Generic[ModelType, QueryType] = ItemModel
    Item        : AccessWrapper = AccessWrapper(ItemName, _model, as_item)

    @classmethod
    def get_fm_materialtype_random(cls, material_type: MaterialType) -> Material:
        with session_scope() as session:
            return as_item(cls._model.get_fm_materialtype_random(session, material_type))

    @classmethod
    def get_fm_quality_random(cls, quality: Quality) -> "Item":
        with session_scope() as session:
            return as_item(cls._model.get_fm_quality_random(session, quality))

    @classmethod
    def get_fm_tag_random(cls, tag: Tag) -> "Item":
        with session_scope() as session:
            return as_item(cls._model.get_fm_tag_random(session, tag))

    @classmethod
    def gets_fm_quality(cls, quality: Quality) -> List["Item"]:
        with session_scope() as session:
            return [as_item(row) for row in cls._model.gets_fm_quality(session, quality)]

    @classmethod
    def gets_fm_materialtype(cls, material_type: MaterialType) -> List["Item"]:
        with session_scope() as session:
            return [as_item(row) for row in cls._model.gets_fm_materialtype(session, material_type)]

    @classmethod
    def gets_fm_tag(cls, tag: Tag) -> List["Item"]:
        with session_scope() as session:
            return [as_item(row) for row in cls._model.gets_fm_tag(session, tag)]


if __name__ == '__main__':
    pass

    # print(ItemManager.Item.FLARP)  # Raises error
    print(ItemManager.Item.TRASH)
    print(ItemManager.Item.random)
    print(ItemManager.Item.all_results)
    print(ItemManager.Item[ItemName.TRASH])
    print(ItemManager.Item.fm_id(1))

    print(ItemManager.get_fm_materialtype_random(MaterialType.WOOD))
    print(ItemManager.get_fm_quality_random(Quality.UNCOMMON))
    print(ItemManager.get_fm_tag_random(Tag.JUNK))
    print(ItemManager.gets_fm_quality(Quality.UNCOMMON))
    print(ItemManager.gets_fm_materialtype(MaterialType.WOOD))

    # print(LootManager.Tables.GOBLIN)
    # print(LootManager.Tables.fm_id(1))

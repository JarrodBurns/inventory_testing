
from typing import Generic, List, TypeVar

from _db_access_wrapper import AccessWrapper
from _db_models import ModelBase, QueryBase, ItemModel
from _db_utils import session_scope
from material import Material
from enums import ItemName, MaterialType, Quality, Tag


ModelType = TypeVar('ModelType', bound=ModelBase)
QueryType = TypeVar('QueryType', bound=QueryBase)


class ItemManager:
    _model      : Generic[ModelType, QueryType] = ItemModel
    Item        : AccessWrapper = AccessWrapper(ItemName, _model, "as_item")

    @classmethod
    def get_fm_materialtype_random(cls, material_type: MaterialType) -> Material:
        with session_scope() as session:
            return cls._model.get_fm_materialtype_random(session, material_type).as_item

    @classmethod
    def get_fm_quality_random(cls, quality: Quality) -> "Item":
        with session_scope() as session:
            return cls._model.get_fm_quality_random(session, quality).as_item

    @classmethod
    def get_fm_tag_random(cls, tag: Tag) -> "Item":
        with session_scope() as session:
            return cls._model.get_fm_tag_random(session, tag).as_item

    @classmethod
    def gets_fm_quality(cls, quality: Quality) -> List["Item"]:
        with session_scope() as session:
            # print(cls._model.gets_fm_quality(session, quality))
            return [row.as_item for row in cls._model.gets_fm_quality(session, quality)]

    @classmethod
    def gets_fm_materialtype(cls, material_type: MaterialType) -> List["Item"]:
        with session_scope() as session:
            return [row.as_item for row in cls._model.gets_fm_materialtype(session, material_type)]

    @classmethod
    def gets_fm_tag(cls, tag: Tag) -> List["Item"]:
        with session_scope() as session:
            return [row.as_item for row in cls._model.gets_fm_tag(session, tag)]


if __name__ == '__main__':
    pass

    # print(ItemManager.Item.FLARP)  # Raises error
    # print(ItemManager.Item.TRASH)
    # print(ItemManager.Item.random)
    # print(ItemManager.Item.all)
    # print(ItemManager.Item[ItemName.TRASH])
    # print(ItemManager.ItemName.random)
    # print(ItemManager.ItemName.model.get_fm_name(ItemName.TRASH))
    # print(ItemManager.Item.fm_id(1))

    # print(ItemManager.get_fm_materialtype_random(MaterialType.WOOD))
    # print(ItemManager.get_fm_quality_random(Quality.UNCOMMON))
    # print(ItemManager.get_fm_tag_random(Tag.JUNK))
    # print(ItemManager.gets_fm_quality(Quality.UNCOMMON))
    # print(ItemManager.gets_fm_materialtype(MaterialType.WOOD))


import json
from typing import List, Optional, Union

from sqlalchemy import Boolean, Column, ForeignKey, func, Integer, JSON, String, Table
from sqlalchemy.orm import joinedload, Query, relationship, selectinload, Session

from _db_utils import session_scope, SingletonModelBase
from enums import ItemName, MaterialType, Monster, Quality, Tag
from item import Item
from loot import LootTable
from material import Material


ModelBase = SingletonModelBase.get_instance()


class QualityModel(ModelBase):
    __tablename__  = "Qualities"
    id             = Column(Integer, primary_key=True)
    name           = Column(String, unique=True, nullable=False)

    def __repr__(self):
        return f"QualityModel(id={self.id}, name='{self.name}')"


class TagModel(ModelBase):
    __tablename__   = 'Tags'
    id              = Column(Integer, primary_key=True)
    name            = Column(String, unique=True, nullable=False)
    items           = relationship('ItemModel', secondary='Item_Tag', back_populates='tags')

    def __str__(self) -> str:
        return self.name

    def __repr__(self):
        return f"TagModel(id={self.id}, name='{self.name}')"


class MaterialModel(ModelBase):
    __tablename__   = "Materials"
    id              = Column(Integer, primary_key=True)
    name            = Column(String, unique=True, nullable=False)
    quality_id      = Column(Integer, ForeignKey('Qualities.id'))
    quality         = relationship('QualityModel', backref="materials")
    quantity        = Column(Integer, default=0, nullable=False)
    items           = relationship("ItemModel", secondary="Item_Material", back_populates="materials")

    def __repr__(self):
        return f"MaterialModel(id={self.id}, name='{self.name}', quality_id={self.quality_id}, quantity={self.quantity})"


class ItemModel(ModelBase):
    __tablename__   = 'Items'
    id              = Column(Integer, primary_key=True)
    name            = Column(String, unique=True, nullable=False)
    weight          = Column(Integer, nullable=False)
    value           = Column(Integer, nullable=False)
    description     = Column(String, nullable=False)
    quality_id      = Column(Integer, ForeignKey('Qualities.id'))
    quality         = relationship('QualityModel', backref='items')
    craftable       = Column(Boolean, nullable=False)
    materials       = relationship("MaterialModel", secondary="Item_Material", back_populates='items')
    tags            = relationship('TagModel', secondary='Item_Tag', back_populates='items')
    flavor_text     = Column(String, nullable=True)

    def __repr__(self):
        return f"ItemModel(id={self.id}, name='{self.name}', weight={self.weight}, value={self.value}, description='{self.description}', quality_id={self.quality_id}, craftable={self.craftable})"

    @property
    def as_item(self) -> Item:
        return Item(
            name=ItemName(self.name),
            weight=self.weight,
            value=self.value,
            description=self.description,
            quality=Quality(self.quality.name),
            craftable=self.craftable,
            composition=[Material(MaterialType(m.name), Quality(m.quality.name)) for m in self.materials],
            tags=[Tag(t.name) for t in self.tags],
            flavor_text=self.flavor_text
        )

    @classmethod
    def get_fm_itemname(cls, session: Session, item_name: ItemName) -> Query["ItemModel"]:
        return (
            session.query(cls)
            .filter_by(name=item_name)
            .first()
        )

    @classmethod
    def get_fm_materialtype_random(cls, session: Session, material_type: MaterialType) -> Query["ItemModel"]:
        return (
            session.query(cls)
            .filter(cls.materials.any(name=material_type))
            .options(selectinload(cls.materials))
            .order_by(func.random())
            .first()
        )

    @classmethod
    def get_fm_quality_random(cls, session: Session, quality: Quality) -> Query["ItemModel"]:
        return (
            session.query(cls)
            .filter(cls.quality.has(name=quality))
            .options(selectinload(cls.quality))
            .order_by(func.random())
            .first()
        )

    @classmethod
    def get_fm_random(cls, session: Session) -> Query["ItemModel"]:
        return (
            session.query(cls).filter(
                cls.id == session.query(cls.id)
                .order_by(func.random())
                .limit(1).scalar_subquery()
            ).first()
        )

    @classmethod
    def get_fm_tag_random(cls, session: Session, tag: Tag) -> Query["ItemModel"]:
        return (
            session.query(cls)
            .filter(cls.tags.any(name=tag))
            .options(selectinload(cls.tags))
            .order_by(func.random())
            .first()
        )

    @classmethod
    def gets_fm_quality(cls, session, quality: Quality) -> Query["ItemModel"]:
        return (
            session.query(cls)
            .filter(cls.quality.has(name=quality))
            .options(selectinload(cls.quality))
            .all()
        )

    @classmethod
    def gets_fm_materialtype(cls, session: Session, material_type: MaterialType) -> Query["ItemModel"]:
        return (
            session.query(cls)
            .filter(cls.materials.any(name=material_type))
            .options(selectinload(cls.materials))
            .all()
        )

    @classmethod
    def gets_fm_tag(cls, session: Session, tag: Tag) -> Query["ItemModel"]:
        return (
            session.query(cls)
            .filter(cls.tags.any(name=tag))
            .options(selectinload(cls.tags))
            .all()
        )


class MonsterModel(ModelBase):
    __tablename__   = "Monsters"
    id              = Column(Integer, primary_key=True)
    name            = Column(String, unique=True, nullable=False)
    loot_table      = relationship('LootTableModel', uselist=False, back_populates='monster')

    def __repr__(self):
        return f"MonsterModel(id={self.id}, name='{self.name}')"

    @property
    def as_monster(self) -> Monster:
        return Monster(self.name)

    @classmethod
    def get_fm_name(cls, session: Session) -> Query["MonsterModel"]:
        raise NotImplementedError("Functionality not yet implemented!")

    @classmethod
    def get_fm_random(cls, session: Session) -> Query["MonsterModel"]:
        return (
            session.query(cls)
            .order_by(func.random())
            .first()
        )


class LootTableModel(ModelBase):
    __tablename__   = "LootTables"
    id              = Column(Integer, primary_key=True)
    weights         = Column(JSON, nullable=False)
    all_loot        = Column(JSON, nullable=False)
    monster_id      = Column(Integer, ForeignKey('Monsters.id'))
    monster         = relationship('MonsterModel', back_populates='loot_table')

    def __repr__(self):
        return f"LootTableModel(id={self.id}, weights={self.weights}, all_loot={self.all_loot}, monster_id={self.monster_id})"

    @staticmethod
    def _item_or_tag_helper(all_loot: List[str]) -> List[Union[ItemName, Tag]]:
        all_out = []

        for loot in all_loot:
            try:
                out = ItemName(loot)
            except ValueError:
                out = Tag(loot)
            all_out.append(out)

        return all_out

    @property
    def as_loot_table(self) -> LootTable:
        return LootTable(
            creature=Monster(self.monster.name),
            weights=json.loads(self.weights),
            all_loot=self._item_or_tag_helper(json.loads(self.all_loot))
        )

    @classmethod
    def get_fm_monster(cls, session, monster: Monster) -> Query["LootTableModel"]:
        return (
            session.query(cls)
            .join(cls.monster)
            .options(joinedload(cls.monster))
            .filter(MonsterModel.name == monster)
            .first()
        )

    @classmethod
    def get_fm_random(cls, session) -> Query["LootTableModel"]:
        return (
            session.query(cls)
            .order_by(func.random())
            .first()
        )


# Association tables
Item_Tag = Table(
    'Item_Tag', ModelBase.metadata,
    Column('item_id', Integer, ForeignKey('Items.id')),
    Column('tag_id', Integer, ForeignKey('Tags.id'))
)
Item_Material = Table(
    'Item_Material', ModelBase.metadata,
    Column('item_id', Integer, ForeignKey('Items.id')),
    Column('material_id', Integer, ForeignKey('Materials.id'))
)

if __name__ == '__main__':

    with session_scope() as session:
        ...
        # ItemModel ==============================================================
        # print(ItemModel.get_fm_itemname(session, ItemName.TRASH).as_item.ascii_art())
        # print(ItemModel.get_fm_materialtype_random(session, MaterialType.WOOD).as_item.ascii_art())
        # print(ItemModel.get_fm_quality_random(session, Quality.UNCOMMON).as_item.ascii_art())
        # print(ItemModel.get_fm_random(session).as_item.ascii_art())
        # print(ItemModel.get_fm_tag_random(session, Tag.JUNK).as_item.ascii_art())
        # print(*[i.as_item.ascii_art() for i in ItemModel.gets_fm_materialtype(session, MaterialType.BRASS)], sep='\n')
        # print(*[i.as_item.ascii_art() for i in ItemModel.gets_fm_quality(session, Quality.UNCOMMON)], sep='\n')
        # print(*[i.as_item.ascii_art() for i in ItemModel.gets_fm_tag(session, Tag.TREASURE)], sep='\n')

        # LootTableModel =========================================================
        # print(LootTableModel.get_fm_monster(session, Monster.GOBLIN).as_loot_table)
        # print(LootTableModel.get_fm_random(session).as_loot_table)

        # MonsterModel ===========================================================
        # print(MonsterModel.get_fm_random(session).as_monster)

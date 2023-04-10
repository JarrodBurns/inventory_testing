
from typing import List

from sqlalchemy import Boolean, Column, ForeignKey, func, Integer, JSON, String, Table
from sqlalchemy.orm import joinedload, Query, relationship, selectinload, Session

from _db_utils import session_scope, SingletonModelBase
from enums import MaterialType, Monster, Quality, Tag

from material import Material


ModelBase = SingletonModelBase.get_instance()


class QueryBase:

    @classmethod
    def get_fm_id(cls, session: Session, id: int) -> Query["QueryBase"]:
        return session.query(cls).filter_by(id=id).first()

    @classmethod
    def get_fm_name(cls, session: Session, name: str) -> Query["QueryBase"]:
        return session.query(cls).filter_by(name=name).first()

    @classmethod
    def get_fm_random(cls, session: Session) -> Query["QueryBase"]:
        return session.query(cls).order_by(func.random()).first()

    @classmethod
    def gets_all(cls, session: Session) -> List[Query["QueryBase"]]:
        return session.query(cls).all()


class QualityModel(ModelBase, QueryBase):
    __tablename__  = "Qualities"
    id             = Column(Integer, primary_key=True)
    name           = Column(String, unique=True, nullable=False)

    def __repr__(self):
        return f"QualityModel(id={self.id}, name='{self.name}')"

    @property
    def as_quality(self) -> Quality:
        return Quality(self.name)


class TagModel(ModelBase, QueryBase):
    __tablename__   = 'Tags'
    id              = Column(Integer, primary_key=True)
    name            = Column(String, unique=True, nullable=False)
    items           = relationship('ItemModel', secondary='Item_Tag', back_populates='tags')

    def __str__(self) -> str:
        return self.name

    def __repr__(self):
        return f"TagModel(id={self.id}, name='{self.name}')"

    @property
    def as_tag(self) -> Tag:
        return Tag(self.name)


class MaterialModel(ModelBase, QueryBase):
    __tablename__   = "Materials"
    id              = Column(Integer, primary_key=True)
    name            = Column(String, unique=True, nullable=False)
    quality_id      = Column(Integer, ForeignKey('Qualities.id'))
    quality         = relationship('QualityModel', backref="materials")
    quantity        = Column(Integer, default=0, nullable=False)
    items           = relationship("ItemModel", secondary="Item_Material", back_populates="materials")

    def __repr__(self):
        return f"MaterialModel(id={self.id}, name='{self.name}', quality_id={self.quality_id}, quantity={self.quantity})"

    @property
    def as_material(self) -> Material:
        return Material(name=MaterialType(self.name), quality=Quality(self.quality.name))

    @classmethod
    def gets_fm_quality(cls, session: Session, quality: Quality) -> Query["MaterialModel"]:
        return (
            session.query(cls)
            .join(cls.quality)
            .filter(QualityModel.name == quality)
            .all()
        )


class ItemModel(ModelBase, QueryBase):
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
    def get_fm_tag_random(cls, session: Session, tag: Tag) -> Query["ItemModel"]:
        return (
            session.query(cls)
            .filter(cls.tags.any(name=tag))
            .options(selectinload(cls.tags))
            .order_by(func.random())
            .first()
        )

    @classmethod
    def gets_fm_quality(cls, session: Session, quality: Quality) -> Query["ItemModel"]:
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


class MonsterModel(ModelBase, QueryBase):
    __tablename__   = "Monsters"
    id              = Column(Integer, primary_key=True)
    name            = Column(String, unique=True, nullable=False)
    loot_table      = relationship('LootTableModel', uselist=False, back_populates='monster')

    def __repr__(self):
        return f"MonsterModel(id={self.id}, name='{self.name}')"

    @property
    def as_monster(self) -> Monster:
        return Monster(self.name)


class LootTableModel(ModelBase, QueryBase):
    __tablename__   = "LootTables"
    id              = Column(Integer, primary_key=True)
    weights         = Column(JSON, nullable=False)
    all_loot        = Column(JSON, nullable=False)
    monster_id      = Column(Integer, ForeignKey('Monsters.id'))
    monster         = relationship('MonsterModel', back_populates='loot_table')

    def __repr__(self):
        return f"LootTableModel(id={self.id}, weights={self.weights}, all_loot={self.all_loot}, monster_id={self.monster_id})"

    @classmethod
    def get_fm_name(cls, session, monster: Monster) -> Query["LootTableModel"]:
        return (
            session.query(cls)
            .join(cls.monster)
            .options(joinedload(cls.monster))
            .filter(MonsterModel.name == monster)
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
        from enums import ItemName

        # QueryBase ==============================================================
        # print(QualityModel.get_fm_name(session, Quality.COMMON))
        # print(QualityModel.get_fm_id(session, 1))
        # print(QualityModel.get_fm_random(session))
        # print(QualityModel.gets_all(session))

        # QualityModel ==============================================================
        # print(QualityModel.get_fm_name(session, Quality.POOR).as_quality)
        # print(QualityModel.get_fm_random(session))

        # TagModel ==============================================================
        # print(TagModel.get_fm_name(session, Tag.JUNK))
        # print(TagModel.get_fm_random(session))

        # MaterialModel ==========================================================
        # print(MaterialModel.get_fm_name(session, MaterialType.BONE))
        # print(MaterialModel.get_fm_random(session))
        # print(*[m for m in MaterialModel.gets_fm_quality(session, Quality.UNCOMMON)], sep='\n')

        # ItemModel ==============================================================
        # print(ItemModel.get_fm_name(session, ItemName.TRASH))
        # print(ItemModel.get_fm_name(session, ItemName.TRASH))
        # print(ItemModel.get_fm_materialtype_random(session, MaterialType.WOOD))
        # print(ItemModel.get_fm_quality_random(session, Quality.UNCOMMON))
        # print(ItemModel.get_fm_random(session))
        # print(ItemModel.get_fm_tag_random(session, Tag.JUNK))
        # print(*[i for i in ItemModel.gets_fm_materialtype(session, MaterialType.BRASS)], sep='\n')
        # print(*[i for i in ItemModel.gets_fm_quality(session, Quality.UNCOMMON)], sep='\n')
        # print(*[i for i in ItemModel.gets_fm_tag(session, Tag.TREASURE)], sep='\n')

        # MonsterModel ===========================================================
        # print(MonsterModel.get_fm_name(session, Monster.GOBLIN).as_monster)
        # print(MonsterModel.get_fm_random(session).as_monster)

        # LootTableModel =========================================================
        # print(LootTableModel.get_fm_name(session, Monster.GOBLIN))
        # print(LootTableModel.get_fm_random(session))

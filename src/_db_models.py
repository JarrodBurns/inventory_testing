
from sqlalchemy import Column, Integer, String, ForeignKey, JSON, Table, Boolean
from sqlalchemy.orm import relationship

from _db_utils import SingletonModelBase


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


class MonsterModel(ModelBase):
    __tablename__ = "Monsters"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    loot_table = relationship('LootTableModel', uselist=False, back_populates='monster')

    def __repr__(self):
        return f"MonsterModel(id={self.id}, name='{self.name}')"


class LootTableModel(ModelBase):
    __tablename__ = "LootTables"
    id = Column(Integer, primary_key=True)
    weights = Column(JSON, nullable=False)
    all_loot = Column(JSON, nullable=False)
    monster_id = Column(Integer, ForeignKey('Monsters.id'))
    monster = relationship('MonsterModel', back_populates='loot_table')

    def __repr__(self):
        return f"LootTableModel(id={self.id}, weights={self.weights}, all_loot={self.all_loot}, monster_id={self.monster_id})"


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

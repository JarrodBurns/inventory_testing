

from dataclasses import dataclass, field
from typing import List, Optional
import random
import textwrap

from access_wrapper import AccessWrapper
from currency import Currency
from enums import Border, ItemName, MaterialType, Quality, Tag
from material import Material

ModelBase = SingletonModelBase.get_instance()
ModelType = TypeVar('ModelType', bound=ModelBase)
QueryType = TypeVar('QueryType', bound=QueryBase)


@dataclass(frozen=True)
class Item:
    name        : ItemName
    weight      : int   # grams
    value       : int   # Indicative of average cost to purchase in the US. Represented in pennies.
    description : str
    quality     : Quality
    craftable   : bool
    composition : List[Material]
    tags        : List[Tag] = field(default_factory=list)
    flavor_text : Optional[str] = None

    @property
    def scrap(self) -> List[Material]:

        max_reward = self.weight // 2 if self.weight > 1 else 2
        return [
            material + quantity
            for material
            in self.composition
            if (quantity := random.randint(0, max_reward))
        ]

    def ascii_art(self, min_line_length=80, max_line_length=80) -> str:
        name    = f"{self.name.value} ({self.quality.name})"
        desc    = self.description
        tags    = ", ".join(self.tags)
        value   = str(Currency(self.value).wallet)
        weight  = f"{self.weight} grams"
        scrap   = ", ".join(mat.name for mat in self.composition)
        lines   = [
            name,
            "=" * len(name),
            desc,
            "",
            "Tags:",
            tags,
            "",
            "Value:",
            value,
            "Weight:",
            weight,
            "Scrap:",
            scrap
        ]

        # Wrap lines that exceed max_line_length
        wrapped_lines = []
        for line in lines:
            if len(line) > max_line_length:
                wrapped_lines.extend(textwrap.wrap(line, width=max_line_length))
            else:
                wrapped_lines.append(line)

        # Add padding to lines shorter than min_line_length
        padded_lines = []
        for line in wrapped_lines:
            if len(line) < min_line_length:
                line += " " * (min_line_length - len(line))
            padded_lines.append(line)

        # Pad lines to be equal length
        max_length = max(len(line) for line in padded_lines)
        padded_lines = [f"{Border.LRM} {line.ljust(max_length)} {Border.LRM}" for line in padded_lines]

        # Format lines as ASCII card
        card = [
            f"{Border.LTC}{Border.TBM * (max_length + 2)}{Border.RTC}"
        ] + padded_lines + [
            f"{Border.LBC}{Border.TBM * (max_length + 2)}{Border.RBC}"
        ]

        return "\n".join(card)


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

    @property
    def as_itemname(self) -> ItemName:
        return ItemName(self.name)

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
            return [row.as_item for row in cls._model.gets_fm_quality(session, quality)]

    @classmethod
    def gets_fm_materialtype(cls, material_type: MaterialType) -> List["Item"]:
        with session_scope() as session:
            return [row.as_item for row in cls._model.gets_fm_materialtype(session, material_type)]

    @classmethod
    def gets_fm_tag(cls, tag: Tag) -> List["Item"]:
        with session_scope() as session:
            return [row.as_item for row in cls._model.gets_fm_tag(session, tag)]

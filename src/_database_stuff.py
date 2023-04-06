
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table, Boolean
from sqlalchemy.orm import Session, sessionmaker, declarative_base, relationship

from _db_utils import SingletonModelBase, Session, session_scope, ENGINE
from quality import Quality
from tag import Tag

ModelBase = SingletonModelBase.get_instance()


class QualityModel(ModelBase):
    __tablename__  = "Qualities"
    id             = Column(Integer, primary_key=True)
    name           = Column(String, unique=True)


class TagModel(ModelBase):
    __tablename__   = 'Tags'
    id              = Column(Integer, primary_key=True)
    name            = Column(String, unique=True)
    items           = relationship('ItemModel', secondary='Item_Tag', back_populates='tags')

    def __str__(self):
        return f"TagModel(name='{self.name}')"


class ItemModel(ModelBase):
    __tablename__   = 'Items'
    id              = Column(Integer, primary_key=True)
    name            = Column(String, unique=True)
    tags            = relationship('TagModel', secondary='Item_Tag', back_populates='items')
    quality_id      = Column(Integer, ForeignKey('Qualities.id'))
    quality         = relationship('QualityModel', backref='items')


# Association tables
Item_Tag = Table(
    'Item_Tag', ModelBase.metadata,
    Column('item_id', Integer, ForeignKey('Items.id')),
    Column('tag_id', Integer, ForeignKey('Tags.id'))
)


def ZERO_DATABASE(model_base):

    with session_scope() as _:

        model_base.metadata.drop_all(bind=ENGINE)
        model_base.metadata.create_all(bind=ENGINE)

# TODO change name=tag.value when using enum


def create_tags(tags: list[Tag]) -> None:
    """
    Query the database and create tag entries which do not exist
    """

    with session_scope() as session:

        all_tags = session.query(TagModel).filter(TagModel.name.in_(new_tags)).all()
        tags_to_add = set(new_tags) - {t.name for t in all_tags}

        for tag in tags_to_add:
            session.add(TagModel(name=tag))


# def get_or_create_quality(quality_name, session) -> None:
#     """
#     Query the database and create tag entries which do not exist
#     """

#     # with session_scope() as session:

#     quality = session.query(QualityModel).filter(QualityModel.name == quality_name.value).first()

#     if quality:
#         print(f"Quality '{quality_name}' has id '{quality.id}'")
#         # return quality
#     else:
#         print(f"No quality found with name '{quality_name}'")

#         session.add(QualityModel(name=quality_name))
#         session.flush()


# def get_or_create_tag(tag_name: Tag, session) -> None:
#     """
#     Query the database and create tag entries which do not exist
#     """

#     # with session_scope() as session:

#     tag = session.query(TagModel).filter(TagModel.name == tag_name.value).first()

#     if tag:
#         print(f"tag '{tag_name}' has id '{tag.id}'")
#         # return tag
#     else:
#         print(f"No tag found with name '{tag_name}'")

#         session.add(QualityModel(name=tag_name.value))
#         session.flush()


if __name__ == '__main__':

    ZERO_DATABASE(ModelBase)

    with session_scope() as session:
        item = ItemModel(name="Health Potion", quality=QualityModel(name="Uncommon"))
        item.tags.append(TagModel(name="Potion"))
        item.tags.append(TagModel(name="Consumable"))
        session.add(item)
        # session.commit()

    new_tags = ["tag1", "XXXX", "Potion", "flipper"]

    create_tags(new_tags)

    from dataclasses import dataclass

    @dataclass
    class Item:
        name: str
        tags: list
        quality: str

    sword = Item(name="Sword", tags=[Tag.MAGIC, Tag.EQUIPMENT], quality=Quality.UNCOMMON)
    club = Item(name="Club", tags=[Tag.TREASURE, Tag.EQUIPMENT], quality=Quality.UNCOMMON)

    items = [sword, club]

    # with session_scope() as session:

    #     for i in items:
    #         # create_tags(i.tags)
    #         item = ItemModel(name=i.name, quality=get_or_create_quality(i.quality, session))
    #         # print(i)

    #         for t in i.tags:
    #             # item.tags.append(TagModel(name=t))
    #             get_or_create_tag(t, session)

    # session.add(item)

# qualities

    with session_scope() as session:
        quality = session.query(QualityModel).filter(QualityModel.name == "Uncommon").first()
        if not quality:
            quality = QualityModel(name="Uncommon")
            session.add(quality)
            session.flush()

        tag_names = ["Potion", "Health"]
        tags = session.query(TagModel).filter(TagModel.name.in_(tag_names)).all()
        existing_tags = set(tag.name for tag in tags)

        for tag_name in tag_names:
            if tag_name not in existing_tags:
                tag = TagModel(name=tag_name)
                session.add(tag)
                session.flush()
                tags.append(tag)

        item = ItemModel(name="Health Potion", quality=quality, tags=tags)
        session.add(item)
        session.commit()

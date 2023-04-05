
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table, Boolean
from sqlalchemy.orm import Session, sessionmaker, declarative_base, relationship

from _db_utils import SingletonModelBase, Session, session_scope, ENGINE
from tag import Tag

ModelBase = SingletonModelBase.get_instance()


class QualityModel(ModelBase):
    __tablename__  = "Quality"
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
    quality_id      = Column(Integer, ForeignKey('Quality.id'))
    quality         = relationship('QualityModel', uselist=False, backref='items')


# Association tables
Item_Tag = Table(
    'Item_Tag', ModelBase.metadata,
    Column('item_id', Integer, ForeignKey('Items.id')),
    Column('tag_id', Integer, ForeignKey('Tags.id'))
)


def ZERO_DATABASE(model_base):

    with session_scope() as session:

        model_base.metadata.drop_all(bind=ENGINE)
        model_base.metadata.create_all(bind=ENGINE)


def create_tag_rows(tags: list[Tag]) -> None:
    """
    Query the database and create tag entries which do not exist
    """

    with session_scope() as session:

        all_tags = session.query(TagModel).filter(TagModel.name.in_(new_tags)).all()
        tags_to_add = set(new_tags) - {t.name for t in all_tags}

        for tag in tags_to_add:
            session.add(TagModel(name=tag))


if __name__ == '__main__':

    ZERO_DATABASE(ModelBase)

    # item = ItemModel(name="Health Potion", quality=QualityModel(name="Uncommon"))
    # item.tags.append(TagModel(name="Potion"))
    # item.tags.append(TagModel(name="Consumable"))
    # session.add(item)
    # session.commit()

    new_tags = ["tag1", "XXXX", "Potion", "flipper"]

    create_tag_rows(new_tags)

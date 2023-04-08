
import json


from _db_utils import ENGINE, session_scope, SingletonModelBase
from enums import Monster, Quality, Tag
from loot import LOOT_TABLES
from item import ITEMS
from material import MATERIALS


import _db_models as _db


def ZERO_DATABASE(model_base):

    with session_scope() as _:

        model_base.metadata.drop_all(bind=ENGINE)
        model_base.metadata.create_all(bind=ENGINE)


def CREATE_DATABASE():
    with session_scope() as session:

        for tag in Tag:
            t = _db.TagModel(name=tag)
            session.add(t)

        for quality in Quality:
            q = _db.QualityModel(name=quality)
            session.add(q)

        for monster in Monster:
            m = _db.MonsterModel(name=monster)
            session.add(m)

        for material in MATERIALS.values():
            m = _db.MaterialModel(
                name=material.name,
                quality=session.query(_db.QualityModel).filter(_db.QualityModel.name == material.quality).first()
            )
            session.add(m)

        for item in ITEMS.values():
            i = _db.ItemModel(
                name=item.name,
                weight=item.weight,
                value=item.value,
                description=item.description,
                quality=session.query(_db.QualityModel).filter(_db.QualityModel.name == item.quality).first(),
                craftable=item.craftable,
                materials=session.query(_db.MaterialModel).filter(_db.MaterialModel.name.in_([i.name for i in item.composition])).all(),
                tags=session.query(_db.TagModel).filter(_db.TagModel.name.in_(item.tags)).all(),
                flavor_text=item.flavor_text
            )
            session.add(i)

        for table in LOOT_TABLES.values():
            t = _db.LootTableModel(
                weights=json.dumps(table.weights),
                all_loot=json.dumps(table.all_loot),
                monster=session.query(_db.MonsterModel).filter(_db.MonsterModel.name == table.creature).first(),
            )
            session.add(t)


if __name__ == '__main__':

    # ZERO_DATABASE(SingletonModelBase.get_instance())
    # CREATE_DATABASE()
    ...

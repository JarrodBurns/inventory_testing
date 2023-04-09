
import json

from _db_entries import ITEMS
from _db_utils import ENGINE, session_scope, SingletonModelBase
from enums import Monster, Quality, Tag
from loot import LOOT_TABLES
from material import MATERIALS


import _db_models as db


def ZERO_DATABASE(model_base):

    with session_scope() as _:

        model_base.metadata.drop_all(bind=ENGINE)
        model_base.metadata.create_all(bind=ENGINE)


def CREATE_DATABASE():
    with session_scope() as session:

        for tag in Tag:
            t = db.TagModel(name=tag)
            session.add(t)

        for quality in Quality:
            q = db.QualityModel(name=quality)
            session.add(q)

        for monster in Monster:
            m = db.MonsterModel(name=monster)
            session.add(m)

        for material in MATERIALS.values():
            m = db.MaterialModel(
                name=material.name,
                quality=db.QualityModel.get_fm_name(session, material.quality)
            )
            session.add(m)

        for item in ITEMS:
            i = db.ItemModel(
                name=item.name,
                weight=item.weight,
                value=item.value,
                description=item.description,
                quality=db.QualityModel.get_fm_name(session, item.quality),
                craftable=item.craftable,
                materials=[db.MaterialModel.get_fm_name(session, material.name) for material in item.composition],
                tags=[db.TagModel.get_fm_name(session, tag) for tag in item.tags],
                flavor_text=item.flavor_text
            )
            session.add(i)

        for table in LOOT_TABLES.values():
            t = db.LootTableModel(
                weights=json.dumps(table.weights),
                all_loot=json.dumps(table.all_loot),
                monster=db.MonsterModel.get_fm_name(session, table.creature),
            )
            session.add(t)


if __name__ == '__main__':

    ZERO_DATABASE(SingletonModelBase.get_instance())
    CREATE_DATABASE()
    ...

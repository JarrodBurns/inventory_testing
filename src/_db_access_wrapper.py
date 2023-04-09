
from enum import Enum
from typing import Generic, List, TypeVar

from sqlalchemy.orm.exc import NoResultFound

from _db_models import ModelBase, QueryBase
from _db_utils import session_scope

ModelType = TypeVar('ModelType', bound=ModelBase)
QueryType = TypeVar('QueryType', bound=QueryBase)


class AccessWrapper:

    def __init__(self, keys, model, access_property):
        self.keys               : Enum = keys  # TODO: Redundent?
        self.model              : Generic[ModelType, QueryType] = model
        self.access_property    : str = access_property

    def __getattr__(self, name: Enum) -> object:

        with session_scope() as session:

            if not (_name := getattr(self.keys, name, None)):
                raise AttributeError(f"{name} is not a valid attribute")

            if not (query := self.model.get_fm_name(session, _name)):
                raise NoResultFound(f"Query '{name}' returned no results.")

            return getattr(query, self.access_property)

    def __getitem__(self, name: Enum) -> object:

        with session_scope() as session:

            if not (_name := getattr(self.keys, name.name, None)):
                raise AttributeError(f"{name} is not a valid attribute")

            if not (query := self.model.get_fm_name(session, _name)):
                raise NoResultFound(f"Query '{name}' returned no results.")

            return getattr(query, self.access_property)

    @property
    def random(self) -> object:
        with session_scope() as session:

            if not (query := self.model.get_fm_random(session)):
                raise NoResultFound(f"Query returned no results.")

            return getattr(query, self.access_property)

    @property
    def all(self) -> List[object]:
        with session_scope() as session:

            if not (query := self.model.gets_all(session)):
                raise NoResultFound(f"Query returned no results.")

            return [getattr(row, self.access_property) for row in query]

    def fm_id(self, id: int):
        with session_scope() as session:

            if not (query := self.model.get_fm_id(session, id)):
                raise NoResultFound(f"Query returned no results.")

            return getattr(query, self.access_property)

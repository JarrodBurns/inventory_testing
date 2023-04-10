
from enum import Enum
from typing import Generic, List, TypeVar

from sqlalchemy.orm.exc import NoResultFound

from _db_models import ModelBase, QueryBase
from _db_utils import session_scope

ModelType = TypeVar('ModelType', bound=ModelBase)
QueryType = TypeVar('QueryType', bound=QueryBase)


class AccessWrapper:

    def __init__(self, keys, model, result_converter):
        self.keys               : Enum = keys  # TODO: Redundent?
        self.model              : Generic[ModelType, QueryType] = model
        self.result_converter = result_converter

    def __getattr__(self, name: Enum) -> object:

        with session_scope() as session:

            if not (_name := getattr(self.keys, name, None)):
                raise AttributeError(f"{name} is not a valid attribute")

            if not (query := self.model.get_fm_name(session, _name)):
                raise NoResultFound(f"Query '{name}' returned no results.")

            return self.result_converter(query)

    def __getitem__(self, name: Enum) -> object:

        with session_scope() as session:

            if not (_name := getattr(self.keys, name.name, None)):
                raise AttributeError(f"{name} is not a valid attribute")

            if not (query := self.model.get_fm_name(session, _name)):
                raise NoResultFound(f"Query '{name}' returned no results.")

            return self.result_converter(query)

    @property
    def random(self) -> object:
        with session_scope() as session:

            if not (query := self.model.get_fm_random(session)):
                raise NoResultFound(f"Query returned no results.")

            return self.result_converter(query)

    @property
    def all_results(self) -> List[object]:
        with session_scope() as session:

            if not (query := self.model.gets_all(session)):
                raise NoResultFound(f"Query returned no results.")

            return [self.result_converter(row) for row in query]

    def get_fm_id(self, id: int) -> object:
        with session_scope() as session:

            if not (query := self.model.get_fm_id(session, id)):
                raise NoResultFound(f"Query returned no results.")

            return self.result_converter(query)

    def get_fm_name(self, name: Enum) -> object:
        with session_scope() as session:

            if not (query := self.model.get_fm_name(session, name)):
                raise NoResultFound(f"Query returned no results.")

            return self.result_converter(query)

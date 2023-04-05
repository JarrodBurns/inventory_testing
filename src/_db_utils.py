
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, declarative_base


DATABASE    = "sqlite:///example.db"
ENGINE      = create_engine(DATABASE)
Session     = sessionmaker(bind=ENGINE)


@contextmanager
def session_scope() -> Session:
    session = Session()

    try:
        yield session
        session.commit()

    except:
        session.rollback()
        raise

    finally:
        session.close()


class SingletonModelBase:
    _model_base = None

    @classmethod
    def get_instance(cls):
        if cls._model_base is None:
            cls._model_base = declarative_base()
        return cls._model_base

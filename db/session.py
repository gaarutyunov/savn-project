from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session as SQLSession

from .models.base import BaseModel, Base

engine: Engine = None

Session: SQLSession = None


def check_instance():
    if engine is None:
        raise Exception('engine must be initiated')

    if Session is None:
        raise Exception('Session must be initiated')


def connect(conn: str):
    global engine
    global Session
    if engine is not None or Session is not None:
        raise Exception('cannot initialize db twice')

    engine = create_engine(conn, echo=True, future=True)
    Base.metadata.bind = engine
    Session = sessionmaker(engine)


def add_one(obj: BaseModel):
    with Session.begin() as session:
        session.add(obj)

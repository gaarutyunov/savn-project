import re
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session as SQLSession

from .models.base import BaseModel

from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.expression import Insert, text

__DO_UPDATE__ = 'ON CONFLICT ("slug") DO UPDATE SET updated_at = now()'
__DO_UPDATE_REF__ = "ON CONFLICT (%s, %s) DO UPDATE SET updated_at = now()"
__RETURNING__ = "RETURNING"
__REF_TABLE_REGEXP__ = (
    r"INSERT INTO (?P<schema>[a-z]+).t_(?P<primary>[a-z]+)_(?P<foreign>[a-z]+)"
)


@compiles(Insert)
def prefix_inserts(insert, compiler, **kw):
    """Compile function for INSERT operations.

    It updates rows that already exist.
    Can handle normal tables and tables holding many-to-many reference.

    :param insert: insert statement
    :param compiler: statements compiler
    :param kw: other arguments
    :return: UPSERT operation
    """
    visited: str = compiler.visit_insert(insert, **kw)

    match = re.match(__REF_TABLE_REGEXP__, visited)
    if match:
        update_str = __DO_UPDATE_REF__ % (
            match.group("primary") + "_id",
            match.group("foreign") + "_id",
        )
    else:
        update_str = __DO_UPDATE__

    if __RETURNING__ in visited:
        idx = visited.find(__RETURNING__)
        return visited[:idx] + update_str + " " + visited[idx:]

    return visited + " " + __DO_UPDATE__


engine: Optional[Engine] = None

Session: Optional[SQLSession] = None


def check_instance():
    """Checks whether engine and session are instantiated."""
    if engine is None:
        raise Exception("engine must be initiated")

    if Session is None:
        raise Exception("Session must be initiated")


def connect(conn: str):
    """Connects to database using :class:`sqlalchemy.orm.sessionmaker`

    :param conn: connection string
    """
    global engine
    global Session
    if engine is not None or Session is not None:
        raise Exception("cannot initialize db twice")

    engine = create_engine(conn, echo=True, future=True)
    BaseModel.metadata.bind = engine
    Session = sessionmaker(engine)


def add_one(obj: BaseModel):
    """Add one instance to database

    :param obj: an instance extending :class:`.models.base.BaseModel`
    """
    check_instance()
    with Session.begin() as session:
        session.add(obj)


def query(stmt: str):
    """Iterate over results of raw sql statement
    :param stmt: raw SQL
    """
    check_instance()

    sql = text(stmt)

    with Session.begin() as session:
        for row in session.execute(sql):
            yield row

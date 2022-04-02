import re
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session as SQLSession

from github.db.models.base import BaseModel

from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.expression import Insert, text

__DO_UPDATE__ = "ON CONFLICT (%s) DO UPDATE SET updated_at = now()"
__RETURNING__ = "RETURNING"
__TABLE_REGEXP__ = r"INSERT INTO (?P<schema>[a-z]+).t_(?P<model>[a-z]+)"

__CONSTRAINTS_MAP__ = {
    "user": "login",
    "comment": "external_id",
    "review": "external_id",
    "request": "number",
    "repository": "owner, name",
}


@compiles(Insert)
def prefix_inserts(insert, compiler, **kw):
    """Compile function for INSERT operations.

    It updates rows that already exist.

    :param insert: insert statement
    :param compiler: statements compiler
    :param kw: other arguments
    :return: UPSERT operation
    """
    visited: str = compiler.visit_insert(insert, **kw)

    match = re.match(__TABLE_REGEXP__, visited)
    if not match:
        return visited

    constraint = __CONSTRAINTS_MAP__[match.get("model")]
    if constraint is None:
        return visited

    update_str = __DO_UPDATE__ % constraint

    idx = visited.find(__RETURNING__)
    if idx > -1:
        return visited[:idx] + update_str + " " + visited[idx:]

    return visited + " " + update_str


engine: Optional[Engine] = None

Session: Optional[SQLSession] = None


def check_instance():
    """Checks whether engine and session are instantiated."""
    assert engine is not None, "engine must be initiated"
    assert Session is not None, "Session must be initiated"


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

    :param obj: an instance extending :class:`github.db.models.base.BaseModel`
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

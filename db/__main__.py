import argparse
import os
from typing import Union

from db.models import BaseModel, User, Request, Comment, Review, Repository
from db.routines import ROUTINES
from db.session import connect, check_instance, engine

from sqlalchemy import event, DDL

from db.views import VIEWS


def create_all(args: argparse.Namespace):
    """Creates or updates database schema

    :param args: command-line arguments
    """
    check_instance()

    if args.drop:
        BaseModel.metadata.drop_all(engine)

    event.listen(
        BaseModel.metadata,
        "before_create",
        DDL("CREATE SCHEMA IF NOT EXISTS %s" % BaseModel.metadata.schema),
    )

    for view in VIEWS:
        event.listen(
            BaseModel.metadata,
            "after_create",
            DDL(view),
        )

    for routine in ROUTINES:
        event.listen(
            BaseModel.metadata,
            "after_create",
            DDL(routine),
        )

    BaseModel.metadata.create_all(engine)


def main(args: argparse.Namespace):
    """Entry point for db module.

    Creates or updates database schema.

    :param args: command-line arguments
    """
    connect(args.conn)

    create_all(args)


def coerce_bool(arg: Union[bool, str]):
    if type(arg) == bool:
        return arg
    return arg.strip() != "false"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--conn",
        "-c",
        type=str,
        help="PostgreSQL connection string",
        default=os.environ.get("PG_CONN"),
    )
    parser.add_argument(
        "--drop",
        "-d",
        type=coerce_bool,
        help="Drop schema before create",
        default=False,
    )

    parsed_args = parser.parse_args()

    main(parsed_args)

import argparse

from db.models import (
    BaseModel,
)
from db.procedures import PROCEDURES
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
        event.listen(BaseModel.metadata, "after_create", DDL(view))

    for procedure in PROCEDURES:
        event.listen(BaseModel.metadata, "after_create", DDL(procedure))

    BaseModel.metadata.create_all(engine)


def main(args: argparse.Namespace):
    """Entry point for db module.

    Creates or updates database schema.

    :param args: command-line arguments
    """
    connect(args.conn)

    create_all(args)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--conn", "-c", type=str, help="PostgreSQL connection string")
    parser.add_argument("--drop", "-d", type=bool, help="Drop schema before create")

    parsed_args = parser.parse_args()

    main(parsed_args)

import argparse

from sqlalchemy.sql.ddl import DropSchema

from db.models import BaseModel, Competition, Tag, Team
from db.session import connect, check_instance, engine

from sqlalchemy import event, DDL


def create_all(args: argparse.Namespace):
    check_instance()

    if args.drop:
        event.listen(BaseModel.metadata, 'before_create', DropSchema(BaseModel.metadata.schema, cascade=True))

    event.listen(BaseModel.metadata, 'before_create', DDL("CREATE SCHEMA IF NOT EXISTS %s" % BaseModel.metadata.schema))

    BaseModel.metadata.create_all(engine)


def main(args: argparse.Namespace):
    connect(args.conn)

    create_all(args)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--conn', '-c', type=str, help='PostgreSQL connection string')
    parser.add_argument('--drop', '-d', type=bool, help='Drop schema before create')

    parsed_args = parser.parse_args()

    main(parsed_args)

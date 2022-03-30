import argparse

from db.models import *
from db.session import connect, check_instance, engine

from sqlalchemy import event
from sqlalchemy.schema import CreateSchema


def create_all():
    check_instance()

    event.listen(BaseModel.metadata, 'before_create', CreateSchema(BaseModel.metadata.schema))

    BaseModel.metadata.create_all(engine)


def main(args):
    connect(args.conn)

    create_all()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--conn', '-c', type=str, help='PostgreSQL connection string')

    args = parser.parse_args()

    main(args)

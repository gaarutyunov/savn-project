import argparse

import kaggle

from db.models import Competition
from db.session import connect, add_one


def main(args):
    connect(args)

    competitions = kaggle.api.competitions_list(page=1)

    for comp in competitions:
        ref: str = comp.ref
        obj = Competition(slug=ref.split('/')[1])
        add_one(obj)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--conn', '-c', type=str, help='PostgreSQL connection string')

    args = parser.parse_args()

    main(args)

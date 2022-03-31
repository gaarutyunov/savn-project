import argparse

from kaggle.db.session import connect
from kaggle.parse.competitions import parse_competitions


def main(args):
    """Entry point for parsing module.

    Parses Kaggle competitions, tags and teams.

    :param args: command-line arguments
    """
    connect(args.conn)

    parse_competitions()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--conn", "-c", type=str, help="PostgreSQL connection string")

    args = parser.parse_args()

    main(args)

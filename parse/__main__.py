import argparse
import asyncio
import logging
import os

from ..db.session import connect
from .pull_request import parse_pull_requests


def main(args):
    """Entry point for parsing module.

    Parses GitHub pull requests, reviews, comments and their authors for specified repository

    :param args: command-line arguments
    """
    logging.basicConfig(
        filename=args.log,
        filemode="a",
        format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
        datefmt="%H:%M:%S",
        level=logging.DEBUG,
    )
    session = connect(args.conn)

    asyncio.run(
        parse_pull_requests(session, args.token, args.owner, args.name, args.n_comments, args.after)
    )


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
        "--token",
        "-t",
        type=str,
        help="GitHub token",
        default=os.environ.get("GITHUB_TOKEN"),
    )
    parser.add_argument("--owner", "-o", type=str, help="GitHub repository owner")
    parser.add_argument("--name", "-r", type=str, help="GitHub repository name")
    parser.add_argument(
        "--log", "-l", type=str, help="Log file name", default="parse.log"
    )
    parser.add_argument(
        "--after", "-a", type=str, help="After for cursor", default=None
    )
    parser.add_argument(
        "--n_comments",
        "-n",
        type=int,
        help="Min number of comments in pull request",
        default=20,
    )

    args = parser.parse_args()

    main(args)

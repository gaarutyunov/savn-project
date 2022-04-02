import argparse
import asyncio
import os

from github.db.session import connect
from github.parse.pull_request import parse_pull_requests


def main(args):
    """Entry point for parsing module.

    Parses GitHub pull requests, reviews, comments and their authors for specified repository

    :param args: command-line arguments
    """
    connect(args.conn)

    asyncio.run(parse_pull_requests(args.token, args.owner, args.name, args.n_comments))


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
        "--n_comments", "-n", type=str, help="Min number of comments in pull request"
    )

    args = parser.parse_args()

    main(args)

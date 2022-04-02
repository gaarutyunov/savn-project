from github.api.pull_request import fetch_pull_requests, parse_all
from github.db.models import Repository
from github.db.session import add_one


async def parse_pull_requests(token: str, owner: str, name: str, n_comments: int):
    repo = Repository(owner=owner, name=name)

    add_one(repo)

    async for prs in fetch_pull_requests(token, repo, n_comments):
        for pr in parse_all(repo, prs):
            add_one(pr)

from github.api.pull_request import fetch_pull_requests, parse_all
from github.db.models import Repository
from github.db.session import commit


async def parse_pull_requests(
    session, token: str, owner: str, name: str, n_comments: int, after: str
):
    repo = Repository.as_unique(session, owner=owner, name=name)

    commit()

    async for prs in fetch_pull_requests(token, repo, n_comments, after):
        for _ in parse_all(session, repo, prs):
            commit()

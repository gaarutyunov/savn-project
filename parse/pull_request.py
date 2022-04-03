from api.pull_request import fetch_pull_requests, parse_all
from db.models import Repository
from db.session import Session


async def parse_pull_requests(
    session: Session, token: str, owner: str, name: str, n_comments: int, after: str
):
    """Parse pull requests and other objects from given repository

    :param session: SQLAlchemy Session instance
    :param token: GitHub access token
    :param owner: Repository owner
    :param name: Repository name
    :param n_comments: Number of minimum comments in pull request
    :param after: endCursor to start parsing from specific page
    """
    repo = Repository.as_unique(session, owner=owner, name=name)

    session.commit()

    async for prs in fetch_pull_requests(token, repo, n_comments, after):
        for _ in parse_all(session, repo, prs):
            session.commit()

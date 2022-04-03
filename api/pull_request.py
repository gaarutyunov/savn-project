import logging
from typing import Generator, Any, AsyncGenerator

from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from sqlalchemy.orm import Session

from ..db.models import Repository, Request, Review, User, Comment

__GITHUB_GRAPHQL_URL__ = "https://api.github.com/graphql"


__GITHUB_PULL_REQUEST_QUERY__ = """query ($query: String!, $after: String) {
    search(query: $query, type: ISSUE, first: 10, after: $after) {
        issueCount
        pageInfo {
            startCursor
            hasNextPage
            endCursor
        }
        edges {
            node {
                ... on PullRequest {
                    title
                    number
                    author {
                        login
                    }
                    reviews(first: 100) {
                        totalCount
                        pageInfo {
                            startCursor
                            hasNextPage
                            endCursor
                        }
                        nodes {
                            databaseId
                            body
                            author {
                                login
                            }
                            comments(first: 10) {
                                totalCount
                                pageInfo {
                                    startCursor
                                    hasNextPage
                                    endCursor
                                }
                                nodes {
                                    databaseId
                                    body
                                    author {
                                        login
                                    }
                                    replyTo {
                                        databaseId
                                        body
                                        author {
                                            login
                                        }
                                    }
                                }
                            }   
                        }
                    }
                }
            }
        }
    }
}"""


async def fetch_pull_requests(
    token: str, repository: Repository, n_comments: int, after: str
) -> AsyncGenerator[Any, list[dict]]:
    """Async function to retrieve pull requests from GitHub repository

    :param token: GitHub access token
    :param repository: Repository model
    :param n_comments: Number of minimum comments in pull request
    :param after: endCursor to start parsing from specific page
    """
    transport = AIOHTTPTransport(
        url=__GITHUB_GRAPHQL_URL__, headers={"Authorization": "Bearer " + token}
    )

    query = "is:pr repo:%s/%s comments:>%d" % (
        repository.owner,
        repository.name,
        n_comments,
    )

    async with Client(transport=transport) as session:
        graph_query = gql(__GITHUB_PULL_REQUEST_QUERY__)

        variables = {"query": query, "after": after}

        has_next_page = True

        while has_next_page:
            result = await session.execute(graph_query, variable_values=variables)

            if "errors" in result:
                raise StopIteration(result["errors"])

            has_next_page = result["search"]["pageInfo"]["hasNextPage"]
            end_cursor = result["search"]["pageInfo"]["endCursor"]

            logging.info(
                "Finished with %s. Moving to %s" % (variables["after"], end_cursor)
            )

            variables["after"] = end_cursor

            yield result["search"]["edges"]


def parse_all(
    session: Session, repository: Repository, requests: list[dict]
) -> Generator[Any, Request, None]:
    """Parses Pull Requests, Reviews, Comments and their Authors from GitHub response

    :param session: SQLAlchemy Session instance
    :param repository: Repository model
    :param requests: list of retrieved pull requests
    """
    for pr_node in requests:
        pr = pr_node["node"]
        pr_model = Request.as_unique(
            session,
            number=pr["number"],
            title=pr["title"],
            author=User.as_unique(session, login=pr["author"]["login"]),
            repository=repository,
        )

        for r_node in pr["reviews"]["nodes"]:
            r_model = Review.as_unique(
                session,
                external_id=r_node["databaseId"],
                body=r_node["body"],
                author=User.as_unique(session, login=r_node["author"]["login"]),
            )

            pr_model.reviews.append(r_model)

            for c_node in r_node["comments"]["nodes"]:
                reply_to = None
                if c_node["replyTo"] is not None:
                    reply_to = Comment.as_unique(
                        session,
                        external_id=c_node["replyTo"]["databaseId"],
                        body=c_node["replyTo"]["body"],
                        author=User.as_unique(
                            session, login=c_node["replyTo"]["author"]["login"]
                        ),
                        review=r_model,
                    )

                c_model = Comment.as_unique(
                    session,
                    external_id=c_node["databaseId"],
                    body=c_node["body"],
                    author=User.as_unique(session, login=c_node["author"]["login"]),
                    reply_to=reply_to,
                )

                r_model.comments.append(c_model)
                if reply_to is not None:
                    r_model.comments.append(reply_to)

        yield pr_model

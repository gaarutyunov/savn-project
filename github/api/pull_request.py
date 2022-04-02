import logging
from typing import Optional, Generator, Any, AsyncGenerator

from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport

from github.db.models import Repository, Request, Review, User, Comment

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
    token: str, repository: Repository, n_comments: int
) -> AsyncGenerator[Any, list[dict]]:
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

        variables = {"query": query, "after": None}

        result: Optional[dict] = None

        while result is None or result["data"]["search"]["pageInfo"]["hasNextPage"]:
            result = await session.execute(graph_query, variable_values=variables)

            if "errors" in result:
                raise StopIteration(result["errors"])

            end_cursor = result["search"]["pageInfo"]["endCursor"]

            logging.info(
                "Finished with %s. Moving to %s" % (variables["after"], end_cursor)
            )

            variables["after"] = end_cursor

            yield result["search"]["edges"]


def parse_all(
    session, repository: Repository, requests: list[dict]
) -> Generator[Any, Request, None]:
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
                c_model = Comment.as_unique(
                    session,
                    external_id=c_node["databaseId"],
                    body=c_node["body"],
                    author=User.as_unique(session, login=c_node["author"]["login"]),
                    reply_to=Comment.as_unique(
                        session,
                        external_id=c_node["replyTo"]["databaseId"],
                        body=c_node["replyTo"]["body"],
                        author=User.as_unique(
                            session, login=c_node["replyTo"]["author"]["login"]
                        ),
                    )
                    if c_node["replyTo"] is not None
                    else None,
                )

                r_model.comments.append(c_model)

        yield pr_model

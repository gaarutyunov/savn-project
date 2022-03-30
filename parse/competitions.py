import kaggle
from sqlalchemy.sql.functions import now

from db.models import Competition, CompetitionTeam, Team, CompetitionTag, Tag
from db.session import add_one


def iter_competitions():
    """Iterator over Kaggle competitions.

    Is handy for pagination handling.
    """
    page = 1
    competitions = kaggle.api.competitions_list(page=page)

    while len(competitions) != 0:
        for comp in competitions:
            yield comp

        page += 1
        competitions = kaggle.api.competitions_list(page=page)


def parse_competitions():
    """Parses all competitions, associated tags and participating teams.

    Saves them to database without duplications and preserving all relations.
    """
    for comp in iter_competitions():
        ref: str = comp.ref
        slug = ref.split("/")[1]

        obj = Competition(slug=slug, created_at=now(), updated_at=now())

        leaderboard = kaggle.api.competition_view_leaderboard(slug)

        for submission in leaderboard["submissions"]:
            obj.teams.append(
                CompetitionTeam(
                    team=Team(
                        slug=submission["teamName"], created_at=now(), updated_at=now()
                    ),
                    created_at=now(),
                    updated_at=now(),
                )
            )

        for tag in comp.tags:
            obj.tags.append(
                CompetitionTag(
                    tag=Tag(slug=tag.name, created_at=now(), updated_at=now()),
                    created_at=now(),
                    updated_at=now(),
                )
            )

        add_one(obj)

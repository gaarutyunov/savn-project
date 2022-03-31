from sqlalchemy import Column, String, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from .base import BaseModel


class Team(BaseModel):
    """Team that participates in Kaggle competition"""

    __tablename__ = "t_team"

    slug = Column(String, nullable=False, unique=True, index=True)

    competitions = relationship("CompetitionTeam", backref="teams")


class CompetitionTeam(BaseModel):
    """Many-to-many relationship between competitions and teams"""

    __tablename__ = "t_competition_team"

    __table_args__ = (UniqueConstraint("competition_id", "team_id"),)

    competition_id = Column(
        Integer,
        ForeignKey("t_competition.id"),
        nullable=False,
        primary_key=True,
    )
    team_id = Column(
        Integer,
        ForeignKey("t_team.id"),
        nullable=False,
        primary_key=True,
    )

    team = relationship("Team")
    competition = relationship("Competition")

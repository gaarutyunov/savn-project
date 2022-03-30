from typing import Any

from sqlalchemy import Column, String, Integer, ForeignKey

from .base import BaseModel


class Team(BaseModel):
    __tablename__ = 't_team'

    name = Column(String, nullable=False, unique=True)
    competitions: Any


class CompetitionTeam(BaseModel):
    __tablename__ = 't_competition_team'

    competition_id = Column(Integer, ForeignKey('t_competition.id'), nullable=False, index=True)
    team_id = Column(Integer, ForeignKey('t_team.id'), nullable=False, index=True)

from typing import Any

from sqlalchemy import Column, String, Integer, ForeignKey

from .base import BaseModel


class Tag(BaseModel):
    __tablename__ = 't_tag'

    name = Column(String, nullable=False, unique=True, index=True)
    competitions: Any


class CompetitionTag(BaseModel):
    __tablename__ = 't_competition_tag'

    competition_id = Column(Integer, ForeignKey('t_competition.id'), nullable=False, index=True)
    tag_id = Column(Integer, ForeignKey('t_tag.id'), nullable=False, index=True)

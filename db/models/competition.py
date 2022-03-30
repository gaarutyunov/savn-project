from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from .base import BaseModel


class Competition(BaseModel):
    __tablename__ = 't_competition'

    slug = Column(String, nullable=False, unique=True, index=True)

    tags = relationship('Tag', secondary='t_competition_tag', backref='competitions')
    teams = relationship('Team', secondary='t_competition_team', backref='competitions')

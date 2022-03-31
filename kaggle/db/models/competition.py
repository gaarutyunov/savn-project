from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from .base import BaseModel


class Competition(BaseModel):
    """Model for Kaggle competition object"""

    __tablename__ = "t_competition"

    slug = Column(String, nullable=False, unique=True, index=True)

    tags = relationship("CompetitionTag", backref="competitions")
    teams = relationship("CompetitionTeam", backref="competitions")

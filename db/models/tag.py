from sqlalchemy import Column, String, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from .base import BaseModel


class Tag(BaseModel):
    """Model for a tag of a Kaggle competition"""

    __tablename__ = "t_tag"

    slug = Column(String, nullable=False, unique=True, index=True)

    competitions = relationship("CompetitionTag", backref="tags")


class CompetitionTag(BaseModel):
    """Many-to-many relationship between Competition and Tag"""

    __tablename__ = "t_competition_tag"

    __table_args__ = (UniqueConstraint("competition_id", "tag_id"),)

    competition_id = Column(
        Integer,
        ForeignKey("t_competition.id"),
        nullable=False,
        primary_key=True,
    )
    tag_id = Column(
        Integer,
        ForeignKey("t_tag.id"),
        nullable=False,
        primary_key=True,
    )

    tag = relationship("Tag")
    competition = relationship("Competition")

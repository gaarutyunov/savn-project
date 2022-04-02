from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from github.db.models.base import BaseModel


class User(BaseModel):
    """Model for Github user"""

    __tablename__ = "t_user"

    login = Column(String, nullable=False, unique=True, index=True)

    requests = relationship("Request", backref="author")
    reviews = relationship("Review", backref="author")
    comments = relationship("Comment", backref="author")

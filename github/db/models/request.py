from sqlalchemy import Integer, Column, String, ForeignKey
from sqlalchemy.orm import relationship

from github.db.models.base import BaseModel


class Request(BaseModel):
    """Model for GitHub pull request"""

    __tablename__ = "t_request"

    number = Column(Integer, nullable=False, unique=True, index=True)
    title = Column(String)

    repository_id = Column(Integer, ForeignKey("t_repository.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("t_user.id"), nullable=False)

    repository = relationship("Repository", backref="requests")
    author = relationship("Author", backref="requests")
    reviews = relationship("Review", backref="request")

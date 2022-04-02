from sqlalchemy import Integer, Column, ForeignKey, String
from sqlalchemy.orm import relationship

from github.db.models.base import BaseModel


class Review(BaseModel):
    """Model for GitHub pull request review"""

    __tablename__ = "t_review"

    external_id = Column(Integer, nullable=False, unique=True, index=True)
    body = Column(String)

    request_id = Column(Integer, ForeignKey("t_request.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("t_user.id"), nullable=False)

    request = relationship("Request", backref="reviews")
    author = relationship("Author", backref="reviews")
    comments = relationship("Comment", backref="review")

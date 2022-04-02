from sqlalchemy import Integer, Column, ForeignKey, String
from sqlalchemy.orm import relationship, backref

from github.db.models.base import BaseModel


class Comment(BaseModel):
    """Model for GitHub review comment"""

    __tablename__ = "t_comment"

    external_id = Column(Integer, nullable=False, unique=True, index=True)
    body = Column(String)

    review_id = Column(Integer, ForeignKey("t_review.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("t_user.id"), nullable=False)
    reply_to_id = Column(Integer, ForeignKey("t_comment.id"))

    review = relationship("Review", backref="comments")
    author = relationship("Author", backref="comments")

    reply_to = relationship("Comment", backref="replies", remote_side=[id])
    replies = relationship("Comment", backref=backref("reply_to", remote_side=[id]))

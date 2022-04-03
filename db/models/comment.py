from sqlalchemy import Integer, Column, ForeignKey, String
from sqlalchemy.orm import relationship, backref

from .base import BaseModel
from ..unique import UniqueMixin


class Comment(BaseModel, UniqueMixin):
    """Model for GitHub review comment"""

    __tablename__ = "t_comment"

    external_id = Column(Integer, nullable=False, unique=True, index=True)
    body = Column(String)

    review_id = Column(Integer, ForeignKey("t_review.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("t_user.id"), nullable=False)
    reply_to_id = Column(Integer, ForeignKey("t_comment.id"))

    author = relationship("User", backref="comments")

    reply_to = relationship("Comment", remote_side="Comment.id")

    def __repr__(self) -> str:
        return super()._repr(external_id=self.external_id)

    @classmethod
    def unique_hash(cls, external_id, **kwargs):
        return external_id

    @classmethod
    def unique_filter(cls, query, external_id, **kwargs):
        return query.filter(Comment.external_id == external_id)

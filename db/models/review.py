from sqlalchemy import Integer, Column, ForeignKey, String
from sqlalchemy.orm import relationship

from db.models.base import BaseModel
from db.unique import UniqueMixin


class Review(BaseModel, UniqueMixin):
    """Model for GitHub pull request review"""

    __tablename__ = "t_review"

    external_id = Column(Integer, nullable=False, unique=True, index=True)
    body = Column(String)

    request_id = Column(Integer, ForeignKey("t_request.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("t_user.id"), nullable=False)

    author = relationship("User", backref="reviews")
    comments = relationship("Comment", backref="review", uselist=True)

    def __repr__(self) -> str:
        return super()._repr(external_id=self.external_id)

    @classmethod
    def unique_hash(cls, external_id, **kwargs):
        return external_id

    @classmethod
    def unique_filter(cls, query, external_id, **kwargs):
        return query.filter(Review.external_id == external_id)

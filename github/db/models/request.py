from sqlalchemy import Integer, Column, String, ForeignKey
from sqlalchemy.orm import relationship

from github.db.models.base import BaseModel
from github.db.unique import UniqueMixin


class Request(BaseModel, UniqueMixin):
    """Model for GitHub pull request"""

    __tablename__ = "t_request"

    number = Column(Integer, nullable=False, unique=True, index=True)
    title = Column(String)

    repository_id = Column(Integer, ForeignKey("t_repository.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("t_user.id"), nullable=False)

    repository = relationship("Repository", backref="requests")
    author = relationship("User", backref="requests")
    reviews = relationship("Review", backref="request", uselist=True)

    def __repr__(self) -> str:
        return super()._repr(number=self.number)

    @classmethod
    def unique_hash(cls, number, **kwargs):
        return number

    @classmethod
    def unique_filter(cls, query, number, **kwargs):
        return query.filter(Request.number == number)

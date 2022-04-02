from sqlalchemy import Column, String, UniqueConstraint

from github.db.models.base import BaseModel
from github.db.unique import UniqueMixin


class Repository(BaseModel, UniqueMixin):
    """Model for GitHub repository"""

    __tablename__ = "t_repository"

    __table_args__ = (UniqueConstraint("owner", "name"),)

    owner = Column(String, nullable=False, unique=True, index=True)
    name = Column(String, nullable=False, index=True)

    def __repr__(self) -> str:
        return super()._repr(owner=self.owner, name=self.name)

    @classmethod
    def unique_hash(cls, owner, name):
        return owner + "/" + name

    @classmethod
    def unique_filter(cls, query, owner, name):
        return query.filter(Repository.owner == owner, Repository.name == name)

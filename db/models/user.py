from sqlalchemy import Column, String

from db.models.base import BaseModel
from db.unique import UniqueMixin


class User(BaseModel, UniqueMixin):
    """Model for Github user"""

    __tablename__ = "t_user"

    login = Column(String, nullable=False, unique=True, index=True)

    def __repr__(self) -> str:
        return super()._repr(login=self.login)

    @classmethod
    def unique_hash(cls, login, **kwargs):
        return login

    @classmethod
    def unique_filter(cls, query, login, **kwargs):
        return query.filter(User.login == login)

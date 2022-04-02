from sqlalchemy import Column, String, UniqueConstraint
from sqlalchemy.orm import relationship

from github.db.models.base import BaseModel


class Repository(BaseModel):
    """Model for GitHub repository"""

    __tablename__ = "t_repository"

    __table_args__ = (UniqueConstraint("owner", "name"),)

    owner = Column(String, nullable=False, unique=True, index=True)
    name = Column(String, nullable=False, index=True)

    requests = relationship("Request", backref="repository")

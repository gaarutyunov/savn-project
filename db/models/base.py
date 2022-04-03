from typing import Any

from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, MetaData
from sqlalchemy.orm.exc import DetachedInstanceError
from sqlalchemy.sql.functions import now

metadata_obj = MetaData(schema="github")

Base = declarative_base(metadata=metadata_obj)


class BaseModel(Base):
    """Base model for database objects with common properties"""

    __abstract__ = True

    id = Column(
        Integer, nullable=False, unique=True, primary_key=True, autoincrement=True
    )
    created_at = Column(TIMESTAMP, nullable=False, default=now())
    updated_at = Column(TIMESTAMP, nullable=False, default=now())

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def __repr__(self) -> str:
        return self._repr(id=self.id)

    def _repr(self, **fields: dict[str, Any]) -> str:
        """Helper for __repr__"""
        field_strings = []
        at_least_one_attached_attribute = False
        for key, field in fields.items():
            try:
                field_strings.append(f"{key}={field!r}")
            except DetachedInstanceError:
                field_strings.append(f"{key}=DetachedInstanceError")
            else:
                at_least_one_attached_attribute = True
        if at_least_one_attached_attribute:
            return f"<{self.__class__.__name__}({','.join(field_strings)})>"
        return f"<{self.__class__.__name__} {id(self)}>"

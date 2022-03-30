from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, MetaData

metadata_obj = MetaData(schema="comp")

Base = declarative_base(metadata=metadata_obj)


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)

    def __repr__(self):
        return "<{0.__class__.__name__}(id={0.id!r})>".format(self)

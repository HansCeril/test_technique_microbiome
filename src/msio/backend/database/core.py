from typing import Any

from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

POSTGRES_INDEXES_NAMING_CONVENTION = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}

metadata_obj = MetaData(naming_convention=POSTGRES_INDEXES_NAMING_CONVENTION)


class Base(DeclarativeBase):
    """Defines the SQLAlchemy base DB class."""

    __mapper_args__ = {"eager_defaults": True}
    metadata = metadata_obj

    def dict(self) -> dict[str, Any]:
        """
        Returns a dict representation of a model.

        Returns
        -------
        dict[str, Any]
            The dictionary containing the key-value data of a model
        """
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

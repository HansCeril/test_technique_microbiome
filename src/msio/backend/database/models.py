from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship
from .core import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    metabolites = relationship("Metabolite", back_populates="uploader_user_id")


class Metabolite(Base):
    __tablename__ = "metabolites"

    id = Column(Integer, primary_key=True, index=True)

    feature = Column(String, nullable=False, unique=True, index=True)
    identification_level = Column(Integer, nullable=False, default=3)

    id_inchi = Column(String, unique=True, nullable=True)
    cas_number = Column(String, unique=True, nullable=True)

    method = Column(String, nullable=False)
    sample_data = Column(String, nullable=True)  # could be float or 'ND'/'NA'

    uploader_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    uploader_user_id = relationship("User", back_populates="metabolites")

    __table_args__ = (
        UniqueConstraint("id_inchi", name="uniq_id_inchi"),
        UniqueConstraint("cas_number", name="uniq_cas_number"),
    )

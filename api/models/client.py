from sqlalchemy import Column, Integer, String, UniqueConstraint
from api.config import Base


class Client(Base):
    __tablename__ = 'client'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=True)
    address = Column(String, nullable=False)
    pesel = Column(String, nullable=True, unique=True)
    nip = Column(String, nullable=True, unique=True)

    __table_args__ = (
        UniqueConstraint('pesel', 'nip', name='uix_pesel_nip'),
    )

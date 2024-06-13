from sqlalchemy import Column, Integer, String
from api.config import Base


class Segment(Base):
    __tablename__ = 'segment'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from config import Base

class Segment(Base):
    __tablename__ = 'segment'
    name = Column(String, primary_key=True)
    description = Column(String, nullable=True)

    models = relationship("CarModel", back_populates="segment")

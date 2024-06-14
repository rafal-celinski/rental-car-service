from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from api.config import Base

class Segment(Base):
    __tablename__ = 'segment'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)

    models = relationship("CarModel", back_populates="segment")

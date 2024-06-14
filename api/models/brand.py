from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from api.config import Base

class Brand(Base):
    __tablename__ = 'brand'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)

    models = relationship("CarModel", back_populates="brand")

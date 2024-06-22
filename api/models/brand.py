from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from config import Base

class Brand(Base):
    __tablename__ = 'brand'
    name = Column(String, primary_key=True)
    logo = Column(String, nullable=True)

    models = relationship("CarModel", back_populates="brand")

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from api.config import Base

class CarModel(Base):
    __tablename__ = 'model'
    
    model_name = Column(String, primary_key=True)
    brand_name = Column(String, ForeignKey('brand.name'), primary_key=True)
    segment_name = Column(String, ForeignKey('segment.name'), nullable=False)

    brand = relationship("Brand", back_populates="models")
    segment = relationship("Segment", back_populates="models")

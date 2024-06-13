from sqlalchemy import Column, Integer, String, Date, Boolean
from sqlalchemy.orm import relationship
from api.config import Base


class Car(Base):
    __tablename__ = 'car'

    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String, nullable=False)
    brand_name = Column(String, nullable=False)
    segment_name = Column(String, nullable=False)
    production_date = Column(Date, nullable=False)
    mileage = Column(Integer, nullable=False)
    license_plate = Column(String, nullable=False, unique=True)
    vin = Column(String, nullable=False, unique=True)
    photo = Column(String, nullable=True)
    is_rented = Column(Boolean, default=False)

    rentals = relationship("Rental", back_populates="car")
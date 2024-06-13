from sqlalchemy import Column, Integer, Date, ForeignKey, Boolean, Numeric
from sqlalchemy.orm import relationship
from api.config import Base


class Rental(Base):
    __tablename__ = 'rental'

    id = Column(Integer, primary_key=True, index=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    price = Column(Numeric, nullable=False)
    active = Column(Boolean, default=True)
    car_id = Column(Integer, ForeignKey('car.id'))
    client_id = Column(Integer, nullable=False)

    car = relationship("Car", back_populates="rentals")

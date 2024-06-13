from sqlalchemy import Column, Integer, String
from api.config import Base


class CarModel(Base):
    __tablename__ = 'car_model'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)

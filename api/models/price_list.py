from sqlalchemy import Column, Integer, String, Numeric
from api.config import Base


class PriceList(Base):
    __tablename__ = 'price_list'

    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String, nullable=False)
    brand_name = Column(String, nullable=False)
    price = Column(Numeric, nullable=False)

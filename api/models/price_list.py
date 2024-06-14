from sqlalchemy import Column, String, Numeric
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Price(Base):
    __tablename__ = "price_list"
    
    model_name = Column(String(20), primary_key=True)
    brand_name = Column(String(20), primary_key=True)
    price = Column(Numeric)

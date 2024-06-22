from sqlalchemy import Column, Integer, Date, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from config import Base


class Invoice(Base):
    __tablename__ = "invoice"
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey('client.id'))
    date = Column(Date)
    price_sum_netto = Column(Numeric)
    tax = Column(Numeric)
    
    elements = relationship("InvoiceElement", back_populates="invoice")
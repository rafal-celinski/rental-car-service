from sqlalchemy import Column, Integer, Date, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from api.config import Base


class Invoice(Base):
    __tablename__ = 'invoice'

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    price_sum_netto = Column(Numeric, nullable=False, default=0)
    tax = Column(Numeric, nullable=False, default=0)

    invoice_elements = relationship("InvoiceElement", back_populates="invoice")

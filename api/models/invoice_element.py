from sqlalchemy import Column, Integer, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from api.config import Base


class InvoiceElement(Base):
    __tablename__ = 'invoice_element'

    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey('invoice.id'), nullable=False)
    rental_id = Column(Integer, ForeignKey('rental.id'), nullable=False)
    element_number = Column(Integer, nullable=False)
    price = Column(Numeric, nullable=False)
    car_id = Column(Integer, nullable=False)

    invoice = relationship("Invoice", back_populates="invoice_elements")
    rental = relationship("Rental")

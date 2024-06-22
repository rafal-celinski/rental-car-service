from sqlalchemy import Column, Integer, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from config import Base


class InvoiceElement(Base):
    __tablename__ = "invoice_element"
    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey('invoice.id'))
    rental_id = Column(Integer, ForeignKey('rental.id'))
    element_number = Column(Integer)
    price = Column(Numeric)
    car_id = Column(Integer, ForeignKey('car.id'))

    invoice = relationship("Invoice", back_populates="elements")
    car = relationship("Car")

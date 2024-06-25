from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from config import Base

class Client(Base):
    __tablename__ = 'client'
    id = Column(Integer, primary_key=True, index=True)
    address = Column(String)
    rentals = relationship("Rental", back_populates="client")

class Person(Client):
    __tablename__ = 'person'
    id = Column(Integer, ForeignKey('client.id'), primary_key=True)
    name = Column(String)
    surname = Column(String)
    pesel = Column(String)

class Company(Client):
    __tablename__ = 'company'
    id = Column(Integer, ForeignKey('client.id'), primary_key=True)
    name = Column(String)
    nip = Column(String)

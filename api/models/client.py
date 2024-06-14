from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Client(Base):
    __tablename__ = "client"
    id = Column(Integer, primary_key=True, index=True)
    address = Column(String)

    person = relationship("Person", back_populates="client", uselist=False)
    company = relationship("Company", back_populates="client", uselist=False)


class Person(Client):
    __tablename__ = "person"
    id = Column(Integer, ForeignKey('client.id'), primary_key=True)
    name = Column(String(20))
    surname = Column(String(20))
    pesel = Column(String(20))

    client = relationship("Client", back_populates="person")


class Company(Client):
    __tablename__ = "company"
    id = Column(Integer, ForeignKey('client.id'), primary_key=True)
    name = Column(String(20))
    nip = Column(String(20))

    client = relationship("Client", back_populates="company")

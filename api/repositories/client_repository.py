from sqlalchemy.orm import Session
from api.models.client import Person, Company, Client
from api.schemas.client_schema import Client as ClientSchema

class ClientRepository:

    @staticmethod
    def get_all(db: Session):
        clients = []

        persons = db.query(Person).all()
        companies = db.query(Company).all()

        for person in persons:
            client = db.query(Client).filter(Client.id == person.id).first()
            clients.append(ClientSchema(
                id=client.id,
                name=person.name,
                surname=person.surname,
                address=client.address,
                pesel=person.pesel,
                nip=None
            ))

        for company in companies:
            client = db.query(Client).filter(Client.id == company.id).first()
            clients.append(ClientSchema(
                id=client.id,
                name=company.name,
                surname=None,
                address=client.address,
                pesel=None,
                nip=company.nip
            ))

        return clients

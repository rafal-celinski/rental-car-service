from sqlalchemy.orm import Session
from models.client import Person, Company, Client
from schemas.client_schema import Client as ClientSchema, ClientCreate, ClientUpdate

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
    
    @staticmethod
    def get_person_by_pesel(db: Session, pesel: str) -> Person:
        return db.query(Person).filter(Person.pesel == pesel).first()

    @staticmethod
    def get_company_by_nip(db: Session, nip: str) -> Company:
        return db.query(Company).filter(Company.nip == nip).first()

    @staticmethod
    def create_person(db: Session, client: ClientCreate) -> Person:
        new_person = Person(
            name=client.name,
            address=client.address,
            surname=client.surname,
            pesel=client.pesel
        )
        db.add(new_person)
        db.commit()
        db.refresh(new_person)
        return new_person

    @staticmethod
    def create_company(db: Session, client: ClientCreate) -> Company:
        new_company = Company(
            name=client.name,
            address = client.address,
            nip=client.nip
        )
        db.add(new_company)
        db.commit()
        db.refresh(new_company)
        return new_company
    
    @staticmethod
    def update(db: Session, db_client, client_update:ClientUpdate):
        if isinstance(db_client, Person):
            if client_update.name:
                db_client.name = client_update.name
            if client_update.surname:
                db_client.surname = client_update.surname
            if client_update.address:
                db_client.address = client_update.address
        elif isinstance(db_client, Company):
            if client_update.name:
                db_client.name = client_update.name
            if client_update.address:
                db_client.address = client_update.address
        db.commit()
        db.refresh(db_client)
        return db_client


    @staticmethod
    def delete(db: Session, client):
        db.delete(client)
        db.commit()
        return client
    
    @staticmethod
    def get_by_id(db: Session, client_id: int):
        client = db.query(Client).filter(Client.id == client_id).first()
        if client:
            person = db.query(Person).filter(Person.id == client_id).first()
            if person:
                return person
            company = db.query(Company).filter(Company.id == client_id).first()
            if company:
                return company
        return None

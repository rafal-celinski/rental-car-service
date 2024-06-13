from sqlalchemy.orm import Session
from api.models.client import Client
from api.schemas.client_schema import ClientCreate

class ClientRepository:

    @staticmethod
    def create(db: Session, client: ClientCreate):
        db_client = Client(**client.dict())
        db.add(db_client)
        db.commit()
        db.refresh(db_client)
        return db_client

    @staticmethod
    def get(db: Session, client_id: int):
        return db.query(Client).filter(Client.id == client_id).first()

    @staticmethod
    def get_all(db: Session):
        return db.query(Client).all()

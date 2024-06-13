from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.schemas.client_schema import Client, ClientCreate
from api.repositories.client_repository import ClientRepository
from api.config import get_db

router = APIRouter()


@router.post("/clients/", response_model=Client)
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    db_client = ClientRepository.create(db, client)
    if db_client is None:
        raise HTTPException(status_code=400, detail="Client already exists")
    return db_client

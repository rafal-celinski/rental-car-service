from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from api.schemas.client_schema import Client, ClientCreate
from api.repositories.client_repository import ClientRepository
from api.config import get_db

router = APIRouter()

@router.post("/clients/", response_model=Client)
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    if client.pesel:
        db_client = ClientRepository.get_person_by_pesel(db, client.pesel)
        if db_client:
            raise HTTPException(status_code=400, detail="Client with this PESEL already exists")
        new_client = ClientRepository.create_person(db, client)
    elif client.nip:
        db_company = ClientRepository.get_company_by_nip(db, client.nip)
        if db_company:
            raise HTTPException(status_code=400, detail="Company with this NIP already exists")
        new_client = ClientRepository.create_company(db, client)
    else:
        raise HTTPException(status_code=400, detail="PESEL or NIP must be provided")
    return new_client

@router.get("/clients/", response_model=List[Client])
def get_all_clients(db: Session = Depends(get_db)):
    return ClientRepository.get_all(db)
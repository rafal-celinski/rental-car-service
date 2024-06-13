from pydantic import BaseModel
from typing import Optional

class ClientCreate(BaseModel):
    name: str
    surname: Optional[str] = None
    address: str
    pesel: Optional[str] = None
    nip: Optional[str] = None

class Client(BaseModel):
    id: int
    name: str
    surname: Optional[str]
    address: str
    pesel: Optional[str]
    nip: Optional[str]

    class Config:
        from_attributes = True

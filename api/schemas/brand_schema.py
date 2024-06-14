from pydantic import BaseModel
from typing import Optional

class BrandCreate(BaseModel):
    name: str

class Brand(BaseModel):
    name: str
    logo: Optional[str]

    class Config:
        orm_mode = True
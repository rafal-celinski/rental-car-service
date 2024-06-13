from pydantic import BaseModel
from datetime import date

class RentalCreate(BaseModel):
    client_id: int
    car_id: int
    estimated_end_date: date

class RentalUpdate(BaseModel):
    end_date: date
    active: bool

class Rental(BaseModel):
    id: int
    start_date: date
    end_date: date
    price: float
    active: bool
    car_id: int
    client_id: int

    class Config:
        orm_mode = True

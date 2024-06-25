from pydantic import BaseModel
from datetime import date
from typing import Optional

class CarCreate(BaseModel):
    model_name: str
    brand_name: str
    segment_name: str
    production_date: date
    mileage: int
    license_plate: str
    vin: str
    photo: Optional[str] = None

class Car(BaseModel):
    id: int
    model_name: str
    brand_name: str
    segment_name: str
    production_date: date
    mileage: int
    license_plate: str
    vin: str
    photo: Optional[str] = None
    is_rented: bool

    class Config:
        orm_mode = True


class CarUpdate(BaseModel):
    mileage: Optional[int] = None
    license_plate: Optional[str] = None
    vin: Optional[str] = None
    photo: Optional[str] = None

    class Config:
        orm_mode = True
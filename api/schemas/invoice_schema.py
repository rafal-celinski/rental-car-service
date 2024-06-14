from pydantic import BaseModel
from datetime import date
from typing import List, Optional

class Car(BaseModel):
    id: int
    model_name: str
    brand_name: str

    class Config:
        orm_mode = True


class InvoiceElement(BaseModel):
    invoice_id: int
    rental_id: int
    element_number: int
    price: float
    car: Car
 
    class Config:
        orm_mode = True

class Invoice(BaseModel):
    id: int
    client_id: int
    date: date
    price_sum_netto: Optional[float]
    tax: Optional[float]

    class Config:
        orm_mode = True

class InvoiceCreate(BaseModel):
    client_id: int
    start_date: date
    end_date: date
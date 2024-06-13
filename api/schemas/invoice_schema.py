from pydantic import BaseModel
from datetime import date

class InvoiceCreate(BaseModel):
    client_id: int
    start_date: date
    end_date: date

class Invoice(BaseModel):
    id: int
    client_id: int
    date: date
    price_sum_netto: float
    tax: float

    class Config:
        orm_mode = True

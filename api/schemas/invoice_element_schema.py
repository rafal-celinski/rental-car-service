from pydantic import BaseModel

class InvoiceElementCreate(BaseModel):
    invoice_id: int
    rental_id: int
    element_number: int
    price: float
    car_id: int

class InvoiceElement(BaseModel):
    id: int
    invoice_id: int
    rental_id: int
    element_number: int
    price: float
    car_id: int

    class Config:
        orm_mode = True

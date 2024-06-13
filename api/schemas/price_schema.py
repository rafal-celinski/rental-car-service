from pydantic import BaseModel

class PriceCreate(BaseModel):
    model_name: str
    brand_name: str
    price: float

class PriceUpdate(BaseModel):
    model_name: str
    brand_name: str
    price: float

class Price(BaseModel):
    id: int
    model_name: str
    brand_name: str
    price: float

    class Config:
        from_attributes = True

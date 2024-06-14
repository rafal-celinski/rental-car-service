from pydantic import BaseModel

class PriceBase(BaseModel):
    model_name: str
    brand_name: str
    price: float

class PriceCreate(PriceBase):
    pass

class PriceUpdate(PriceBase):
    pass

class Price(PriceBase):
    class Config:
        orm_mode = True

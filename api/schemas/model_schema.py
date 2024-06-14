from pydantic import BaseModel

class CarModelCreate(BaseModel):
    model_name: str
    brand_name: str
    segment_name: str

class CarModel(BaseModel):
    model_name: str
    brand_name: str
    segment_name: str

    class Config:
        from_attributes = True
        protected_namespaces = ()

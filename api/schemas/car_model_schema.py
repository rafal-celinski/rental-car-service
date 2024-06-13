from pydantic import BaseModel

class CarModelCreate(BaseModel):
    name: str

class CarModel(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
        protected_namespaces = ()

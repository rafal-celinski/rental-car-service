from pydantic import BaseModel

class BrandCreate(BaseModel):
    name: str

class Brand(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
        protected_namespaces = ()

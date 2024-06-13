from pydantic import BaseModel

class SegmentCreate(BaseModel):
    name: str
    description: str

class Segment(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        from_attributes = True
        protected_namespaces = ()

from pydantic import BaseModel

class SegmentCreate(BaseModel):
    name: str
    description: str

class Segment(BaseModel):
    name: str
    description: str

    class Config:
        orm_mode = True

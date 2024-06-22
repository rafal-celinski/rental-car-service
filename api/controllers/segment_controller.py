from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from schemas.segment_schema import Segment, SegmentCreate
from repositories.segment_repository import SegmentRepository
from config import get_db

router = APIRouter()

@router.post("/segments/", response_model=Segment)
def create_segment(segment: SegmentCreate, db: Session = Depends(get_db)):
    return SegmentRepository.create(db, segment)

@router.get("/segments/", response_model=List[Segment])
def get_all_segments(db: Session = Depends(get_db)):
    return SegmentRepository.get_all(db)

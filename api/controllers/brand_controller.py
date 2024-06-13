from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from api.schemas.brand_schema import Brand, BrandCreate
from api.repositories.brand_repository import BrandRepository
from api.config import get_db

router = APIRouter()

@router.post("/brands/", response_model=Brand)
def create_brand(brand: BrandCreate, db: Session = Depends(get_db)):
    return BrandRepository.create(db, brand)

@router.get("/brands/", response_model=List[Brand])
def get_all_brands(db: Session = Depends(get_db)):
    return BrandRepository.get_all(db)

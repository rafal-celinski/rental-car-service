from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from schemas.price_schema import Price, PriceCreate, PriceUpdate
from repositories.price_repository import PriceRepository
from config import get_db

router = APIRouter()

@router.post("/prices/", response_model=Price)
def create_or_update_price(price: PriceCreate, db: Session = Depends(get_db)):
    db_price = PriceRepository.get(db, price.model_name, price.brand_name)
    if db_price:
        return PriceRepository.update(db, db_price, PriceUpdate(**price.dict()))
    else:
        return PriceRepository.create(db, price)

@router.delete("/prices/{model_name}/{brand_name}", response_model=Price)
def delete_price(model_name: str, brand_name: str, db: Session = Depends(get_db)):
    db_price = PriceRepository.delete(db, model_name, brand_name)
    if not db_price:
        raise HTTPException(status_code=404, detail="Price not found")
    return db_price

@router.get("/prices/", response_model=List[Price])
def get_all_prices(db: Session = Depends(get_db)):
    return PriceRepository.get_all(db)


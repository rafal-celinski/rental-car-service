from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.schemas.price_schema import Price, PriceCreate, PriceUpdate
from api.repositories.price_repository import PriceRepository
from api.config import get_db

router = APIRouter()

@router.post("/prices/", response_model=Price)
def create_or_update_price(price: PriceCreate, db: Session = Depends(get_db)):
    db_price = PriceRepository.get(db, price.model_name, price.brand_name)
    if db_price:
        return PriceRepository.update(db, db_price, PriceUpdate(**price.dict()))
    else:
        return PriceRepository.create(db, price)

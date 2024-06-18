from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from api.schemas.model_schema import CarModel as CarModelSchema, CarModelCreate
from api.repositories.model_repository import CarModelRepository
from api.config import get_db

router = APIRouter()

@router.post("/models/", response_model=CarModelSchema)
def create_car_model(car_model: CarModelCreate, db: Session = Depends(get_db)):
    return CarModelRepository.create(db, car_model)

@router.get("/models/", response_model=List[CarModelSchema])
def get_all_models(db: Session = Depends(get_db)):
    models = CarModelRepository.get_all(db)
    if not models:
        raise HTTPException(status_code=404, detail="No car models found")
    return models
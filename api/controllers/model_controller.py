from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from api.schemas.car_model_schema import CarModel as CarModelSchema, CarModelCreate
from api.repositories.car_model_repository import CarModelRepository
from api.config import get_db

router = APIRouter()

@router.post("/models/", response_model=CarModelSchema)
def create_car_model(car_model: CarModelCreate, db: Session = Depends(get_db)):
    return CarModelRepository.create(db, car_model)

@router.get("/models/", response_model=List[CarModelSchema])
def get_all_car_models(db: Session = Depends(get_db)):
    car_models = CarModelRepository.get_all(db)
    return [CarModelSchema.from_orm(car_model) for car_model in car_models]

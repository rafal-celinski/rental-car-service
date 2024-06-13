from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from api.schemas.car_schema import Car, CarCreate
from api.repositories.car_repository import CarRepository
from api.config import get_db

router = APIRouter()

@router.post("/cars/", response_model=Car)
def create_car(car: CarCreate, db: Session = Depends(get_db)):
    return CarRepository.create(db, car)

@router.get("/cars/", response_model=List[Car])
def get_all_cars(db: Session = Depends(get_db)):
    return CarRepository.get_all(db)

@router.get("/cars/{car_id}", response_model=Car)
def get_car(car_id: int, db: Session = Depends(get_db)):
    db_car = CarRepository.get(db, car_id)
    if db_car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    return db_car

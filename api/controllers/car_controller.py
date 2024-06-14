from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.respones import FileResponse
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from api.schemas.car_schema import Car, CarCreate
from api.models.car import Car as CarModel
from api.repositories.car_repository import CarRepository
from api.config import get_db
import shutil 
import os

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/cars/", response_model=Car)
def create_car(
    model_name: str = Form(...),
    brand_name: str = Form(...),
    segment_name: str = Form(...),
    production_date: date = Form(...),
    mileage: int = Form(...),
    license_plate: str = Form(...),
    vin: str = Form(...),
    photo: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Save the uploaded photo file
    photo_path = os.path.join(UPLOAD_DIR, photo.filename)
    with open(photo_path, "wb") as buffer:
        shutil.copyfileobj(photo.file, buffer)
    
    db_car = CarModel(
        model_name=model_name,
        brand_name=brand_name,
        segment_name=segment_name,
        production_date=production_date,
        mileage=mileage,
        license_plate=license_plate,
        vin=vin,
        photo=photo.filename,  # Store the filename
        is_rented=False
    )
    db.add(db_car)
    db.commit()
    db.refresh(db_car)

    # Create the photo URL
    photo_url = f"http://localhost:8000/api/images/{photo.filename}"

    # Explicitly convert photo to string in the response
    response_car = Car(
        id=db_car.id,
        model_name=db_car.model_name,
        brand_name=db_car.brand_name,
        segment_name=db_car.segment_name,
        production_date=db_car.production_date,
        mileage=db_car.mileage,
        license_plate=db_car.license_plate,
        vin=db_car.vin,
        photo_url=photo_url,
        is_rented=db_car.is_rented
    )
    return response_car

@router.get("/cars/", response_model=List[Car])
def get_all_cars(db: Session = Depends(get_db)):
    return CarRepository.get_all(db)

@router.get("/cars/{car_id}", response_model=Car)
def get_car(car_id: int, db: Session = Depends(get_db)):
    db_car = CarRepository.get(db, car_id)
    if db_car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    return db_car

@router.get("/images/{filename}")
def get_image(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        raise HTTPException(status_code=404, detail="Image not found")
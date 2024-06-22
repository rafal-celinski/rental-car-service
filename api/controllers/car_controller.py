from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from schemas.car_schema import Car, CarCreate
from models.car import Car as CarModel
from repositories.car_repository import CarRepository
from config import get_db
import shutil 
import os

router = APIRouter()

UPLOAD_DIR = "/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def remove_bom(text):
    if text.startswith('\ufeff'):
        return text.replace('\ufeff', '')
    return text

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

    photo_filename = photo.filename.encode('utf-8').decode('utf-8') 
    
    db_car = CarModel(
        model_name=model_name,
        brand_name=brand_name,
        segment_name=segment_name,
        production_date=production_date,
        mileage=mileage,
        license_plate=license_plate,
        vin=vin,
        photo=photo_filename,  # Store the filename
        is_rented=False
    )
    db.add(db_car)
    db.commit()
    db.refresh(db_car)


    response_car = Car(
        id=db_car.id,
        model_name=db_car.model_name,
        brand_name=db_car.brand_name,
        segment_name=db_car.segment_name,
        production_date=db_car.production_date,
        mileage=db_car.mileage,
        license_plate=db_car.license_plate,
        vin=db_car.vin,
        photo=f"http://localhost:8000/api/images/{photo.filename}",
        is_rented=db_car.is_rented
    )
    return response_car

@router.get("/cars/", response_model=List[Car])
def get_cars(db: Session = Depends(get_db)):
    cars = db.query(CarModel).all()
    response_cars = []
    for car in cars:
        photo_filename = car.photo.tobytes().decode('utf-8') if isinstance(car.photo, memoryview) else car.photo
        photo_filename = remove_bom(photo_filename) if photo_filename else ""
        
        photo_url = f"http://localhost:8000/api/images/{photo_filename}" if photo_filename else ""
        
        response_car = Car(
            id=car.id,
            model_name=car.model_name,
            brand_name=car.brand_name,
            segment_name=car.segment_name,
            production_date=car.production_date,
            mileage=car.mileage,
            license_plate=car.license_plate,
            vin=car.vin,
            photo=str(photo_url),  
            is_rented=car.is_rented
        )
        response_cars.append(response_car)
    return response_cars

@router.get("/cars/{car_id}", response_model=Car)
def get_car(car_id: int, db: Session = Depends(get_db)):
    car = CarRepository.get(db, car_id)
    if car is None:
        raise HTTPException(status_code=404, detail="Car not found")

    photo_filename = car.photo.tobytes().decode('utf-8') if isinstance(car.photo, memoryview) else car.photo
    photo_filename = remove_bom(photo_filename) if photo_filename else ""
    photo_url = f"http://localhost:8000/api/images/{photo_filename}" if photo_filename else ""
    response_car = Car(
        id=car.id,
        model_name=car.model_name,
        brand_name=car.brand_name,
        segment_name=car.segment_name,
        production_date=car.production_date,
        mileage=car.mileage,
        license_plate=car.license_plate,
        vin=car.vin,
        photo=str(photo_url),  
        is_rented=car.is_rented
    )
    return response_car

@router.get("/images/{filename}")
def get_image(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        raise HTTPException(status_code=404, detail="Image not found")
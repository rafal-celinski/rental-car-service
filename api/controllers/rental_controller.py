from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from sqlalchemy.exc import SQLAlchemyError
from schemas.rental_schema import Rental, RentalCreate
from repositories.rental_repository import RentalRepository
from config import get_db
from typing import List

router = APIRouter()

@router.post("/rentals/", response_model=Rental)
def rent_car(rental: RentalCreate, db: Session = Depends(get_db)):
    try:
        db.execute(text("CALL start_rent(:client_id, :car_id, :estimated_end_date)"), {
            'client_id': rental.client_id,
            'car_id': rental.car_id,
            'estimated_end_date': rental.estimated_end_date
        })
        db.commit()
        new_rental = RentalRepository.get_latest(db, rental.client_id, rental.car_id)
        response = Rental(
            id = new_rental.id,
            start_date = new_rental.start_date,
            price = new_rental.price,
            active = new_rental.active,
            car_id = new_rental.car_id,
            client_id = new_rental.client_id,
            end_date = new_rental.end_date
        )
        return response
    except SQLAlchemyError as e:
        db.rollback()
        if "Car with id" in str(e) and "is already rented" in str(e):
            raise HTTPException(status_code=403, detail="This car is already rented.")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/rentals/{rental_id}/return", response_model=Rental)
def return_car(rental_id: int, db: Session = Depends(get_db)):
    try:
        db.execute(text("CALL end_rent(:rent_id)"), {'rent_id': rental_id})
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

    return RentalRepository.get(db, rental_id)

@router.get("/rentals/client/{client_id}", response_model=List[Rental])
def get_rentals_by_client(client_id: int, db: Session = Depends(get_db)):
    return RentalRepository.get_rentals_by_client(db, client_id)

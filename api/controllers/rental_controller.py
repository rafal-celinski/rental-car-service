from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.schemas.rental_schema import Rental, RentalCreate
from api.repositories.rental_repository import RentalRepository
from api.config import get_db

router = APIRouter()

@router.post("/rentals/", response_model=Rental)
def rent_car(rental: RentalCreate, db: Session = Depends(get_db)):
    try:
        db.execute("CALL start_rent(:client_id, :car_id, :estimated_end_date)", {
            'client_id': rental.client_id,
            'car_id': rental.car_id,
            'estimated_end_date': rental.estimated_end_date
        })
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

    return RentalRepository.get_latest(db, rental.client_id, rental.car_id)

@router.post("/rentals/{rental_id}/return", response_model=Rental)
def return_car(rental_id: int, db: Session = Depends(get_db)):
    try:
        db.execute("CALL end_rent(:rent_id)", {'rent_id': rental_id})
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

    return RentalRepository.get(db, rental_id)

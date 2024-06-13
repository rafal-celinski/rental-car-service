from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.schemas.rental_schema import Rental, RentalCreate, RentalUpdate
from api.repositories.rental_repository import RentalRepository
from api.config import get_db

router = APIRouter()

@router.post("/rentals/", response_model=Rental)
def rent_car(rental: RentalCreate, db: Session = Depends(get_db)):
    return RentalRepository.create(db, rental)

@router.post("/rentals/{rental_id}/return", response_model=Rental)
def return_car(rental_id: int, db: Session = Depends(get_db)):
    db_rental = RentalRepository.get(db, rental_id)
    if db_rental is None:
        raise HTTPException(status_code=404, detail="Rental not found")
    rental_update = RentalUpdate(end_date=db_rental.end_date, active=False)
    return RentalRepository.update(db, db_rental, rental_update)

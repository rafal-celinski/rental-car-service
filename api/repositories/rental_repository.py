from sqlalchemy.orm import Session
from models.rental import Rental
from schemas.rental_schema import RentalCreate, RentalUpdate

class RentalRepository:

    @staticmethod
    def create(db: Session, rental: RentalCreate):
        db_rental = Rental(**rental.dict())
        db.add(db_rental)
        db.commit()
        db.refresh(db_rental)
        return db_rental

    @staticmethod
    def update(db: Session, db_rental: Rental, rental_update: RentalUpdate):
        for key, value in rental_update.dict().items():
            setattr(db_rental, key, value)
        db.commit()
        db.refresh(db_rental)
        return db_rental

    @staticmethod
    def get(db: Session, rental_id: int):
        return db.query(Rental).filter(Rental.id == rental_id).first()

    @staticmethod
    def delete(db: Session, rental_id: int):
        db_rental = db.query(Rental).filter(Rental.id == rental_id).first()
        db.delete(db_rental)
        db.commit()

    @staticmethod
    def get_latest(db: Session, client_id: int, car_id: int):
        return db.query(Rental).filter(Rental.client_id == client_id, Rental.car_id == car_id).order_by(Rental.id.desc()).first()
    
    @staticmethod
    def get_rentals_by_client(db: Session, client_id: int):
        return db.query(Rental).filter(Rental.client_id == client_id, Rental.active == True).all()
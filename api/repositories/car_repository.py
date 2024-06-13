from sqlalchemy.orm import Session
from api.models.car import Car
from api.schemas.car_schema import CarCreate

class CarRepository:

    @staticmethod
    def create(db: Session, car: CarCreate):
        db_car = Car(**car.dict())
        db.add(db_car)
        db.commit()
        db.refresh(db_car)
        return db_car

    @staticmethod
    def get_all(db: Session):
        return db.query(Car).all()

    @staticmethod
    def get(db: Session, car_id: int):
        return db.query(Car).filter(Car.id == car_id).first()

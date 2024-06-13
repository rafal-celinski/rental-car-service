from sqlalchemy.orm import Session
from api.models.car_model import CarModel
from api.schemas.car_model_schema import CarModelCreate


class CarModelRepository:

    @staticmethod
    def create(db: Session, car_model: CarModelCreate):
        db_car_model = CarModel(name=car_model.name)
        db.add(db_car_model)
        db.commit()
        db.refresh(db_car_model)
        return db_car_model

    @staticmethod
    def get_all(db: Session):
        return db.query(CarModel).all()

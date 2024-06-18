from sqlalchemy.orm import Session
from api.models.model import CarModel
from api.schemas.model_schema import CarModelCreate

class CarModelRepository:

    @staticmethod
    def create(db: Session, car_model: CarModelCreate):
        db_car_model = CarModel(
            model_name=car_model.model_name,
            brand_name=car_model.brand_name,
            segment_name=car_model.segment_name
        )
        db.add(db_car_model)
        db.commit()
        db.refresh(db_car_model)
        return db_car_model

    @staticmethod
    def get_all(db: Session):
        return db.query(CarModel).all()

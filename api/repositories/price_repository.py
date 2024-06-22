from sqlalchemy.orm import Session
from models.price_list import Price
from schemas.price_schema import PriceCreate, PriceUpdate

class PriceRepository:
    @staticmethod
    def get(db: Session, model_name: str, brand_name: str):
        return db.query(Price).filter(Price.model_name == model_name, Price.brand_name == brand_name).first()

    @staticmethod
    def create(db: Session, price: PriceCreate):
        db_price = Price(**price.dict())
        db.add(db_price)
        db.commit()
        db.refresh(db_price)
        return db_price

    @staticmethod
    def update(db: Session, db_price: Price, price_update: PriceUpdate):
        db_price.price = price_update.price
        db.commit()
        db.refresh(db_price)
        return db_price

    @staticmethod
    def delete(db: Session, model_name: str, brand_name: str):
        db_price = db.query(Price).filter(Price.model_name == model_name, Price.brand_name == brand_name).first()
        if db_price:
            db.delete(db_price)
            db.commit()
        return db_price

    @staticmethod
    def get_all(db: Session):
        return db.query(Price).all()

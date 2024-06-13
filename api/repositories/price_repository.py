from sqlalchemy.orm import Session
from api.models.price_list import PriceList
from api.schemas.price_schema import PriceCreate, PriceUpdate

class PriceRepository:

    @staticmethod
    def create(db: Session, price: PriceCreate):
        db_price = PriceList(**price.dict())
        db.add(db_price)
        db.commit()
        db.refresh(db_price)
        return db_price

    @staticmethod
    def update(db: Session, db_price: PriceList, price_update: PriceUpdate):
        for key, value in price_update.dict().items():
            setattr(db_price, key, value)
        db.commit()
        db.refresh(db_price)
        return db_price

    @staticmethod
    def get(db: Session, price_id: int):
        return db.query(PriceList).filter(PriceList.id == price_id).first()

    @staticmethod
    def get_all(db: Session):
        return db.query(PriceList).all()

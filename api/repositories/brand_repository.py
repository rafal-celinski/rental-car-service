from sqlalchemy.orm import Session
from api.models.brand import Brand
from api.schemas.brand_schema import BrandCreate

class BrandRepository:

    @staticmethod
    def create(db: Session, brand: BrandCreate):
        db_brand = Brand(name=brand.name)
        db.add(db_brand)
        db.commit()
        db.refresh(db_brand)
        return db_brand

    @staticmethod
    def get_all(db: Session):
        return db.query(Brand).all()

from sqlalchemy.orm import Session
from models.segment import Segment
from schemas.segment_schema import SegmentCreate

class SegmentRepository:

    @staticmethod
    def create(db: Session, segment: SegmentCreate):
        db_segment = Segment(name=segment.name, description=segment.description)
        db.add(db_segment)
        db.commit()
        db.refresh(db_segment)
        return db_segment

    @staticmethod
    def get_all(db: Session):
        return db.query(Segment).all()

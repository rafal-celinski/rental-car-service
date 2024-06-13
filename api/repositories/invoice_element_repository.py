from sqlalchemy.orm import Session
from api.models.invoice_element import InvoiceElement
from api.schemas.invoice_element_schema import InvoiceElementCreate

class InvoiceElementRepository:

    @staticmethod
    def create(db: Session, invoice_element: InvoiceElementCreate):
        db_invoice_element = InvoiceElement(**invoice_element.dict())
        db.add(db_invoice_element)
        db.commit()
        db.refresh(db_invoice_element)
        return db_invoice_element

    @staticmethod
    def get(db: Session, invoice_element_id: int):
        return db.query(InvoiceElement).filter(InvoiceElement.id == invoice_element_id).first()

    @staticmethod
    def get_all(db: Session):
        return db.query(InvoiceElement).all()

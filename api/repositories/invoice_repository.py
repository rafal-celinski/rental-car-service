from sqlalchemy.orm import Session
from api.models.invoice import Invoice
from api.schemas.invoice_schema import InvoiceCreate

class InvoiceRepository:

    @staticmethod
    def create(db: Session, invoice: InvoiceCreate):
        db_invoice = Invoice(**invoice.dict())
        db.add(db_invoice)
        db.commit()
        db.refresh(db_invoice)
        return db_invoice

    @staticmethod
    def get(db: Session, invoice_id: int):
        return db.query(Invoice).filter(Invoice.id == invoice_id).first()

    @staticmethod
    def get_all(db: Session):
        return db.query(Invoice).all()

    @staticmethod
    def get_latest(db: Session, client_id: int):
        return db.query(Invoice).filter(Invoice.client_id == client_id).order_by(Invoice.id.desc()).first()

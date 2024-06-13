from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.schemas.invoice_schema import Invoice, InvoiceCreate
from api.repositories.invoice_repository import InvoiceRepository
from api.config import get_db

router = APIRouter()

@router.post("/invoices/", response_model=Invoice)
def generate_invoice(invoice: InvoiceCreate, db: Session = Depends(get_db)):
    try:
        db.execute("CALL create_invoice(:client_id, :start_date, :end_date)", {
            'client_id': invoice.client_id,
            'start_date': invoice.start_date,
            'end_date': invoice.end_date
        })
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

    return InvoiceRepository.get_latest(db, invoice.client_id)

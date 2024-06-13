from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.schemas.invoice_schema import Invoice, InvoiceCreate
from api.repositories.invoice_repository import InvoiceRepository
from api.config import get_db

router = APIRouter()

@router.post("/invoices/", response_model=Invoice)
def generate_invoice(invoice: InvoiceCreate, db: Session = Depends(get_db)):
    db_invoice = InvoiceRepository.create(db, invoice)
    if db_invoice is None:
        raise HTTPException(status_code=400, detail="Invoice could not be created")
    return db_invoice

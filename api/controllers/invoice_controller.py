from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.invoice_schema import Invoice, InvoiceCreate, InvoiceElement
from repositories.invoice_repository import InvoiceRepository
from config import get_db
from typing import List
from sqlalchemy import text

router = APIRouter()

@router.post("/invoices/", response_model=Invoice)
def generate_invoice(invoice: InvoiceCreate, db: Session = Depends(get_db)):
    try:
        db.execute(text("CALL create_invoice(:client_id, :start_date, :end_date)"), {
            'client_id': invoice.client_id,
            'start_date': invoice.start_date,
            'end_date': invoice.end_date
        })
        db.commit()
    except Exception as e:
        db.rollback()
        if 'Total price for invoice must be greater than zero' in str(e):
            raise HTTPException(status_code=400, detail="No rentals found in the specified date window.")
        raise HTTPException(status_code=400, detail=str(e))

    return InvoiceRepository.get_latest(db, invoice.client_id)


@router.get("/invoices/client/{client_id}", response_model=List[Invoice])
def get_invoices_by_client(client_id: int, db: Session = Depends(get_db)):
    return InvoiceRepository.get_all_by_client(db, client_id)

@router.get("/invoices/{invoice_id}/elements", response_model=List[InvoiceElement])
def get_invoice_elements(invoice_id: int, db: Session = Depends(get_db)):
    elements = InvoiceRepository.get_invoice_elements_with_car_details(db, invoice_id)
    if not elements:
        raise HTTPException(status_code=404, detail="Invoice elements not found")
    return elements
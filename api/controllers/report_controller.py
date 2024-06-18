from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from typing import Dict
from api.config import get_db
from api.models.invoice import Invoice

router = APIRouter()

@router.get("/reports/monthly/", response_model=Dict)
def generate_monthly_report(year: int, month: int, db: Session = Depends(get_db)) -> Dict:
    try:
        total_invoices = db.query(func.count(Invoice.id)).filter(
            extract('year', Invoice.date) == year,
            extract('month', Invoice.date) == month
        ).scalar() or 0

        total_revenue = db.query(func.sum(Invoice.price_sum_netto)).filter(
            extract('year', Invoice.date) == year,
            extract('month', Invoice.date) == month
        ).scalar() or 0.0

        total_clients = db.query(func.count(func.distinct(Invoice.client_id))).filter(
            extract('year', Invoice.date) == year,
            extract('month', Invoice.date) == month
        ).scalar() or 0

        return {
            "total_invoices": total_invoices,
            "total_revenue": total_revenue,
            "total_clients": total_clients
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating monthly report: {str(e)}")

@router.get("/reports/yearly/", response_model=Dict)
def generate_yearly_report(year: int, db: Session = Depends(get_db)) -> Dict:
    try:
        total_invoices = db.query(func.count(Invoice.id)).filter(
            extract('year', Invoice.date) == year
        ).scalar() or 0

        total_revenue = db.query(func.sum(Invoice.price_sum_netto)).filter(
            extract('year', Invoice.date) == year
        ).scalar() or 0.0

        total_clients = db.query(func.count(func.distinct(Invoice.client_id))).filter(
            extract('year', Invoice.date) == year
        ).scalar() or 0

        return {
            "total_invoices": total_invoices,
            "total_revenue": total_revenue,
            "total_clients": total_clients
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating yearly report: {str(e)}")

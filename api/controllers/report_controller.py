from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from typing import Dict
from api.config import get_db
from api.models.rental import Rental

router = APIRouter()

@router.get("/reports/monthly/", response_model=Dict)
def generate_monthly_report(year: int, month: int, db: Session = Depends(get_db)) -> Dict:
    try:
        total_rentals = db.query(func.count(Rental.id)).filter(
            extract('year', Rental.start_date) == year,
            extract('month', Rental.start_date) == month
        ).scalar() or 0

        total_revenue = db.query(func.sum(Rental.price)).filter(
            extract('year', Rental.start_date) == year,
            extract('month', Rental.start_date) == month
        ).scalar() or 0.0

        total_clients = db.query(func.count(func.distinct(Rental.client_id))).filter(
            extract('year', Rental.start_date) == year,
            extract('month', Rental.start_date) == month
        ).scalar() or 0

        return {
            "total_rentals": total_rentals,
            "total_revenue": total_revenue,
            "total_clients": total_clients
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating monthly report: {str(e)}")

@router.get("/reports/yearly/", response_model=Dict)
def generate_yearly_report(year: int, db: Session = Depends(get_db)) -> Dict:
    try:
        total_rentals = db.query(func.count(Rental.id)).filter(
            extract('year', Rental.start_date) == year
        ).scalar() or 0

        total_revenue = db.query(func.sum(Rental.price)).filter(
            extract('year', Rental.start_date) == year
        ).scalar() or 0.0

        total_clients = db.query(func.count(func.distinct(Rental.client_id))).filter(
            extract('year', Rental.start_date) == year
        ).scalar() or 0

        return {
            "total_rentals": total_rentals,
            "total_revenue": total_revenue,
            "total_clients": total_clients
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating yearly report: {str(e)}")

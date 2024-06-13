from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from typing import Dict
from api.config import get_db
from api.models.rental import Rental

router = APIRouter()

@router.get("/reports/monthly/")
def generate_monthly_report(year: int, month: int, db: Session = Depends(get_db)) -> Dict:
    try:
        total_rentals = db.query(func.count(Rental.id)).filter(
            extract('year', Rental.start_date) == year,
            extract('month', Rental.start_date) == month
        ).scalar()

        total_revenue = db.query(func.sum(Rental.price)).filter(
            extract('year', Rental.start_date) == year,
            extract('month', Rental.start_date) == month
        ).scalar()

        total_clients = db.query(func.count(func.distinct(Rental.client_id))).filter(
            extract('year', Rental.start_date) == year,
            extract('month', Rental.start_date) == month
        ).scalar()

        return {
            "total_rentals": total_rentals,
            "total_revenue": total_revenue,
            "total_clients": total_clients
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/reports/yearly/")
def generate_yearly_report(year: int, db: Session = Depends(get_db)) -> Dict:
    try:
        total_rentals = db.query(func.count(Rental.id)).filter(
            extract('year', Rental.start_date) == year
        ).scalar()

        total_revenue = db.query(func.sum(Rental.price)).filter(
            extract('year', Rental.start_date) == year
        ).scalar()

        total_clients = db.query(func.count(func.distinct(Rental.client_id))).filter(
            extract('year', Rental.start_date) == year
        ).scalar()

        return {
            "total_rentals": total_rentals,
            "total_revenue": total_revenue,
            "total_clients": total_clients
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from typing import Dict
from config import get_db
from models.invoice import Invoice
from typing import List
from models.car import Car as CarModel
from models.rental import Rental as RentalModel

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

@router.get("/reports/car_rentals/", response_model=List[Dict])
def get_car_rental_stats(db: Session = Depends(get_db)):
    try:
        rental_stats = db.query(
            CarModel.id.label("car_id"),
            CarModel.model_name.label("model_name"),
            CarModel.brand_name.label("brand_name"),
            func.count(RentalModel.id).label("rental_count"),
            func.sum(func.extract('epoch', func.age(RentalModel.end_date, RentalModel.start_date)) / 86400).label("total_duration"),
            func.sum(RentalModel.price).label("total_profit")
        ).join(RentalModel, CarModel.id == RentalModel.car_id).group_by(CarModel.id).all()

        results = []
        for stat in rental_stats:
            results.append({
                "car_id": stat.car_id,
                "model_name": stat.model_name,
                "brand_name": stat.brand_name,
                "rental_count": stat.rental_count,
                "total_duration": stat.total_duration if stat.total_duration is not None else 0,
                "total_profit": stat.total_profit if stat.total_profit is not None else 0.0
            })

        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating rental statistics: {str(e)}")
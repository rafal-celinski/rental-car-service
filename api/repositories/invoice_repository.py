from sqlalchemy.orm import Session
from sqlalchemy import text
from models import Invoice, InvoiceElement, Car
from typing import List

class InvoiceRepository:
    @staticmethod
    def get_latest(db: Session, client_id: int) -> Invoice:
        return db.query(Invoice).filter(Invoice.client_id == client_id).order_by(Invoice.id.desc()).first()

    @staticmethod
    def get_by_id(db: Session, invoice_id: int) -> Invoice:
        return db.query(Invoice).filter(Invoice.id == invoice_id).first()

    @staticmethod
    def get_all_by_client(db: Session, client_id: int) -> List[Invoice]:
        return db.query(Invoice).filter(Invoice.client_id == client_id).all()

    @staticmethod
    def get_invoice_elements(db: Session, invoice_id: int) -> List[InvoiceElement]:
        return db.query(InvoiceElement).filter(InvoiceElement.invoice_id == invoice_id).all()
        
    @staticmethod
    def get_invoice_elements_with_car_details(db: Session, invoice_id: int):
        query = text("""
            SELECT 
                ie.invoice_id AS ie_invoice_id, 
                ie.rental_id AS ie_rental_id, 
                ie.element_number AS ie_element_number, 
                ie.price AS ie_price, 
                c.id AS car_id, 
                c.model_name AS car_model_name, 
                c.brand_name AS car_brand_name 
            FROM 
                invoice_element ie 
            JOIN 
                car c 
            ON 
                ie.car_id = c.id 
            WHERE 
                ie.invoice_id = :invoice_id
        """)
        result = db.execute(query, {'invoice_id': invoice_id}).fetchall()
        
        elements = []
        for row in result:
            element = {
                'invoice_id': row.ie_invoice_id,
                'rental_id': row.ie_rental_id,
                'element_number': row.ie_element_number,
                'price': row.ie_price,
                'car': {
                    'id': row.car_id,
                    'model_name': row.car_model_name,
                    'brand_name': row.car_brand_name,
                }
            }
            elements.append(element)
        
        return elements
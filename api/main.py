from fastapi import FastAPI
from api.controllers import client_router, car_router, rental_router, price_router, report_router, invoice_router, brand_router, model_router, segment_router
from api.config import engine
from api.models import client, car, rental, price_list, invoice, invoice_element, brand, model, segment

app = FastAPI()

client.Base.metadata.create_all(bind=engine)
car.Base.metadata.create_all(bind=engine)
rental.Base.metadata.create_all(bind=engine)
price_list.Base.metadata.create_all(bind=engine)
invoice.Base.metadata.create_all(bind=engine)
invoice_element.Base.metadata.create_all(bind=engine)
brand.Base.metadata.create_all(bind=engine)
model.Base.metadata.create_all(bind=engine)
segment.Base.metadata.create_all(bind=engine)

app.include_router(client_router, prefix="/api")
app.include_router(car_router, prefix="/api")
app.include_router(rental_router, prefix="/api")
app.include_router(price_router, prefix="/api")
app.include_router(report_router, prefix="/api")
app.include_router(invoice_router, prefix="/api")
app.include_router(brand_router, prefix="/api")
app.include_router(model_router, prefix="/api")
app.include_router(segment_router, prefix="/api")

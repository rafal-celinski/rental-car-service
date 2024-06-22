from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.client_controller import router as client_router
from controllers.car_controller import router as car_router
from controllers.rental_controller import router as rental_router
from controllers.price_controller import router as price_router
from controllers.report_controller import router as report_router
from controllers.invoice_controller import router as invoice_router
from controllers.brand_controller import router as brand_router
from controllers.model_controller import router as model_router
from controllers.segment_controller import router as segment_router
from config import engine
from models import client, car, rental, price_list, invoice, invoice_element, brand, model, segment

app = FastAPI()

# Configure CORS
origins = [
    "http://localhost:5000",
    "http://127.0.0.1:5000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

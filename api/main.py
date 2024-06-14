from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.controllers.client_controller import router as client_router
from api.controllers.car_controller import router as car_router
from api.controllers.rental_controller import router as rental_router
from api.controllers.price_controller import router as price_router
from api.controllers.report_controller import router as report_router
from api.controllers.invoice_controller import router as invoice_router
from api.controllers.brand_controller import router as brand_router
from api.controllers.model_controller import router as model_router
from api.controllers.segment_controller import router as segment_router
from api.config import engine
from api.models import client, car, rental, price_list, invoice, invoice_element, brand, car_model, segment

app = FastAPI()

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, you can specify specific origins here
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

client.Base.metadata.create_all(bind=engine)
car.Base.metadata.create_all(bind=engine)
rental.Base.metadata.create_all(bind=engine)
price_list.Base.metadata.create_all(bind=engine)
invoice.Base.metadata.create_all(bind=engine)
invoice_element.Base.metadata.create_all(bind=engine)
brand.Base.metadata.create_all(bind=engine)
car_model.Base.metadata.create_all(bind=engine)
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

from fastapi import FastAPI

from .table_models import transaction_model
from .core.database import engine
from .endpoint_routers import transaction_routes

# Creates table for data
transaction_model.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(transaction_routes.router)


@app.get("/")
def root_point():
  return {"message": "API still working?"}
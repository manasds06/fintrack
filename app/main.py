from fastapi import FastAPI

from .table_models import transaction_model, budget_model, user_model
from .core.database import engine
from .endpoint_routers import transaction_router, budget_router, user_router

# Creates table for data
user_model.Base.metadata.create_all(bind=engine)
budget_model.Base.metadata.create_all(bind=engine)
transaction_model.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(transaction_router.router)
app.include_router(budget_router.router)
app.include_router(user_router.router)


@app.get("/")
def root_point():
  return {"message": "API still working?"}
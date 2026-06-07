from fastapi import APIRouter

from route.account_routes import router as account_router
from route.transaction_routes import router as transaction_router
from route.category_routes import router as category_router
from route.budget_routes import router as budget_router
from route.statistics_routes import router as statistics_router
from route.log_routes import router as log_router

api = APIRouter(prefix="/api")
api.include_router(account_router)
api.include_router(transaction_router)
api.include_router(category_router)
api.include_router(budget_router)
api.include_router(statistics_router)
api.include_router(log_router)

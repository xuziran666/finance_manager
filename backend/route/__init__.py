"""路由控制层"""
from flask import Blueprint
from route.account_routes import init_account_routes
from route.transaction_routes import init_transaction_routes
from route.category_routes import init_category_routes
from route.budget_routes import init_budget_routes
from route.statistics_routes import init_statistics_routes
from route.log_routes import init_log_routes

api = Blueprint("api", __name__, url_prefix="/api")

init_account_routes(api)
init_transaction_routes(api)
init_category_routes(api)
init_budget_routes(api)
init_statistics_routes(api)
init_log_routes(api)
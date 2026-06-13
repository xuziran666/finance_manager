from functools import lru_cache

from dao import AccountDAO, TransactionDAO, CategoryDAO, BudgetDAO, LogDAO
from service import AccountService, TransactionService, CategoryService, BudgetService, StatisticsService, LogService


@lru_cache(maxsize=None)
def get_account_dao() -> AccountDAO:
    return AccountDAO()


@lru_cache(maxsize=None)
def get_transaction_dao() -> TransactionDAO:
    return TransactionDAO()


@lru_cache(maxsize=None)
def get_category_dao() -> CategoryDAO:
    return CategoryDAO()


@lru_cache(maxsize=None)
def get_budget_dao() -> BudgetDAO:
    return BudgetDAO()


@lru_cache(maxsize=None)
def get_log_dao() -> LogDAO:
    return LogDAO()


@lru_cache(maxsize=None)
def get_account_service() -> AccountService:
    return AccountService(get_account_dao(), get_log_dao())


@lru_cache(maxsize=None)
def get_transaction_service() -> TransactionService:
    return TransactionService(get_account_dao(), get_transaction_dao(), get_log_dao())


@lru_cache(maxsize=None)
def get_category_service() -> CategoryService:
    return CategoryService(get_category_dao(), get_log_dao())


@lru_cache(maxsize=None)
def get_budget_service() -> BudgetService:
    return BudgetService(get_budget_dao(), get_transaction_dao(), get_log_dao())


@lru_cache(maxsize=None)
def get_log_service() -> LogService:
    return LogService(get_log_dao())


@lru_cache(maxsize=None)
def get_statistics_service() -> StatisticsService:
    return StatisticsService(get_transaction_dao())

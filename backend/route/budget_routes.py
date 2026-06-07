from datetime import datetime
from fastapi import APIRouter, Query
from typing import Optional
from dto import BudgetSet, BudgetDelete
from vo import ApiResponse
from service import BudgetService

router = APIRouter(tags=["预算管理"])


@router.get("/budgets/summary", summary="预算汇总")
def get_budget_summary(
    year: Optional[int] = Query(None),
    month: Optional[int] = Query(None),
):
    now = datetime.now()
    y = year if year is not None else now.year
    m = month if month is not None else now.month
    return ApiResponse(data=BudgetService.get_summary(y, m))


@router.delete("/budgets", summary="删除预算")
def delete_budget(data: BudgetDelete):
    BudgetService.delete(data.year, data.month, data.category)
    return ApiResponse(msg="删除成功")


@router.post("/budgets", summary="设置预算")
def set_budget(data: BudgetSet):
    ok, msg = BudgetService.set(data.year, data.month, data.category, data.amount)
    return ApiResponse(msg=msg) if ok else ApiResponse(code=400, msg=msg)


@router.get("/budgets", summary="查询预算")
def get_budgets(
    year: Optional[int] = Query(None),
    month: Optional[int] = Query(None),
):
    return ApiResponse(data=BudgetService.get_all(year, month))

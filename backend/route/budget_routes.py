from datetime import datetime
from fastapi import APIRouter, Depends, Query
from typing import Optional
from dto import BudgetSet, BudgetDelete
from vo import ApiResponse
from service import BudgetService
from route.depends import get_current_user
from route.di_providers import get_budget_service

router = APIRouter(tags=["预算管理"])


@router.get("/budgets/summary", dependencies=[Depends(get_current_user)], summary="预算汇总")
def get_budget_summary(
    svc: BudgetService = Depends(get_budget_service),
    year: Optional[int] = Query(None),
    month: Optional[int] = Query(None),
):
    now = datetime.now()
    y = year if year is not None else now.year
    m = month if month is not None else now.month
    return ApiResponse(data=svc.get_summary(y, m))


@router.delete("/budgets", dependencies=[Depends(get_current_user)], summary="删除预算")
def delete_budget(data: BudgetDelete, svc: BudgetService = Depends(get_budget_service)):
    svc.delete(data.year, data.month, data.category)
    return ApiResponse(msg="删除成功")


@router.post("/budgets", dependencies=[Depends(get_current_user)], summary="设置预算")
def set_budget(data: BudgetSet, svc: BudgetService = Depends(get_budget_service)):
    ok, msg = svc.set(data.year, data.month, data.category, data.amount)
    return ApiResponse(msg=msg) if ok else ApiResponse(code=400, msg=msg)


@router.get("/budgets", dependencies=[Depends(get_current_user)], summary="查询预算")
def get_budgets(
    svc: BudgetService = Depends(get_budget_service),
    year: Optional[int] = Query(None),
    month: Optional[int] = Query(None),
):
    return ApiResponse(data=svc.get_all(year, month))

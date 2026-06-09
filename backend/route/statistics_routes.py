from fastapi import APIRouter, Depends, Query
from typing import Optional
from vo import ApiResponse
from service import StatisticsService
from route.depends import get_current_user

router = APIRouter(tags=["统计分析"])


@router.get("/statistics", summary="获取统计数据")
def get_statistics(
    user: dict = Depends(get_current_user),
    account_id: Optional[int] = Query(None),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    group_by: str = Query("month"),
):
    return ApiResponse(data=StatisticsService.get(user["user_id"], account_id, start_date, end_date, group_by))

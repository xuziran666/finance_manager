from fastapi import APIRouter, Query
from typing import Optional
from vo import ApiResponse
from service import StatisticsService

router = APIRouter(tags=["统计分析"])


@router.get("/statistics", summary="获取统计数据")
def get_statistics(
    account_id: Optional[int] = Query(None),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    group_by: str = Query("month"),
):
    return ApiResponse(data=StatisticsService.get(account_id, start_date, end_date, group_by))

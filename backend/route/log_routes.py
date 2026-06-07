from fastapi import APIRouter, Query
from vo import ApiResponse
from service import LogService

router = APIRouter(tags=["操作日志"])


@router.get("/logs", summary="获取操作日志")
def get_logs(limit: int = Query(100)):
    return ApiResponse(data=LogService.get_all(limit))

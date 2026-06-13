from fastapi import APIRouter, Depends, Query
from vo import ApiResponse
from service import LogService
from route.depends import get_current_user
from route.di_providers import get_log_service

router = APIRouter(tags=["操作日志"])


@router.get("/logs", dependencies=[Depends(get_current_user)], summary="获取操作日志")
def get_logs(svc: LogService = Depends(get_log_service), limit: int = Query(100)):
    return ApiResponse(data=svc.get_all(limit))

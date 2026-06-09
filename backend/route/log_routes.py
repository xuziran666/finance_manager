from fastapi import APIRouter, Depends, Query
from vo import ApiResponse
from service import LogService
from route.depends import get_current_user

router = APIRouter(tags=["操作日志"])


@router.get("/logs", summary="获取操作日志")
def get_logs(user: dict = Depends(get_current_user), limit: int = Query(100)):
    return ApiResponse(data=LogService.get_all(user["user_id"], limit))

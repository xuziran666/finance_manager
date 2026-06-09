from fastapi import APIRouter
from dto import RegisterDTO, LoginDTO
from vo import ApiResponse
from service import UserService

router = APIRouter(tags=["用户认证"])


@router.post("/auth/register", summary="用户注册")
def register(data: RegisterDTO):
    ok, msg = UserService.register(data.username, data.password)
    return ApiResponse(msg=msg) if ok else ApiResponse(code=400, msg=msg)


@router.post("/auth/login", summary="用户登录")
def login(data: LoginDTO):
    ok, result = UserService.login(data.username, data.password)
    return ApiResponse(data=result) if ok else ApiResponse(code=400, msg=result)

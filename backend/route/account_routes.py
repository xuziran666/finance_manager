from fastapi import APIRouter
from dto import AccountCreate, AccountUpdate
from vo import ApiResponse
from service import AccountService

router = APIRouter(tags=["账户管理"])


@router.post("/accounts", summary="添加账户")
def add_account(data: AccountCreate):
    ok, result = AccountService.add(data.name, data.type, data.balance)
    return ApiResponse(data=result) if ok else ApiResponse(code=400, msg=result)


@router.delete("/accounts/{aid}", summary="删除账户")
def delete_account(aid: int):
    ok, msg = AccountService.delete(aid)
    return ApiResponse(msg=msg) if ok else ApiResponse(code=400, msg=msg)


@router.put("/accounts/{aid}", summary="更新账户")
def update_account(aid: int, data: AccountUpdate):
    ok, result = AccountService.update(aid, data.name, data.type)
    return ApiResponse(data=result) if ok else ApiResponse(code=400, msg=result)


@router.get("/accounts", summary="获取账户列表")
def get_accounts():
    return ApiResponse(data=AccountService.get_all())

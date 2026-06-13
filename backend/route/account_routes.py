from fastapi import APIRouter, Depends
from dto import AccountCreate, AccountUpdate
from vo import ApiResponse
from service import AccountService
from route.depends import get_current_user
from route.di_providers import get_account_service

router = APIRouter(tags=["账户管理"])


@router.post("/accounts", dependencies=[Depends(get_current_user)], summary="添加账户")
def add_account(data: AccountCreate, svc: AccountService = Depends(get_account_service)):
    ok, result = svc.add(data.name, data.type, data.balance)
    return ApiResponse(data=result) if ok else ApiResponse(code=400, msg=result)


@router.delete("/accounts/{aid}", dependencies=[Depends(get_current_user)], summary="删除账户")
def delete_account(aid: int, svc: AccountService = Depends(get_account_service)):
    ok, msg = svc.delete(aid)
    return ApiResponse(msg=msg) if ok else ApiResponse(code=400, msg=msg)


@router.put("/accounts/{aid}", dependencies=[Depends(get_current_user)], summary="更新账户")
def update_account(aid: int, data: AccountUpdate, svc: AccountService = Depends(get_account_service)):
    ok, result = svc.update(aid, data.name, data.type)
    return ApiResponse(data=result) if ok else ApiResponse(code=400, msg=result)


@router.get("/accounts", dependencies=[Depends(get_current_user)], summary="获取账户列表")
def get_accounts(svc: AccountService = Depends(get_account_service)):
    return ApiResponse(data=svc.get_all())

from fastapi import APIRouter, Depends
from dto import CategoryCreate, CategoryDelete, CategoryUpdate
from vo import ApiResponse
from service import CategoryService
from route.depends import get_current_user
from route.di_providers import get_category_service

router = APIRouter(tags=["分类管理"])


@router.post("/categories", summary="添加分类")
def add_category(data: CategoryCreate, user: dict = Depends(get_current_user), svc: CategoryService = Depends(get_category_service)):
    ok, msg = svc.add(user["user_id"], data.type, data.main, data.sub)
    return ApiResponse(msg=msg) if ok else ApiResponse(code=400, msg=msg)


@router.delete("/categories", summary="删除分类")
def delete_category(data: CategoryDelete, user: dict = Depends(get_current_user), svc: CategoryService = Depends(get_category_service)):
    ok, msg = svc.delete(user["user_id"], data.type, data.main, data.sub)
    return ApiResponse(msg=msg) if ok else ApiResponse(code=400, msg=msg)


@router.put("/categories", summary="修改分类")
def update_category(data: CategoryUpdate, user: dict = Depends(get_current_user), svc: CategoryService = Depends(get_category_service)):
    ok, msg = svc.update(
        user["user_id"],
        data.old_type, data.old_main, data.old_sub,
        data.new_type, data.new_main, data.new_sub,
    )
    return ApiResponse(msg=msg) if ok else ApiResponse(code=400, msg=msg)


@router.get("/categories", summary="获取分类列表")
def get_categories(user: dict = Depends(get_current_user), svc: CategoryService = Depends(get_category_service)):
    return ApiResponse(data=svc.get_all(user["user_id"]))

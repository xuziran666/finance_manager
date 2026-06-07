from fastapi import APIRouter
from dto import CategoryCreate, CategoryDelete, CategoryUpdate
from vo import ApiResponse
from service import CategoryService

router = APIRouter(tags=["分类管理"])


@router.post("/categories", summary="添加分类")
def add_category(data: CategoryCreate):
    ok, msg = CategoryService.add(data.type, data.main, data.sub)
    return ApiResponse(msg=msg) if ok else ApiResponse(code=400, msg=msg)


@router.delete("/categories", summary="删除分类")
def delete_category(data: CategoryDelete):
    ok, msg = CategoryService.delete(data.type, data.main, data.sub)
    return ApiResponse(msg=msg) if ok else ApiResponse(code=400, msg=msg)


@router.put("/categories", summary="修改分类")
def update_category(data: CategoryUpdate):
    ok, msg = CategoryService.update(
        data.old_type, data.old_main, data.old_sub,
        data.new_type, data.new_main, data.new_sub,
    )
    return ApiResponse(msg=msg) if ok else ApiResponse(code=400, msg=msg)


@router.get("/categories", summary="获取分类列表")
def get_categories():
    return ApiResponse(data=CategoryService.get_all())

"""分类管理路由：定义收支分类的增删改查 API 接口"""
from flask import request
from service import CategoryService
from route.result import Result


def init_category_routes(api):
    """注册分类相关路由到指定的 Blueprint 对象"""

    @api.route("/categories", methods=["POST"])
    def add_category():
        """POST /api/categories — 添加新分类（type, main, sub）"""
        data = request.json
        ok, msg = CategoryService.add(data.get("type"), data.get("main"), data.get("sub", ""))
        return Result.success(msg=msg) if ok else Result.fail(msg)

    @api.route("/categories", methods=["DELETE"])
    def delete_category():
        """DELETE /api/categories — 删除指定分类"""
        data = request.json
        ok, msg = CategoryService.delete(data.get("type"), data.get("main", ""), data.get("sub", ""))
        return Result.success(msg=msg) if ok else Result.fail(msg)

    @api.route("/categories", methods=["PUT"])
    def update_category():
        """PUT /api/categories — 修改分类（支持修改类型/主分类/子分类）"""
        data = request.json
        ok, msg = CategoryService.update(
            data.get("old_type"), data.get("old_main", ""), data.get("old_sub", ""),
            data.get("new_type"), data.get("new_main", ""), data.get("new_sub", "")
        )
        return Result.success(msg=msg) if ok else Result.fail(msg)

    @api.route("/categories", methods=["GET"])
    def get_categories():
        """GET /api/categories — 获取分类树结构和扁平列表"""
        return Result.success(CategoryService.get_all())

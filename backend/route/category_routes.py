"""分类管理路由：定义收支分类的增删改查 API 接口"""
from flask import request
from service import CategoryService
from route.result import Result


def init_category_routes(api):
    """注册分类相关路由到指定的 Blueprint 对象"""

    @api.route("/categories", methods=["GET"])
    def gc():
        """GET /api/categories — 获取分类树结构和扁平列表"""
        return Result.success(CategoryService.get_all())

    @api.route("/categories", methods=["POST"])
    def ac():
        """POST /api/categories — 添加新分类（type, main, sub）"""
        d = request.json
        succ, r = CategoryService.add(d.get("type"), d.get("main"), d.get("sub", ""))
        return Result.success(msg=r) if succ else Result.fail(r)

    @api.route("/categories", methods=["PUT"])
    def uc():
        """PUT /api/categories — 修改分类（支持修改类型/主分类/子分类）"""
        d = request.json
        succ, r = CategoryService.update(
            d.get("old_type"), d.get("old_main", ""), d.get("old_sub", ""),
            d.get("new_type"), d.get("new_main", ""), d.get("new_sub", "")
        )
        return Result.success(msg=r) if succ else Result.fail(r)

    @api.route("/categories", methods=["DELETE"])
    def dc():
        """DELETE /api/categories — 删除指定分类"""
        d = request.json
        succ, r = CategoryService.delete(d.get("type"), d.get("main", ""), d.get("sub", ""))
        return Result.success(msg=r) if succ else Result.fail(r)
"""账户管理路由：定义账户的增删改查 API 接口"""
from flask import request
from service import AccountService
from route.result import Result


def init_account_routes(api):
    """注册账户相关路由到指定的 Blueprint 对象"""

    @api.route("/accounts", methods=["GET"])
    def ga():
        """GET /api/accounts — 获取所有账户列表"""
        return Result.success(AccountService.get_all())

    @api.route("/accounts", methods=["POST"])
    def aa():
        """POST /api/accounts — 添加新账户（name, type, balance）"""
        d = request.json
        succ, r = AccountService.add(d.get("name"), d.get("type"), d.get("balance", 0))
        return Result.success(r) if succ else Result.fail(r)

    @api.route("/accounts/<int:aid>", methods=["PUT"])
    def ua(aid):
        """PUT /api/accounts/{id} — 更新指定账户的名称和类型"""
        d = request.json
        succ, r = AccountService.update(aid, d.get("name"), d.get("type"))
        return Result.success(r) if succ else Result.fail(r)

    @api.route("/accounts/<int:aid>", methods=["DELETE"])
    def da(aid):
        """DELETE /api/accounts/{id} — 删除指定账户及其关联交易"""
        succ, r = AccountService.delete(aid)
        return Result.success(msg=r) if succ else Result.fail(r)
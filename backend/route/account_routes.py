"""账户管理路由：定义账户的增删改查 API 接口"""
from flask import request
from service import AccountService
from route.result import Result


def init_account_routes(api):
    """注册账户相关路由到指定的 Blueprint 对象"""

    @api.route("/accounts", methods=["POST"])
    def add_account():
        """POST /api/accounts — 添加新账户（name, type, balance）"""
        data = request.json
        ok, result = AccountService.add(data.get("name"), data.get("type"), data.get("balance", 0))
        return Result.success(result) if ok else Result.fail(result)

    @api.route("/accounts/<int:aid>", methods=["DELETE"])
    def delete_account(aid):
        """DELETE /api/accounts/{id} — 删除指定账户及其关联交易"""
        ok, msg = AccountService.delete(aid)
        return Result.success(msg=msg) if ok else Result.fail(msg)

    @api.route("/accounts/<int:aid>", methods=["PUT"])
    def update_account(aid):
        """PUT /api/accounts/{id} — 更新指定账户的名称和类型"""
        data = request.json
        ok, result = AccountService.update(aid, data.get("name"), data.get("type"))
        return Result.success(result) if ok else Result.fail(result)

    @api.route("/accounts", methods=["GET"])
    def get_accounts():
        """GET /api/accounts — 获取所有账户列表"""
        return Result.success(AccountService.get_all())
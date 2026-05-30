"""预算管理路由：定义预算的查询、设置、汇总预警和删除接口"""
from datetime import datetime
from flask import request
from service import BudgetService
from route.result import Result


def init_budget_routes(api):
    """注册预算相关路由到指定的 Blueprint 对象"""

    @api.route("/budgets", methods=["GET"])
    def gb():
        """GET /api/budgets — 获取预算列表，可按年月筛选"""
        return Result.success(BudgetService.get_all(
            request.args.get("year", type=int),
            request.args.get("month", type=int)
        ))

    @api.route("/budgets", methods=["POST"])
    def sb():
        """POST /api/budgets — 设置预算（若已存在则覆盖更新金额）"""
        d = request.json
        succ, r = BudgetService.set(
            d.get("year"), d.get("month"),
            d.get("category"), d.get("amount")
        )
        return Result.success(msg=r) if succ else Result.fail(r)

    @api.route("/budgets/summary", methods=["GET"])
    def bs():
        """GET /api/budgets/summary — 预算汇总，含实际花费对比和超支预警"""
        now = datetime.now()
        return Result.success(BudgetService.get_summary(
            request.args.get("year", type=int, default=now.year),
            request.args.get("month", type=int, default=now.month)
        ))

    @api.route("/budgets", methods=["DELETE"])
    def db():
        """DELETE /api/budgets — 删除指定预算"""
        d = request.json
        BudgetService.delete(d.get("year"), d.get("month"), d.get("category", ""))
        return Result.success(msg="删除成功")
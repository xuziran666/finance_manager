"""预算管理路由：定义预算的查询、设置、汇总预警和删除接口"""
from datetime import datetime
from flask import request
from service import BudgetService
from route.result import Result


def init_budget_routes(api):
    """注册预算相关路由到指定的 Blueprint 对象"""

    @api.route("/budgets/summary", methods=["GET"])
    def get_budget_summary():
        """GET /api/budgets/summary — 预算汇总，含实际花费对比和超支预警"""
        now = datetime.now()
        return Result.success(BudgetService.get_summary(
            request.args.get("year", type=int, default=now.year),
            request.args.get("month", type=int, default=now.month)
        ))

    @api.route("/budgets", methods=["DELETE"])
    def delete_budget():
        """DELETE /api/budgets — 删除指定预算"""
        data = request.json
        BudgetService.delete(data.get("year"), data.get("month"), data.get("category", ""))
        return Result.success(msg="删除成功")

    @api.route("/budgets", methods=["POST"])
    def set_budget():
        """POST /api/budgets — 设置预算（若已存在则覆盖更新金额）"""
        data = request.json
        ok, msg = BudgetService.set(
            data.get("year"), data.get("month"),
            data.get("category"), data.get("amount")
        )
        return Result.success(msg=msg) if ok else Result.fail(msg)

    @api.route("/budgets", methods=["GET"])
    def get_budgets():
        """GET /api/budgets — 获取预算列表，可按年月筛选"""
        return Result.success(BudgetService.get_all(
            request.args.get("year", type=int),
            request.args.get("month", type=int)
        ))
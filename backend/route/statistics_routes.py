"""统计分析路由：提供收支数据的聚合统计接口"""
from flask import request
from service import StatisticsService
from route.result import Result


def init_statistics_routes(api):
    """注册统计相关路由到指定的 Blueprint 对象"""

    @api.route("/statistics", methods=["GET"])
    def gs():
        """GET /api/statistics — 获取统计数据（总收入/支出/趋势/分类占比）"""
        return Result.success(StatisticsService.get(
            request.args.get("account_id", type=int),
            request.args.get("start_date"),
            request.args.get("end_date"),
            request.args.get("group_by", "month")
        ))
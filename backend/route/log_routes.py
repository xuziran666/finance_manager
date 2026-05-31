"""操作日志路由：提供系统操作日志的查询接口"""
from flask import request
from service import LogService
from route.result import Result


def init_log_routes(api):
    """注册日志相关路由到指定的 Blueprint 对象"""

    @api.route("/logs", methods=["GET"])
    def get_logs():
        """GET /api/logs — 获取操作日志列表，支持限制返回条数"""
        return Result.success(LogService.get_all(request.args.get("limit", 100, type=int)))
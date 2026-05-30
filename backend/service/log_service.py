"""日志业务层：封装操作日志的查询逻辑"""
from dao import LogDAO


class LogService:
    """日志服务类，提供操作日志的查询方法"""

    @staticmethod
    def get_all(limit=100):
        """获取操作日志列表，默认返回最近 100 条"""
        return LogDAO.get_all(limit)

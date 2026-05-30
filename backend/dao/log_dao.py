"""日志数据访问层：封装 logs 表的写入与查询操作"""
from db import get_connection


class LogDAO:
    """日志数据访问对象，提供操作日志的插入和查询方法"""

    @staticmethod
    def add(action, detail, user="system", conn=None):
        """
        添加一条操作日志
        action — 操作类型（如 ADD_ACCOUNT, ADD_TRANSACTION 等）
        detail — 操作详情描述
        """
        own_conn = False
        if conn is None:
            conn = get_connection()
            own_conn = True
        try:
            c = conn.cursor()
            c.execute("INSERT INTO logs (user,action,detail) VALUES (%s,%s,%s)", (user, action, detail))
            if own_conn:
                conn.commit()
        finally:
            if own_conn:
                conn.close()

    @staticmethod
    def get_all(limit=100, conn=None):
        """获取操作日志列表，按时间降序排列，默认返回最近 100 条"""
        own_conn = False
        if conn is None:
            conn = get_connection()
            own_conn = True
        try:
            c = conn.cursor()
            c.execute("SELECT * FROM logs ORDER BY time DESC LIMIT %s", (limit,))
            return [dict(r) for r in c.fetchall()]
        finally:
            if own_conn:
                conn.close()
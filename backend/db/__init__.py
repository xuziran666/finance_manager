"""实体层 - 数据实体与数据库连接"""
from db.connection import get_connection, connection_scope

__all__ = ["get_connection", "connection_scope"]

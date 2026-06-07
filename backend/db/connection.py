"""数据库连接管理模块：基于 DBUtils 连接池实现 MySQL 连接复用"""
from contextlib import contextmanager
import pymysql
import pymysql.cursors
from dbutils.pooled_db import PooledDB
from config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME, POOL_MIN, POOL_MAX

# 连接池单例对象（全局唯一）
_pool = None


def _get_pool():
    """
    获取或创建连接池单例
    使用 DBUtils 的 PooledDB 实现连接的自动管理与复用，
    避免频繁创建/销毁数据库连接的开销。
    """
    global _pool
    if _pool is None:
        _pool = PooledDB(
            creator=pymysql,
            mincached=POOL_MIN,
            maxcached=POOL_MAX,
            maxconnections=POOL_MAX,
            blocking=True,
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            init_command="SET time_zone = '+08:00'",
        )
    return _pool


def get_connection():
    """从连接池获取一个可用连接，失败时抛出 RuntimeError"""
    try:
        return _get_pool().connection()
    except pymysql.Error as e:
        raise RuntimeError(f"数据库连接失败: {e}")


@contextmanager
def connection_scope():
    """
    事务上下文管理器：自动管理连接的获取、提交、回滚和归还
    使用方式：
        with connection_scope() as conn:
            # 在此作用域内使用 conn 进行数据库操作
            # 正常退出自动 commit
            # 异常退出自动 rollback
    """
    conn = get_connection()
    try:
        # 将连接交给调用方使用
        yield conn
        # 无异常则提交事务
        conn.commit()
    except:
        # 发生异常时回滚事务
        conn.rollback()
        # 继续向外抛出异常
        raise
    finally:
        # 无论成功失败，最终都将连接归还连接池
        conn.close()

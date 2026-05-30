"""账户数据访问层：封装 accounts 表的 CRUD 操作"""
from db import get_connection


class AccountDAO:
    """账户数据访问对象，提供账户表的增删改查方法"""

    @staticmethod
    def get_all(conn=None):
        """
        获取所有账户列表，按 id 升序排列
        conn — 可选的外部数据库连接（用于事务共享）
        """
        own_conn = False
        if conn is None:
            conn = get_connection()
            own_conn = True
        try:
            c = conn.cursor()
            c.execute("SELECT * FROM accounts ORDER BY id")
            return [dict(r) for r in c.fetchall()]
        finally:
            if own_conn:
                conn.close()

    @staticmethod
    def get_by_id(aid, conn=None):
        """根据主键 ID 查询单个账户"""
        own_conn = False
        if conn is None:
            conn = get_connection()
            own_conn = True
        try:
            c = conn.cursor()
            c.execute("SELECT * FROM accounts WHERE id=%s", (aid,))
            r = c.fetchone()
            return dict(r) if r else None
        finally:
            if own_conn:
                conn.close()

    @staticmethod
    def create(name, type_, balance=0.0, conn=None):
        """创建新账户，返回完整的账户记录"""
        own_conn = False
        if conn is None:
            conn = get_connection()
            own_conn = True
        try:
            c = conn.cursor()
            c.execute("INSERT INTO accounts (name,type,balance) VALUES (%s,%s,%s)", (name, type_, balance))
            if own_conn:
                conn.commit()
            aid = c.lastrowid
            return AccountDAO.get_by_id(aid, conn=conn)
        finally:
            if own_conn:
                conn.close()

    @staticmethod
    def update(aid, name=None, type_=None, conn=None):
        """更新账户的名称和/或类型，返回更新后的账户记录"""
        own_conn = False
        if conn is None:
            conn = get_connection()
            own_conn = True
        try:
            c = conn.cursor()
            if name:
                c.execute("UPDATE accounts SET name=%s WHERE id=%s", (name, aid))
            if type_:
                c.execute("UPDATE accounts SET type=%s WHERE id=%s", (type_, aid))
            if own_conn:
                conn.commit()
            return AccountDAO.get_by_id(aid, conn=conn)
        finally:
            if own_conn:
                conn.close()

    @staticmethod
    def update_balance(aid, bal, conn=None):
        """直接更新账户余额（用于余额修正场景）"""
        own_conn = False
        if conn is None:
            conn = get_connection()
            own_conn = True
        try:
            c = conn.cursor()
            c.execute("UPDATE accounts SET balance=%s WHERE id=%s", (bal, aid))
            if own_conn:
                conn.commit()
            return AccountDAO.get_by_id(aid, conn=conn)
        finally:
            if own_conn:
                conn.close()

    @staticmethod
    def delete(aid, conn=None):
        """删除指定账户及其关联的所有交易记录（级联删除）"""
        own_conn = False
        if conn is None:
            conn = get_connection()
            own_conn = True
        try:
            c = conn.cursor()
            c.execute("DELETE FROM transactions WHERE account_id=%s", (aid,))
            c.execute("DELETE FROM accounts WHERE id=%s", (aid,))
            if own_conn:
                conn.commit()
            return True
        finally:
            if own_conn:
                conn.close()
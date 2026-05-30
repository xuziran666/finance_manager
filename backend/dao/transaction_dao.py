"""交易记录数据访问层：封装 transactions 表的 CRUD 与分页查询"""
from datetime import datetime
from db import get_connection


class TransactionDAO:
    """交易记录数据访问对象，提供交易表的增删改查与分页方法"""

    @staticmethod
    def get_all(account_id=None, start_date=None, end_date=None, category=None, page=1, page_size=20, conn=None):
        """
        分页查询交易记录，支持按账户、日期范围、分类筛选
        返回包含交易列表、总数、页码、总页数的字典
        """
        own_conn = False
        if conn is None:
            conn = get_connection()
            own_conn = True
        try:
            c = conn.cursor()
            wh = ["1=1"]
            params = []
            if account_id:
                wh.append("t.account_id=%s")
                params.append(account_id)
            if start_date:
                wh.append("t.date>=%s")
                params.append(start_date)
            if end_date:
                wh.append("t.date<=%s")
                params.append(end_date)
            if category:
                wh.append("t.category=%s")
                params.append(category)
            wsql = " AND ".join(wh)
            # 查询符合条件的总记录数
            c.execute(f"SELECT COUNT(*) AS count FROM transactions t WHERE {wsql}", params)
            total = c.fetchone()['count']
            off = (page - 1) * page_size
            # 查询当前页数据，同时关联账户表获取账户名称和类型
            c.execute(
                f"SELECT t.*,a.name as account_name,a.type as account_type "
                f"FROM transactions t LEFT JOIN accounts a ON t.account_id=a.id "
                f"WHERE {wsql} ORDER BY t.date DESC,t.id DESC LIMIT %s OFFSET %s",
                params + [page_size, off]
            )
            return {
                "transactions": [dict(r) for r in c.fetchall()],
                "total": total, "page": page,
                "page_size": page_size, "total_pages": max(1, (total + page_size - 1) // page_size)
            }
        finally:
            if own_conn:
                conn.close()

    @staticmethod
    def create(account_id, type_, category, amount, note="", date=None, subcategory="", conn=None):
        """
        创建新交易记录，并自动更新对应账户的余额
        收入 → 余额增加；支出 → 余额减少
        """
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        own_conn = False
        if conn is None:
            conn = get_connection()
            own_conn = True
        try:
            c = conn.cursor()
            c.execute(
                "INSERT INTO transactions (account_id,type,category,subcategory,amount,note,date,created_at) "
                "VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                (account_id, type_, category, subcategory, amount, note, date, now)
            )
            tid = c.lastrowid
            # 更新账户余额
            c.execute("SELECT balance FROM accounts WHERE id=%s", (account_id,))
            row = c.fetchone()
            if row:
                bal = float(row["balance"])
                bal = bal + amount if type_ == "income" else bal - amount
                c.execute("UPDATE accounts SET balance=%s WHERE id=%s", (bal, account_id))
            if own_conn:
                conn.commit()
            return TransactionDAO.get_by_id(tid, conn=conn)
        finally:
            if own_conn:
                conn.close()

    @staticmethod
    def get_by_id(tid, conn=None):
        """根据主键 ID 查询单条交易记录（含账户信息）"""
        own_conn = False
        if conn is None:
            conn = get_connection()
            own_conn = True
        try:
            c = conn.cursor()
            c.execute(
                "SELECT t.*,a.name as account_name,a.type as account_type "
                "FROM transactions t LEFT JOIN accounts a ON t.account_id=a.id WHERE t.id=%s",
                (tid,)
            )
            r = c.fetchone()
            return dict(r) if r else None
        finally:
            if own_conn:
                conn.close()
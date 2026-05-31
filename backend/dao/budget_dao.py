"""预算数据访问层：封装 budgets 表的 upsert 与查询操作"""
from db import get_connection


class BudgetDAO:
    """预算数据访问对象，提供预算表的 upsert 与查询方法"""

    @staticmethod
    def get_all(year=None, month=None, conn=None):
        """获取预算列表，可按年月筛选"""
        own_conn = False
        if conn is None:
            conn = get_connection()
            own_conn = True
        try:
            c = conn.cursor()
            where_conditions = []
            params = []
            if year:
                where_conditions.append("year=%s")
                params.append(year)
            if month:
                where_conditions.append("month=%s")
                params.append(month)
            where_clause = " AND ".join(where_conditions) if where_conditions else "1=1"
            c.execute(f"SELECT * FROM budgets WHERE {where_clause}", params)
            return [dict(r) for r in c.fetchall()]
        finally:
            if own_conn:
                conn.close()

    @staticmethod
    def set(year, month, category, amount, subcategory="", conn=None):
        """
        设置预算（Upsert 语义）
        如果该年月分类已存在预算则更新金额，否则插入新记录
        """
        own_conn = False
        if conn is None:
            conn = get_connection()
            own_conn = True
        try:
            c = conn.cursor()
            c.execute("SELECT id FROM budgets WHERE year=%s AND month=%s AND category=%s AND subcategory=%s",
                      (year, month, category, subcategory))
            r = c.fetchone()
            if r:
                c.execute("UPDATE budgets SET amount=%s WHERE id=%s", (amount, r["id"]))
            else:
                c.execute("INSERT INTO budgets (year,month,category,subcategory,amount) VALUES (%s,%s,%s,%s,%s)",
                          (year, month, category, subcategory, amount))
            if own_conn:
                conn.commit()
        finally:
            if own_conn:
                conn.close()

    @staticmethod
    def delete(year, month, category, subcategory="", conn=None):
        """删除指定预算记录"""
        own_conn = False
        if conn is None:
            conn = get_connection()
            own_conn = True
        try:
            c = conn.cursor()
            c.execute("DELETE FROM budgets WHERE year=%s AND month=%s AND category=%s AND subcategory=%s",
                      (year, month, category, subcategory))
            if own_conn:
                conn.commit()
        finally:
            if own_conn:
                conn.close()
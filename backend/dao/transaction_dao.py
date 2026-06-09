from datetime import datetime
from db import get_connection


class TransactionDAO:

    @staticmethod
    def get_all(user_id, account_id=None, start_date=None, end_date=None, category=None, page=1, page_size=20, conn=None):
        own_conn = False
        if conn is None:
            conn = get_connection()
            own_conn = True
        try:
            c = conn.cursor()
            where_conditions = ["t.user_id=%s"]
            params = [user_id]
            if account_id:
                where_conditions.append("t.account_id=%s")
                params.append(account_id)
            if start_date:
                where_conditions.append("t.date>=%s")
                params.append(start_date)
            if end_date:
                where_conditions.append("t.date<=%s")
                params.append(end_date)
            if category:
                where_conditions.append("t.category=%s")
                params.append(category)
            where_clause = " AND ".join(where_conditions)
            c.execute(f"SELECT COUNT(*) AS count FROM transactions t WHERE {where_clause}", params)
            total = c.fetchone()['count']
            offset = (page - 1) * page_size
            c.execute(
                f"SELECT t.*,a.name as account_name,a.type as account_type "
                f"FROM transactions t LEFT JOIN accounts a ON t.account_id=a.id "
                f"WHERE {where_clause} ORDER BY t.date DESC,t.id DESC LIMIT %s OFFSET %s",
                params + [page_size, offset]
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
    def create(user_id, account_id, type_, category, amount, note="", date=None, subcategory="", conn=None):
        now_dt = datetime.now()
        now_str = now_dt.strftime("%Y-%m-%d %H:%M:%S")
        if not date:
            date = now_str
        elif len(date) <= 10:
            date = f"{date} {now_dt.strftime('%H:%M:%S')}"
        own_conn = False
        if conn is None:
            conn = get_connection()
            own_conn = True
        try:
            c = conn.cursor()
            c.execute(
                "INSERT INTO transactions (user_id,account_id,type,category,subcategory,amount,note,date,created_at) "
                "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (user_id, account_id, type_, category, subcategory, amount, note, date, now_str)
            )
            transaction_id = c.lastrowid
            c.execute("SELECT balance FROM accounts WHERE id=%s", (account_id,))
            row = c.fetchone()
            if row:
                balance = float(row["balance"])
                balance = balance + amount if type_ == "income" else balance - amount
                c.execute("UPDATE accounts SET balance=%s WHERE id=%s", (balance, account_id))
            if own_conn:
                conn.commit()
            return TransactionDAO.get_by_id(transaction_id, conn=conn)
        finally:
            if own_conn:
                conn.close()

    @staticmethod
    def delete(transaction_id, user_id=None, conn=None):
        own_conn = False
        if conn is None:
            conn = get_connection()
            own_conn = True
        try:
            c = conn.cursor()
            txn = TransactionDAO.get_by_id(transaction_id, conn=conn)
            if not txn:
                return False
            if user_id is None:
                from context import get_current_user_id
                user_id = get_current_user_id()
            if user_id is not None and txn["user_id"] != user_id:
                return False
            if txn["type"] == "income":
                c.execute("UPDATE accounts SET balance = balance - %s WHERE id = %s", (txn["amount"], txn["account_id"]))
            elif txn["type"] == "expense":
                c.execute("UPDATE accounts SET balance = balance + %s WHERE id = %s", (txn["amount"], txn["account_id"]))
            c.execute("DELETE FROM transactions WHERE id = %s", (transaction_id,))
            if own_conn:
                conn.commit()
            return True
        finally:
            if own_conn:
                conn.close()

    @staticmethod
    def get_by_id(transaction_id, user_id=None, conn=None):
        own_conn = False
        if conn is None:
            conn = get_connection()
            own_conn = True
        try:
            c = conn.cursor()
            if user_id is None:
                from context import get_current_user_id
                user_id = get_current_user_id()
            if user_id:
                c.execute(
                    "SELECT t.*,a.name as account_name,a.type as account_type "
                    "FROM transactions t LEFT JOIN accounts a ON t.account_id=a.id WHERE t.id=%s AND t.user_id=%s",
                    (transaction_id, user_id)
                )
            else:
                c.execute(
                    "SELECT t.*,a.name as account_name,a.type as account_type "
                    "FROM transactions t LEFT JOIN accounts a ON t.account_id=a.id WHERE t.id=%s",
                    (transaction_id,)
                )
            row = c.fetchone()
            return dict(row) if row else None
        finally:
            if own_conn:
                conn.close()

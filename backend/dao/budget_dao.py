from db import get_connection


class BudgetDAO:

    @staticmethod
    def get_all(user_id, year=None, month=None, conn=None):
        own_conn = False
        if conn is None:
            conn = get_connection()
            own_conn = True
        try:
            c = conn.cursor()
            where_conditions = ["user_id=%s"]
            params = [user_id]
            if year:
                where_conditions.append("year=%s")
                params.append(year)
            if month:
                where_conditions.append("month=%s")
                params.append(month)
            where_clause = " AND ".join(where_conditions)
            c.execute(f"SELECT * FROM budgets WHERE {where_clause}", params)
            return [dict(r) for r in c.fetchall()]
        finally:
            if own_conn:
                conn.close()

    @staticmethod
    def set(user_id, year, month, category, amount, subcategory="", conn=None):
        own_conn = False
        if conn is None:
            conn = get_connection()
            own_conn = True
        try:
            c = conn.cursor()
            c.execute(
                "SELECT id FROM budgets WHERE user_id=%s AND year=%s AND month=%s AND category=%s AND subcategory=%s",
                (user_id, year, month, category, subcategory)
            )
            r = c.fetchone()
            if r:
                c.execute("UPDATE budgets SET amount=%s WHERE id=%s", (amount, r["id"]))
            else:
                c.execute(
                    "INSERT INTO budgets (user_id,year,month,category,subcategory,amount) VALUES (%s,%s,%s,%s,%s,%s)",
                    (user_id, year, month, category, subcategory, amount)
                )
            if own_conn:
                conn.commit()
        finally:
            if own_conn:
                conn.close()

    @staticmethod
    def delete(user_id, year, month, category, subcategory="", conn=None):
        own_conn = False
        if conn is None:
            conn = get_connection()
            own_conn = True
        try:
            c = conn.cursor()
            c.execute(
                "DELETE FROM budgets WHERE user_id=%s AND year=%s AND month=%s AND category=%s AND subcategory=%s",
                (user_id, year, month, category, subcategory)
            )
            if own_conn:
                conn.commit()
        finally:
            if own_conn:
                conn.close()

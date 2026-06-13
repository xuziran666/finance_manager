from db import get_connection


class LogDAO:

    def add(self, user_id, action, detail, conn=None):
        own_conn = False
        if conn is None:
            conn = get_connection()
            own_conn = True
        try:
            c = conn.cursor()
            c.execute("INSERT INTO logs (user_id,action,detail) VALUES (%s,%s,%s)",
                      (user_id, action, detail))
            if own_conn:
                conn.commit()
        finally:
            if own_conn:
                conn.close()

    def get_all(self, user_id, limit=100, conn=None):
        own_conn = False
        if conn is None:
            conn = get_connection()
            own_conn = True
        try:
            c = conn.cursor()
            c.execute("SELECT * FROM logs WHERE user_id=%s ORDER BY time DESC LIMIT %s",
                      (user_id, limit))
            return [dict(r) for r in c.fetchall()]
        finally:
            if own_conn:
                conn.close()

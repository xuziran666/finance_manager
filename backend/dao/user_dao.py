from db import get_connection


class UserDAO:

    def get_by_username(self, username, conn=None):
        own_conn = False
        if conn is None:
            conn = get_connection()
            own_conn = True
        try:
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE username=%s", (username,))
            row = c.fetchone()
            return dict(row) if row else None
        finally:
            if own_conn:
                conn.close()

    def create(self, username, password_hash, conn=None):
        own_conn = False
        if conn is None:
            conn = get_connection()
            own_conn = True
        try:
            c = conn.cursor()
            c.execute("INSERT INTO users (username,password_hash) VALUES (%s,%s)", (username, password_hash))
            if own_conn:
                conn.commit()
            return c.lastrowid
        finally:
            if own_conn:
                conn.close()

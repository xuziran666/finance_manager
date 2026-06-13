from db import get_connection
from context import get_current_user_id


class AccountDAO:

    def get_all(self, user_id, conn=None):
        own_conn = False
        if conn is None:
            conn = get_connection()
            own_conn = True
        try:
            c = conn.cursor()
            c.execute("SELECT * FROM accounts WHERE user_id=%s ORDER BY id", (user_id,))
            return [dict(r) for r in c.fetchall()]
        finally:
            if own_conn:
                conn.close()

    def get_by_id(self, aid, user_id=None, conn=None):
        own_conn = False
        if conn is None:
            conn = get_connection()
            own_conn = True
        try:
            c = conn.cursor()
            if user_id is None:
                user_id = get_current_user_id()
            if user_id:
                c.execute("SELECT * FROM accounts WHERE id=%s AND user_id=%s", (aid, user_id))
            else:
                c.execute("SELECT * FROM accounts WHERE id=%s", (aid,))
            row = c.fetchone()
            return dict(row) if row else None
        finally:
            if own_conn:
                conn.close()

    def create(self, user_id, name, type_, balance=0.0, conn=None):
        own_conn = False
        if conn is None:
            conn = get_connection()
            own_conn = True
        try:
            c = conn.cursor()
            c.execute("INSERT INTO accounts (user_id,name,type,balance) VALUES (%s,%s,%s,%s)",
                      (user_id, name, type_, balance))
            if own_conn:
                conn.commit()
            aid = c.lastrowid
            return self.get_by_id(aid, conn=conn)
        finally:
            if own_conn:
                conn.close()

    def update(self, aid, user_id=None, name=None, type_=None, conn=None):
        own_conn = False
        if conn is None:
            conn = get_connection()
            own_conn = True
        try:
            c = conn.cursor()
            if user_id is None:
                user_id = get_current_user_id()
            if user_id:
                c.execute("SELECT user_id FROM accounts WHERE id=%s", (aid,))
                row = c.fetchone()
                if not row or row["user_id"] != user_id:
                    return None
            if name is not None:
                c.execute("UPDATE accounts SET name=%s WHERE id=%s", (name, aid))
            if type_ is not None:
                c.execute("UPDATE accounts SET type=%s WHERE id=%s", (type_, aid))
            if own_conn:
                conn.commit()
            return self.get_by_id(aid, conn=conn)
        finally:
            if own_conn:
                conn.close()

    def update_balance(self, aid, bal, conn=None):
        own_conn = False
        if conn is None:
            conn = get_connection()
            own_conn = True
        try:
            c = conn.cursor()
            c.execute("UPDATE accounts SET balance=%s WHERE id=%s", (bal, aid))
            if own_conn:
                conn.commit()
            return self.get_by_id(aid, conn=conn)
        finally:
            if own_conn:
                conn.close()

    def delete(self, aid, user_id=None, conn=None):
        own_conn = False
        if conn is None:
            conn = get_connection()
            own_conn = True
        try:
            c = conn.cursor()
            if user_id is None:
                user_id = get_current_user_id()
            if user_id:
                c.execute("SELECT user_id FROM accounts WHERE id=%s", (aid,))
                row = c.fetchone()
                if not row or row["user_id"] != user_id:
                    return False
            c.execute("DELETE FROM transactions WHERE account_id=%s", (aid,))
            c.execute("DELETE FROM accounts WHERE id=%s", (aid,))
            if own_conn:
                conn.commit()
            return self.get_by_id(aid, conn=conn)
        finally:
            if own_conn:
                conn.close()

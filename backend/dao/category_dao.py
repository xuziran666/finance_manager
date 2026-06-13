from db import get_connection, connection_scope


class CategoryDAO:

    def copy_defaults(self, new_user_id, conn=None):
        own_conn = False
        if conn is None:
            conn = get_connection()
            own_conn = True
        try:
            c = conn.cursor()
            c.execute(
                "INSERT INTO categories (user_id, type, main, sub) "
                "SELECT %s, type, main, sub FROM categories WHERE user_id=-1",
                (new_user_id,)
            )
            if own_conn:
                conn.commit()
        finally:
            if own_conn:
                conn.close()

    def create(self, type_, main, sub="", conn=None, user_id=None):
        own_conn = False
        if conn is None:
            conn = get_connection()
            own_conn = True
        try:
            c = conn.cursor()
            c.execute("INSERT INTO categories (user_id,type,main,sub) VALUES (%s,%s,%s,%s)",
                      (user_id, type_, main, sub))
            if own_conn:
                conn.commit()
        finally:
            if own_conn:
                conn.close()

    def delete(self, user_id, type_, main, sub="", conn=None):
        own_conn = False
        if conn is None:
            conn = get_connection()
            own_conn = True
        try:
            c = conn.cursor()
            if sub == "":
                c.execute("DELETE FROM categories WHERE user_id=%s AND type=%s AND main=%s",
                          (user_id, type_, main))
            else:
                c.execute("DELETE FROM categories WHERE user_id=%s AND type=%s AND main=%s AND sub=%s",
                          (user_id, type_, main, sub))
            if own_conn:
                conn.commit()
            return c.rowcount > 0
        finally:
            if own_conn:
                conn.close()

    def update(self, user_id, old_type, old_main, old_sub, new_type, new_main, new_sub, conn=None):
        own_conn = False
        if conn is None:
            conn = get_connection()
            own_conn = True
        try:
            c = conn.cursor()
            c.execute(
                "UPDATE categories SET type=%s,main=%s,sub=%s "
                "WHERE user_id=%s AND type=%s AND main=%s AND sub=%s",
                (new_type, new_main, new_sub, user_id, old_type, old_main, old_sub)
            )
            if own_conn:
                conn.commit()
            return c.rowcount > 0
        finally:
            if own_conn:
                conn.close()

    def get_all(self, user_id, conn=None):
        own_conn = False
        if conn is None:
            conn = get_connection()
            own_conn = True
        try:
            c = conn.cursor()
            c.execute("SELECT * FROM categories WHERE user_id=%s ORDER BY type,main,sub", (user_id,))
            return [dict(r) for r in c.fetchall()]
        finally:
            if own_conn:
                conn.close()

    def get_tree(self, user_id, conn=None):
        cats = self.get_all(user_id, conn=conn)
        tree = {}
        for cat in cats:
            cat_type = cat["type"]
            cat_main = cat["main"]
            cat_sub = cat["sub"]
            if cat_type not in tree:
                tree[cat_type] = {}
            if cat_main not in tree[cat_type]:
                tree[cat_type][cat_main] = []
            if cat_sub:
                tree[cat_type][cat_main].append(cat_sub)
        return tree

    def exists(self, user_id, type_, main, sub="", conn=None):
        own_conn = False
        if conn is None:
            conn = get_connection()
            own_conn = True
        try:
            c = conn.cursor()
            c.execute(
                "SELECT COUNT(*) AS count FROM categories WHERE user_id=%s AND type=%s AND main=%s AND sub=%s",
                (user_id, type_, main, sub)
            )
            return c.fetchone()['count'] > 0
        finally:
            if own_conn:
                conn.close()

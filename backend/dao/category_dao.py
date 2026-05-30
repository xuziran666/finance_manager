"""分类数据访问层：封装 categories 表的 CRUD 与树结构构建"""
from db import get_connection


class CategoryDAO:
    """分类数据访问对象，提供分类表的增删改查与树形结构生成方法"""

    @staticmethod
    def get_all(conn=None):
        """获取全部分类列表，按类型/主分类/子分类排序"""
        own_conn = False
        if conn is None:
            conn = get_connection()
            own_conn = True
        try:
            c = conn.cursor()
            c.execute("SELECT * FROM categories ORDER BY type,main,sub")
            return [dict(r) for r in c.fetchall()]
        finally:
            if own_conn:
                conn.close()

    @staticmethod
    def get_tree(conn=None):
        """
        将扁平分类数据转换为树形结构
        返回格式: {"income": {"工资": ["基本工资", ...]}, "expense": {...}}
        """
        cats = CategoryDAO.get_all(conn=conn)
        tree = {"income": {}, "expense": {}}
        for cat in cats:
            tp = cat["type"]
            m = cat["main"]
            s = cat["sub"]
            if m not in tree[tp]:
                tree[tp][m] = []
            if s:
                tree[tp][m].append(s)
        return tree

    @staticmethod
    def exists(type_, main, sub="", conn=None):
        """检查指定分类组合是否已存在（防重复）"""
        own_conn = False
        if conn is None:
            conn = get_connection()
            own_conn = True
        try:
            c = conn.cursor()
            c.execute("SELECT COUNT(*) AS count FROM categories WHERE type=%s AND main=%s AND sub=%s",
                      (type_, main, sub))
            return c.fetchone()['count'] > 0
        finally:
            if own_conn:
                conn.close()

    @staticmethod
    def create(type_, main, sub="", conn=None):
        """插入新分类记录"""
        own_conn = False
        if conn is None:
            conn = get_connection()
            own_conn = True
        try:
            c = conn.cursor()
            c.execute("INSERT INTO categories (type,main,sub) VALUES (%s,%s,%s)", (type_, main, sub))
            if own_conn:
                conn.commit()
        finally:
            if own_conn:
                conn.close()

    @staticmethod
    def update(ot, om, os_, nt, nm, ns_, conn=None):
        """修改分类（type/main/sub 均可更改），返回是否更新成功"""
        own_conn = False
        if conn is None:
            conn = get_connection()
            own_conn = True
        try:
            c = conn.cursor()
            c.execute("UPDATE categories SET type=%s,main=%s,sub=%s WHERE type=%s AND main=%s AND sub=%s",
                      (nt, nm, ns_, ot, om, os_))
            if own_conn:
                conn.commit()
            return c.rowcount > 0
        finally:
            if own_conn:
                conn.close()

    @staticmethod
    def delete(type_, main, sub="", conn=None):
        """删除指定分类，返回是否删除成功"""
        own_conn = False
        if conn is None:
            conn = get_connection()
            own_conn = True
        try:
            c = conn.cursor()
            c.execute("DELETE FROM categories WHERE type=%s AND main=%s AND sub=%s", (type_, main, sub))
            if own_conn:
                conn.commit()
            return c.rowcount > 0
        finally:
            if own_conn:
                conn.close()
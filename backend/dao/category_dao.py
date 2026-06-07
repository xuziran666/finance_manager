"""分类数据访问层：封装 categories 表的 CRUD 与树结构构建"""
from db import get_connection


class CategoryDAO:
    """分类数据访问对象，提供分类表的增删改查与树形结构生成方法"""

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
    def delete(type_, main, sub="", conn=None):
        """删除指定分类，返回是否删除成功（主分类时级联删除其下所有子分类）"""
        own_conn = False
        if conn is None:
            conn = get_connection()
            own_conn = True
        try:
            c = conn.cursor()
            if sub == "":
                c.execute("DELETE FROM categories WHERE type=%s AND main=%s", (type_, main))
            else:
                c.execute("DELETE FROM categories WHERE type=%s AND main=%s AND sub=%s", (type_, main, sub))
            if own_conn:
                conn.commit()
            return c.rowcount > 0
        finally:
            if own_conn:
                conn.close()

    @staticmethod
    def update(old_type, old_main, old_sub, new_type, new_main, new_sub, conn=None):
        """修改分类（type/main/sub 均可更改），返回是否更新成功"""
        own_conn = False
        if conn is None:
            conn = get_connection()
            own_conn = True
        try:
            c = conn.cursor()
            c.execute("UPDATE categories SET type=%s,main=%s,sub=%s WHERE type=%s AND main=%s AND sub=%s",
                      (new_type, new_main, new_sub, old_type, old_main, old_sub))
            if own_conn:
                conn.commit()
            return c.rowcount > 0
        finally:
            if own_conn:
                conn.close()

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
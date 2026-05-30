"""分类业务层：封装收支分类的增删改查与去重校验"""
from dao import CategoryDAO, LogDAO
from db import connection_scope


class CategoryService:
    """分类服务类，提供分类管理的核心业务方法"""

    @staticmethod
    def get_all():
        """获取全部分类，返回树形结构 + 扁平列表"""
        with connection_scope() as conn:
            return {"tree": CategoryDAO.get_tree(conn=conn), "flat": CategoryDAO.get_all(conn=conn)}

    @staticmethod
    def add(type_, main, sub=""):
        """
        添加新分类
        校验：类型和主分类不能为空，同一组合不能重复
        """
        if not type_ or not main:
            return False, "请填写完整"
        with connection_scope() as conn:
            if CategoryDAO.exists(type_, main, sub, conn=conn):
                return False, "分类已存在"
            CategoryDAO.create(type_, main, sub, conn=conn)
            LogDAO.add("ADD_CATEGORY", f"{type_}:{main}:{sub}", conn=conn)
            return True, "添加成功"

    @staticmethod
    def update(ot, om, os_, nt, nm, ns_):
        """
        修改分类（原分类 → 新分类）
        返回 False 表示原分类不存在
        """
        with connection_scope() as conn:
            if CategoryDAO.update(ot, om, os_, nt, nm, ns_, conn=conn):
                LogDAO.add("UPDATE_CATEGORY", f"{ot}:{om}:{os_}->{nt}:{nm}:{ns_}", conn=conn)
                return True, "修改成功"
            return False, "原分类不存在"

    @staticmethod
    def delete(type_, main, sub=""):
        """删除指定分类，返回 False 表示分类不存在"""
        with connection_scope() as conn:
            if CategoryDAO.delete(type_, main, sub, conn=conn):
                LogDAO.add("DELETE_CATEGORY", f"{type_}:{main}:{sub}", conn=conn)
                return True, "删除成功"
            return False, "分类不存在"
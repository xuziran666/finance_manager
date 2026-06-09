from dao import CategoryDAO, LogDAO
from db import connection_scope


class CategoryService:

    @staticmethod
    def add(user_id, type_, main, sub=""):
        if not type_ or not main:
            return False, "请填写完整"
        with connection_scope() as conn:
            if CategoryDAO.exists(user_id, type_, main, sub, conn=conn):
                return False, "分类已存在"
            CategoryDAO.create(type_, main, sub, conn=conn, user_id=user_id)
            LogDAO.add(user_id, "ADD_CATEGORY", f"{type_}:{main}:{sub}", conn=conn)
            return True, "添加成功"

    @staticmethod
    def delete(user_id, type_, main, sub=""):
        with connection_scope() as conn:
            if CategoryDAO.delete(user_id, type_, main, sub, conn=conn):
                return True, "删除成功"
            return False, "分类不存在"

    @staticmethod
    def update(user_id, old_type, old_main, old_sub, new_type, new_main, new_sub):
        with connection_scope() as conn:
            if CategoryDAO.update(user_id, old_type, old_main, old_sub, new_type, new_main, new_sub, conn=conn):
                return True, "修改成功"
            return False, "原分类不存在"

    @staticmethod
    def get_all(user_id):
        with connection_scope() as conn:
            return {"tree": CategoryDAO.get_tree(user_id, conn=conn), "flat": CategoryDAO.get_all(user_id, conn=conn)}

from dao import CategoryDAO, LogDAO
from db import connection_scope


class CategoryService:

    def __init__(self, category_dao: CategoryDAO, log_dao: LogDAO):
        self.category_dao = category_dao
        self.log_dao = log_dao

    def add(self, user_id, type_, main, sub=""):
        if not type_ or not main:
            return False, "请填写完整"
        with connection_scope() as conn:
            if self.category_dao.exists(user_id, type_, main, sub, conn=conn):
                return False, "分类已存在"
            self.category_dao.create(type_, main, sub, conn=conn, user_id=user_id)
            self.log_dao.add(user_id, "ADD_CATEGORY", f"{type_}:{main}:{sub}", conn=conn)
            return True, "添加成功"

    def delete(self, user_id, type_, main, sub=""):
        with connection_scope() as conn:
            if self.category_dao.delete(user_id, type_, main, sub, conn=conn):
                return True, "删除成功"
            return False, "分类不存在"

    def update(self, user_id, old_type, old_main, old_sub, new_type, new_main, new_sub):
        with connection_scope() as conn:
            if self.category_dao.update(user_id, old_type, old_main, old_sub, new_type, new_main, new_sub, conn=conn):
                return True, "修改成功"
            return False, "原分类不存在"

    def get_all(self, user_id):
        with connection_scope() as conn:
            return {"tree": self.category_dao.get_tree(user_id, conn=conn), "flat": self.category_dao.get_all(user_id, conn=conn)}

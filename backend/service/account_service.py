from dao import AccountDAO, LogDAO
from db import connection_scope
from context import get_current_user_id


class AccountService:

    def __init__(self, account_dao: AccountDAO, log_dao: LogDAO):
        self.account_dao = account_dao
        self.log_dao = log_dao

    def get_all(self, user_id):
        return self.account_dao.get_all(user_id)

    def add(self, user_id, name, type_, balance=0):
        if not name or not name.strip():
            return False, "名称不能为空"
        if not type_:
            return False, "类型不能为空"
        try:
            balance = float(balance)
            if balance < 0:
                return False, "余额不能为负"
        except:
            return False, "余额格式错误"
        with connection_scope() as conn:
            a = self.account_dao.create(user_id, name.strip(), type_, balance, conn=conn)
            self.log_dao.add(user_id, "ADD_ACCOUNT", f"添加账户:{name}", conn=conn)
            return True, a

    def update(self, aid, name=None, type_=None):
        if name is not None and not name.strip():
            return False, "名称不能为空"
        with connection_scope() as conn:
            user_id = get_current_user_id()
            a = self.account_dao.get_by_id(aid, user_id=user_id, conn=conn)
            if not a:
                return False, "账户不存在"
            updated = self.account_dao.update(aid, user_id=user_id, name=name.strip() if name else None, type_=type_, conn=conn)
            detail = f"更新账户:{a['name']}"
            if name:
                detail += f" → {name}"
            self.log_dao.add(user_id, "UPDATE_ACCOUNT", detail, conn=conn)
            return True, updated

    def delete(self, aid):
        with connection_scope() as conn:
            user_id = get_current_user_id()
            acc = self.account_dao.get_by_id(aid, user_id=user_id, conn=conn)
            if not acc:
                return False, "账户不存在"
            self.account_dao.delete(aid, user_id=user_id, conn=conn)
            self.log_dao.add(user_id, "DELETE_ACCOUNT", f"删除账户:{acc['name']}", conn=conn)
            return True, "删除成功"

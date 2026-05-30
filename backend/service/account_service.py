"""账户业务层：封装账户的增删改查业务逻辑与数据校验"""
from dao import AccountDAO, LogDAO
from db import connection_scope


class AccountService:
    """账户服务类，提供账户管理的核心业务方法"""

    @staticmethod
    def get_all():
        """获取所有账户列表"""
        return AccountDAO.get_all()

    @staticmethod
    def add(name, type_, balance=0):
        """
        添加新账户
        校验：名称和类型不能为空，余额不能为负
        成功时自动记录操作日志
        """
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
            a = AccountDAO.create(name.strip(), type_, balance, conn=conn)
            LogDAO.add("ADD_ACCOUNT", f"添加账户:{name}", conn=conn)
            return True, a

    @staticmethod
    def update(aid, name=None, type_=None):
        """
        更新账户信息
        校验：名称不能为空字符串
        返回 (是否成功, 结果数据或错误信息)
        """
        if name and not name.strip():
            return False, "名称不能为空"
        with connection_scope() as conn:
            a = AccountDAO.update(aid, name.strip() if name else None, type_, conn=conn)
            if not a:
                return False, "账户不存在"
            LogDAO.add("UPDATE_ACCOUNT", f"更新账户:{aid}", conn=conn)
            return True, a

    @staticmethod
    def delete(aid):
        """删除指定账户，同时级联删除其交易记录"""
        with connection_scope() as conn:
            AccountDAO.delete(aid, conn=conn)
            LogDAO.add("DELETE_ACCOUNT", f"删除账户:{aid}", conn=conn)
            return True, "删除成功"
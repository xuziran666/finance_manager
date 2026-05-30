"""交易记录业务层：封装收支记录与转账的核心业务逻辑"""
from datetime import datetime
from dao import AccountDAO, TransactionDAO, LogDAO
from db import connection_scope


class TransactionService:
    """交易服务类，提供交易记录的查询、添加、转账等业务方法"""

    @staticmethod
    def get_all(*a, **k):
        """查询交易记录，透传给 TransactionDAO"""
        return TransactionDAO.get_all(*a, **k)

    @staticmethod
    def add(account_id, type_, category, amount, note="", date=None, subcategory=""):
        """
        添加一条交易记录
        校验：账户必选、类型合法、分类必填、金额非负
        成功时自动更新对应账户余额并记录操作日志
        """
        if not account_id:
            return False, "请选择账户"
        if type_ not in ("income", "expense"):
            return False, "类型错误"
        if not category:
            return False, "请选择分类"
        try:
            amount = float(amount)
            if amount < 0:
                return False, "金额不能为负"
        except:
            return False, "金额格式错误"
        with connection_scope() as conn:
            acct = AccountDAO.get_by_id(account_id, conn=conn)
            if not acct:
                return False, "账户不存在"
            txn = TransactionDAO.create(account_id, type_, category, amount, note, date, subcategory, conn=conn)
            LogDAO.add("ADD_TRANSACTION", f"账户[{account_id}] {type_}:{amount}", conn=conn)
            return True, txn

    @staticmethod
    def transfer(frm, to_, amount, note=""):
        """
        账户间转账
        同时生成一笔转出（支出）和一笔转入（收入）记录
        校验：账户存在、不能转给自己、余额充足
        """
        try:
            amount = float(amount)
            if amount <= 0:
                return False, "金额必须>0"
        except:
            return False, "金额格式错误"
        with connection_scope() as conn:
            fa = AccountDAO.get_by_id(frm, conn=conn)
            ta = AccountDAO.get_by_id(to_, conn=conn)
            if not fa or not ta:
                return False, "账户不存在"
            if frm == to_:
                return False, "不能转给自己"
            if fa["balance"] < amount:
                return False, f"余额不足:{fa['balance']:.2f}"
            dt = datetime.now().strftime("%Y-%m-%d")
            n1 = f"转至{ta['name']}:{note}" if note else f"转至{ta['name']}"
            n2 = f"来自{fa['name']}:{note}" if note else f"来自{fa['name']}"
            TransactionDAO.create(frm, "expense", "转账", amount, n1, dt, conn=conn)
            TransactionDAO.create(to_, "income", "转账", amount, n2, dt, conn=conn)
            LogDAO.add("TRANSFER", f"从{frm}转{amount}到{to_}", conn=conn)
            return True, "转账成功"
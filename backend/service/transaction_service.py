"""交易记录业务层：封装收支记录与转账的核心业务逻辑"""
from datetime import datetime
from dao import AccountDAO, TransactionDAO, LogDAO
from db import connection_scope


class TransactionService:
    """交易服务类，提供交易记录的查询、添加、转账等业务方法"""

    @staticmethod
    def get_all(*args, **kwargs):
        """查询交易记录，透传给 TransactionDAO"""
        return TransactionDAO.get_all(*args, **kwargs)

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
            account = AccountDAO.get_by_id(account_id, conn=conn)
            if not account:
                return False, "账户不存在"
            if type_ == "expense" and account["balance"] < amount:
                return False, f"余额不足:{account['balance']:.2f}"
            transaction = TransactionDAO.create(account_id, type_, category, amount, note, date, subcategory, conn=conn)
            LogDAO.add("ADD_TRANSACTION", f"账户[{account_id}] {type_}:{amount}", conn=conn)
            return True, transaction

    @staticmethod
    def delete(transaction_id):
        with connection_scope() as conn:
            txn = TransactionDAO.get_by_id(transaction_id, conn=conn)
            if not txn:
                return False, "交易不存在"
            TransactionDAO.delete(transaction_id, conn=conn)
            LogDAO.add("DELETE_TRANSACTION", f"删除交易[{transaction_id}]:{txn['type']} {txn['amount']}", conn=conn)
            return True, "删除成功"

    @staticmethod
    def transfer(source_id, target_id, amount, note=""):
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
            from_account = AccountDAO.get_by_id(source_id, conn=conn)
            to_account = AccountDAO.get_by_id(target_id, conn=conn)
            if not from_account or not to_account:
                return False, "账户不存在"
            if source_id == target_id:
                return False, "不能转给自己"
            if from_account["balance"] < amount:
                return False, f"余额不足:{from_account['balance']:.2f}"
            today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            outgoing_note = f"转至{to_account['name']}:{note}" if note else f"转至{to_account['name']}"
            incoming_note = f"来自{from_account['name']}:{note}" if note else f"来自{from_account['name']}"
            TransactionDAO.create(source_id, "expense", "转账", amount, outgoing_note, today, conn=conn)
            TransactionDAO.create(target_id, "income", "转账", amount, incoming_note, today, conn=conn)
            LogDAO.add("TRANSFER", f"从{source_id}转{amount}到{target_id}", conn=conn)
            return True, "转账成功"

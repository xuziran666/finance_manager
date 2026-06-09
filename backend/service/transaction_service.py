from datetime import datetime
from dao import AccountDAO, TransactionDAO, LogDAO
from db import connection_scope
from context import get_current_user_id


class TransactionService:

    @staticmethod
    def get_all(user_id, *args, **kwargs):
        return TransactionDAO.get_all(user_id, *args, **kwargs)

    @staticmethod
    def add(user_id, account_id, type_, category, amount, note="", date=None, subcategory=""):
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
            if not account or account.get("user_id") != user_id:
                return False, "账户不存在"
            if type_ == "expense" and account["balance"] < amount:
                return False, f"余额不足:{account['balance']:.2f}"
            transaction = TransactionDAO.create(
                user_id, account_id, type_, category, amount, note, date, subcategory, conn=conn
            )
            LogDAO.add(user_id, "ADD_TRANSACTION", f"账户[{account_id}] {type_}:{amount}", conn=conn)
            return True, transaction

    @staticmethod
    def delete(transaction_id):
        with connection_scope() as conn:
            user_id = get_current_user_id()
            txn = TransactionDAO.get_by_id(transaction_id, user_id=user_id, conn=conn)
            if not txn:
                return False, "交易不存在"
            TransactionDAO.delete(transaction_id, user_id=user_id, conn=conn)
            LogDAO.add(user_id, "DELETE_TRANSACTION", f"删除交易[{transaction_id}]:{txn['type']} {txn['amount']}", conn=conn)
            return True, "删除成功"

    @staticmethod
    def transfer(user_id, source_id, target_id, amount, note=""):
        try:
            amount = float(amount)
            if amount <= 0:
                return False, "金额必须>0"
        except:
            return False, "金额格式错误"
        with connection_scope() as conn:
            from_account = AccountDAO.get_by_id(source_id, conn=conn)
            to_account = AccountDAO.get_by_id(target_id, conn=conn)
            if not from_account or from_account.get("user_id") != user_id:
                return False, "转出账户不存在"
            if not to_account or to_account.get("user_id") != user_id:
                return False, "转入账户不存在"
            if source_id == target_id:
                return False, "不能转给自己"
            if from_account["balance"] < amount:
                return False, f"余额不足:{from_account['balance']:.2f}"
            today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            outgoing_note = f"转至{to_account['name']}:{note}" if note else f"转至{to_account['name']}"
            incoming_note = f"来自{from_account['name']}:{note}" if note else f"来自{from_account['name']}"
            TransactionDAO.create(user_id, source_id, "expense", "转账", amount, outgoing_note, today, conn=conn)
            TransactionDAO.create(user_id, target_id, "income", "转账", amount, incoming_note, today, conn=conn)
            LogDAO.add(user_id, "TRANSFER", f"从{source_id}转{amount}到{target_id}", conn=conn)
            return True, "转账成功"

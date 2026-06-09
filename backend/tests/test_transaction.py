import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from tests import ensure_test_user, cleanup_test_user
from dao import AccountDAO, TransactionDAO
from service import TransactionService
from db import connection_scope

_uid = None

def setUpModule():
    global _uid
    _uid = ensure_test_user("test_transaction_user")


def tearDownModule():
    cleanup_test_user("test_transaction_user")


class TestTransactionDAO(unittest.TestCase):

    def setUp(self):
        with connection_scope() as conn:
            c = conn.cursor()
            c.execute("DELETE FROM transactions WHERE account_id IN (SELECT id FROM accounts WHERE name LIKE '测试%')")
            c.execute("DELETE FROM accounts WHERE name LIKE '测试%'")
        self.aid = AccountDAO.create(_uid, "测试交易账户", "bank", 5000.00)["id"]

    def test_create_transaction(self):
        t = TransactionDAO.create(_uid, self.aid, "income", "工资", 3000.00, "测试收入")
        self.assertIsNotNone(t)
        self.assertEqual(float(t["amount"]), 3000.00)
        a = AccountDAO.get_by_id(self.aid)
        self.assertEqual(float(a["balance"]), 8000.00)

    def test_get_all_pagination(self):
        for i in range(5):
            TransactionDAO.create(_uid, self.aid, "expense", "餐饮", 10.00 + i, f"测试{i}")
        r = TransactionDAO.get_all(_uid, account_id=self.aid, page=1, page_size=3)
        self.assertEqual(len(r["transactions"]), 3)
        self.assertEqual(r["total"], 5)
        self.assertEqual(r["total_pages"], 2)


class TestTransactionService(unittest.TestCase):

    def setUp(self):
        with connection_scope() as conn:
            c = conn.cursor()
            c.execute("DELETE FROM transactions WHERE account_id IN (SELECT id FROM accounts WHERE name LIKE '测试%')")
            c.execute("DELETE FROM accounts WHERE name LIKE '测试%'")
        self.aid = AccountDAO.create(_uid, "测试交易服务账户", "bank", 10000.00)["id"]

    def test_add_income(self):
        succ, t = TransactionService.add(_uid, self.aid, "income", "工资", 5000.00)
        self.assertTrue(succ)

    def test_add_expense(self):
        succ, t = TransactionService.add(_uid, self.aid, "expense", "餐饮", 100.00)
        self.assertTrue(succ)

    def test_transfer(self):
        aid2 = AccountDAO.create(_uid, "测试账户B", "alipay", 0.00)["id"]
        succ, msg = TransactionService.transfer(_uid, self.aid, aid2, 2000.00)
        self.assertTrue(succ)
        a1 = AccountDAO.get_by_id(self.aid)
        a2 = AccountDAO.get_by_id(aid2)
        self.assertEqual(float(a1["balance"]), 8000.00)
        self.assertEqual(float(a2["balance"]), 2000.00)

    def test_transfer_insufficient(self):
        aid2 = AccountDAO.create(_uid, "测试账户C", "cash", 0.00)["id"]
        succ, msg = TransactionService.transfer(_uid, self.aid, aid2, 999999.00)
        self.assertFalse(succ)

    def test_transfer_self(self):
        succ, msg = TransactionService.transfer(_uid, self.aid, self.aid, 100.00)
        self.assertFalse(succ)


if __name__ == "__main__":
    unittest.main(verbosity=2)

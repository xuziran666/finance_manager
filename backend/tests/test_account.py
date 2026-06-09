import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from tests import ensure_test_user, cleanup_test_user
from dao import AccountDAO
from service import AccountService
from db import connection_scope

_uid = None

def setUpModule():
    global _uid
    _uid = ensure_test_user("test_account_user")


def tearDownModule():
    cleanup_test_user("test_account_user")


class TestAccountDAO(unittest.TestCase):

    def setUp(self):
        with connection_scope() as conn:
            c = conn.cursor()
            c.execute("DELETE FROM transactions WHERE account_id IN (SELECT id FROM accounts WHERE name LIKE '测试%')")
            c.execute("DELETE FROM accounts WHERE name LIKE '测试%'")

    def test_create_account(self):
        a = AccountDAO.create(_uid, "测试账户", "bank", 1000.00)
        self.assertIsNotNone(a)
        self.assertEqual(a["name"], "测试账户")
        self.assertEqual(a["type"], "bank")
        self.assertEqual(float(a["balance"]), 1000.00)
        return a["id"]

    def test_get_all_accounts(self):
        self.test_create_account()
        accs = AccountDAO.get_all(_uid)
        self.assertGreaterEqual(len(accs), 1)

    def test_get_by_id(self):
        aid = self.test_create_account()
        a = AccountDAO.get_by_id(aid)
        self.assertIsNotNone(a)
        self.assertEqual(a["id"], aid)

    def test_update_account(self):
        aid = self.test_create_account()
        a = AccountDAO.update(aid, name="测试账户新名称")
        self.assertEqual(a["name"], "测试账户新名称")


class TestAccountService(unittest.TestCase):

    def setUp(self):
        with connection_scope() as conn:
            c = conn.cursor()
            c.execute("DELETE FROM transactions WHERE account_id IN (SELECT id FROM accounts WHERE name LIKE '测试%')")
            c.execute("DELETE FROM accounts WHERE name LIKE '测试%'")

    def test_add_valid(self):
        succ, r = AccountService.add(_uid, "测试服务账户", "alipay", 100.00)
        self.assertTrue(succ)
        self.assertEqual(r["name"], "测试服务账户")

    def test_add_empty_name(self):
        succ, msg = AccountService.add(_uid, "", "bank", 0)
        self.assertFalse(succ)
        self.assertEqual(msg, "名称不能为空")

    def test_add_negative_balance(self):
        succ, msg = AccountService.add(_uid, "测试", "bank", -100)
        self.assertFalse(succ)
        self.assertEqual(msg, "余额不能为负")


if __name__ == "__main__":
    unittest.main(verbosity=2)

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from tests import ensure_test_user, cleanup_test_user
from dao import AccountDAO, BudgetDAO
from service import BudgetService, TransactionService
from db import connection_scope

_uid = None

def setUpModule():
    global _uid
    _uid = ensure_test_user("test_budget_user")


def tearDownModule():
    cleanup_test_user("test_budget_user")


class TestBudgetDAO(unittest.TestCase):

    def setUp(self):
        with connection_scope() as conn:
            c = conn.cursor()
            c.execute("DELETE FROM budgets WHERE category='测试预算分类'")

    def test_set_budget(self):
        BudgetDAO.set(_uid, 2026, 6, "测试预算分类", 2000.00)
        budgets = BudgetDAO.get_all(_uid, 2026, 6)
        found = any(b["category"] == "测试预算分类" for b in budgets)
        self.assertTrue(found)

    def test_upsert_budget(self):
        BudgetDAO.set(_uid, 2026, 6, "测试预算分类", 2000.00)
        BudgetDAO.set(_uid, 2026, 6, "测试预算分类", 3000.00)
        budgets = BudgetDAO.get_all(_uid, 2026, 6)
        for b in budgets:
            if b["category"] == "测试预算分类":
                self.assertEqual(float(b["amount"]), 3000.00)


class TestBudgetService(unittest.TestCase):

    def setUp(self):
        with connection_scope() as conn:
            c = conn.cursor()
            c.execute("DELETE FROM budgets WHERE category='测试服务预算'")
            c.execute("DELETE FROM transactions WHERE account_id IN (SELECT id FROM accounts WHERE name LIKE '测试%')")
            c.execute("DELETE FROM accounts WHERE name LIKE '测试%'")

    def test_set_budget(self):
        succ, msg = BudgetService.set(_uid, 2026, 6, "测试服务预算", 3000.00)
        self.assertTrue(succ)

    def test_get_summary(self):
        BudgetService.set(_uid, 2026, 6, "测试服务预算", 1000.00)
        aid = AccountDAO.create(_uid, "测试预算账户", "bank", 5000.00)["id"]
        TransactionService.add(_uid, aid, "expense", "测试服务预算", 300.00)
        result = BudgetService.get_summary(_uid, 2026, 6)
        self.assertIn("summary", result)
        self.assertIn("warnings", result)


if __name__ == "__main__":
    unittest.main(verbosity=2)

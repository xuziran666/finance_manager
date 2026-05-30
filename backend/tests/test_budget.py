"""
个人收支财务管理系统 — 预算模块单元测试
运行方式：python -m pytest tests/test_budget.py -v
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from dao import AccountDAO, BudgetDAO
from service import BudgetService, TransactionService
from db import connection_scope


class TestBudgetDAO(unittest.TestCase):
    """预算数据访问层单元测试"""

    def setUp(self):
        with connection_scope() as conn:
            c = conn.cursor()
            c.execute("DELETE FROM budgets WHERE category='测试预算分类'")

    def test_set_budget(self):
        BudgetDAO.set(2026, 6, "测试预算分类", 2000.00)
        budgets = BudgetDAO.get_all(2026, 6)
        found = any(b["category"] == "测试预算分类" for b in budgets)
        self.assertTrue(found)

    def test_upsert_budget(self):
        BudgetDAO.set(2026, 6, "测试预算分类", 2000.00)
        BudgetDAO.set(2026, 6, "测试预算分类", 3000.00)
        budgets = BudgetDAO.get_all(2026, 6)
        for b in budgets:
            if b["category"] == "测试预算分类":
                self.assertEqual(float(b["amount"]), 3000.00)


class TestBudgetService(unittest.TestCase):
    """预算业务层单元测试"""

    def setUp(self):
        with connection_scope() as conn:
            c = conn.cursor()
            c.execute("DELETE FROM budgets WHERE category='测试服务预算'")
            c.execute("DELETE FROM transactions WHERE account_id IN (SELECT id FROM accounts WHERE name LIKE '测试%')")
            c.execute("DELETE FROM accounts WHERE name LIKE '测试%'")

    def test_set_budget(self):
        succ, msg = BudgetService.set(2026, 6, "测试服务预算", 3000.00)
        self.assertTrue(succ)

    def test_get_summary(self):
        BudgetService.set(2026, 6, "测试服务预算", 1000.00)
        aid = AccountDAO.create("测试预算账户", "bank", 5000.00)["id"]
        TransactionService.add(aid, "expense", "测试服务预算", 300.00)
        result = BudgetService.get_summary(2026, 6)
        self.assertIn("summary", result)
        self.assertIn("warnings", result)


if __name__ == "__main__":
    unittest.main(verbosity=2)

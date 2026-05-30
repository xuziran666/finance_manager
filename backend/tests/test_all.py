"""
个人收支财务管理系统 — 自动化测试脚本
运行方式：python -m pytest tests/test_all.py -v
或直接运行：python tests/test_all.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from datetime import datetime
from dao import AccountDAO, TransactionDAO, CategoryDAO, BudgetDAO, LogDAO
from service import AccountService, TransactionService, CategoryService, BudgetService, StatisticsService, LogService
from db import get_connection, connection_scope


class TestAccountDAO(unittest.TestCase):
    """账户数据访问层单元测试"""

    def setUp(self):
        """每个测试前清理测试数据"""
        with connection_scope() as conn:
            c = conn.cursor()
            c.execute("DELETE FROM transactions WHERE account_id IN (SELECT id FROM accounts WHERE name LIKE '测试%')")
            c.execute("DELETE FROM accounts WHERE name LIKE '测试%'")

    def test_create_account(self):
        """测试创建账户"""
        a = AccountDAO.create("测试账户", "bank", 1000.00)
        self.assertIsNotNone(a)
        self.assertEqual(a["name"], "测试账户")
        self.assertEqual(a["type"], "bank")
        self.assertEqual(float(a["balance"]), 1000.00)
        return a["id"]

    def test_get_all_accounts(self):
        """测试获取所有账户"""
        self.test_create_account()
        accs = AccountDAO.get_all()
        self.assertGreaterEqual(len(accs), 1)

    def test_get_by_id(self):
        """测试按ID查询账户"""
        aid = self.test_create_account()
        a = AccountDAO.get_by_id(aid)
        self.assertIsNotNone(a)
        self.assertEqual(a["id"], aid)

    def test_update_account(self):
        """测试更新账户"""
        aid = self.test_create_account()
        a = AccountDAO.update(aid, name="测试账户新名称")
        self.assertEqual(a["name"], "测试账户新名称")


class TestTransactionDAO(unittest.TestCase):
    """交易记录数据访问层单元测试"""

    def setUp(self):
        with connection_scope() as conn:
            c = conn.cursor()
            c.execute("DELETE FROM transactions WHERE account_id IN (SELECT id FROM accounts WHERE name LIKE '测试%')")
            c.execute("DELETE FROM accounts WHERE name LIKE '测试%'")
        self.aid = AccountDAO.create("测试交易账户", "bank", 5000.00)["id"]

    def test_create_transaction(self):
        """测试创建交易记录"""
        t = TransactionDAO.create(self.aid, "income", "工资", 3000.00, "测试收入")
        self.assertIsNotNone(t)
        self.assertEqual(float(t["amount"]), 3000.00)
        # 验证余额自动更新
        a = AccountDAO.get_by_id(self.aid)
        self.assertEqual(float(a["balance"]), 8000.00)

    def test_get_all_pagination(self):
        """测试分页查询"""
        for i in range(5):
            TransactionDAO.create(self.aid, "expense", "餐饮", 10.00 + i, f"测试{i}")
        r = TransactionDAO.get_all(account_id=self.aid, page=1, page_size=3)
        self.assertEqual(len(r["transactions"]), 3)
        self.assertEqual(r["total"], 5)
        self.assertEqual(r["total_pages"], 2)


class TestCategoryDAO(unittest.TestCase):
    """分类数据访问层单元测试"""

    def setUp(self):
        with connection_scope() as conn:
            c = conn.cursor()
            c.execute("DELETE FROM categories WHERE main='测试分类'")

    def test_create_category(self):
        """测试创建分类"""
        CategoryDAO.create("expense", "测试分类", "测试子分类")
        cats = CategoryDAO.get_all()
        found = any(c["main"] == "测试分类" for c in cats)
        self.assertTrue(found)

    def test_exists(self):
        """测试分类存在性检查"""
        CategoryDAO.create("expense", "测试分类", "测试子分类")
        self.assertTrue(CategoryDAO.exists("expense", "测试分类", "测试子分类"))
        self.assertFalse(CategoryDAO.exists("income", "测试分类", "测试子分类"))

    def test_get_tree(self):
        """测试分类树生成"""
        tree = CategoryDAO.get_tree()
        self.assertIn("income", tree)
        self.assertIn("expense", tree)


class TestBudgetDAO(unittest.TestCase):
    """预算数据访问层单元测试"""

    def setUp(self):
        with connection_scope() as conn:
            c = conn.cursor()
            c.execute("DELETE FROM budgets WHERE category='测试预算分类'")

    def test_set_budget(self):
        """测试设置预算"""
        BudgetDAO.set(2026, 6, "测试预算分类", 2000.00)
        budgets = BudgetDAO.get_all(2026, 6)
        found = any(b["category"] == "测试预算分类" for b in budgets)
        self.assertTrue(found)

    def test_upsert_budget(self):
        """测试预算覆盖更新"""
        BudgetDAO.set(2026, 6, "测试预算分类", 2000.00)
        BudgetDAO.set(2026, 6, "测试预算分类", 3000.00)
        budgets = BudgetDAO.get_all(2026, 6)
        for b in budgets:
            if b["category"] == "测试预算分类":
                self.assertEqual(float(b["amount"]), 3000.00)


class TestLogDAO(unittest.TestCase):
    """日志数据访问层单元测试"""

    def test_add_log(self):
        """测试添加日志"""
        LogDAO.add("TEST_ACTION", "测试日志")
        logs = LogDAO.get_all(limit=10)
        found = any(l["action"] == "TEST_ACTION" for l in logs)
        self.assertTrue(found)


class TestAccountService(unittest.TestCase):
    """账户业务层单元测试"""

    def setUp(self):
        with connection_scope() as conn:
            c = conn.cursor()
            c.execute("DELETE FROM transactions WHERE account_id IN (SELECT id FROM accounts WHERE name LIKE '测试%')")
            c.execute("DELETE FROM accounts WHERE name LIKE '测试%'")

    def test_add_valid(self):
        """测试添加有效账户"""
        succ, r = AccountService.add("测试服务账户", "alipay", 100.00)
        self.assertTrue(succ)
        self.assertEqual(r["name"], "测试服务账户")

    def test_add_empty_name(self):
        """测试添加空名称账户"""
        succ, msg = AccountService.add("", "bank", 0)
        self.assertFalse(succ)
        self.assertEqual(msg, "名称不能为空")

    def test_add_negative_balance(self):
        """测试添加负余额账户"""
        succ, msg = AccountService.add("测试", "bank", -100)
        self.assertFalse(succ)
        self.assertEqual(msg, "余额不能为负")


class TestTransactionService(unittest.TestCase):
    """交易记录业务层单元测试"""

    def setUp(self):
        with connection_scope() as conn:
            c = conn.cursor()
            c.execute("DELETE FROM transactions WHERE account_id IN (SELECT id FROM accounts WHERE name LIKE '测试%')")
            c.execute("DELETE FROM accounts WHERE name LIKE '测试%'")
        self.aid = AccountDAO.create("测试交易服务账户", "bank", 10000.00)["id"]

    def test_add_income(self):
        """测试添加收入"""
        succ, t = TransactionService.add(self.aid, "income", "工资", 5000.00)
        self.assertTrue(succ)

    def test_add_expense(self):
        """测试添加支出"""
        succ, t = TransactionService.add(self.aid, "expense", "餐饮", 100.00)
        self.assertTrue(succ)

    def test_transfer(self):
        """测试转账"""
        aid2 = AccountDAO.create("测试账户B", "alipay", 0.00)["id"]
        succ, msg = TransactionService.transfer(self.aid, aid2, 2000.00)
        self.assertTrue(succ)
        a1 = AccountDAO.get_by_id(self.aid)
        a2 = AccountDAO.get_by_id(aid2)
        self.assertEqual(float(a1["balance"]), 8000.00)
        self.assertEqual(float(a2["balance"]), 2000.00)

    def test_transfer_insufficient(self):
        """测试余额不足转账"""
        aid2 = AccountDAO.create("测试账户C", "cash", 0.00)["id"]
        succ, msg = TransactionService.transfer(self.aid, aid2, 999999.00)
        self.assertFalse(succ)

    def test_transfer_self(self):
        """测试自转账"""
        succ, msg = TransactionService.transfer(self.aid, self.aid, 100.00)
        self.assertFalse(succ)


class TestCategoryService(unittest.TestCase):
    """分类业务层单元测试"""

    def setUp(self):
        with connection_scope() as conn:
            c = conn.cursor()
            c.execute("DELETE FROM categories WHERE main='测试服务分类'")

    def test_add_category(self):
        """测试添加分类"""
        succ, msg = CategoryService.add("expense", "测试服务分类", "测试子")
        self.assertTrue(succ)

    def test_add_duplicate(self):
        """测试添加重复分类"""
        CategoryService.add("expense", "测试服务分类", "测试子")
        succ, msg = CategoryService.add("expense", "测试服务分类", "测试子")
        self.assertFalse(succ)


class TestBudgetService(unittest.TestCase):
    """预算业务层单元测试"""

    def setUp(self):
        with connection_scope() as conn:
            c = conn.cursor()
            c.execute("DELETE FROM budgets WHERE category='测试服务预算'")
            c.execute("DELETE FROM transactions WHERE account_id IN (SELECT id FROM accounts WHERE name LIKE '测试%')")
            c.execute("DELETE FROM accounts WHERE name LIKE '测试%'")

    def test_set_budget(self):
        """测试设置预算"""
        succ, msg = BudgetService.set(2026, 6, "测试服务预算", 3000.00)
        self.assertTrue(succ)

    def test_get_summary(self):
        """测试预算汇总"""
        BudgetService.set(2026, 6, "测试服务预算", 1000.00)
        aid = AccountDAO.create("测试预算账户", "bank", 5000.00)["id"]
        TransactionService.add(aid, "expense", "测试服务预算", 300.00)
        result = BudgetService.get_summary(2026, 6)
        self.assertIn("summary", result)
        self.assertIn("warnings", result)


class TestStatisticsService(unittest.TestCase):
    """统计业务层单元测试"""

    def test_get_statistics(self):
        """测试获取统计"""
        r = StatisticsService.get()
        self.assertIn("total_income", r)
        self.assertIn("total_expense", r)
        self.assertIn("balance", r)


if __name__ == "__main__":
    unittest.main(verbosity=2)

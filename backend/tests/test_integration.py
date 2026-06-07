"""
个人收支财务管理系统 — 集成测试
测试全栈流程：route → service → DAO → DB
运行方式：python -m pytest tests/test_integration.py -v
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import unittest
from app import app
from db import connection_scope


class TestAccountIntegration(unittest.TestCase):
    """账户模块全链路集成测试 (Flask TestClient)"""

    def setUp(self):
        self.client = app.test_client()
        with connection_scope() as conn:
            c = conn.cursor()
            c.execute("DELETE FROM transactions WHERE account_id IN (SELECT id FROM accounts WHERE name LIKE '集成测试%')")
            c.execute("DELETE FROM accounts WHERE name LIKE '集成测试%'")

    def test_full_account_lifecycle(self):
        """测试账户的完整生命周期：创建 → 查询列表 → 查询详情 → 更新 → 删除"""
        # 1. 创建账户
        resp = self.client.post("/api/accounts", json={
            "name": "集成测试账户", "type": "bank", "balance": 500.00
        })
        self.assertEqual(resp.status_code, 200)
        body = resp.get_json()
        self.assertEqual(body["code"], 200)
        data = body["data"]
        self.assertEqual(data["name"], "集成测试账户")
        self.assertEqual(data["type"], "bank")
        self.assertEqual(float(data["balance"]), 500.00)
        aid = data["id"]

        # 2. 获取账户列表 — 应包含刚创建的账户
        resp = self.client.get("/api/accounts")
        self.assertEqual(resp.status_code, 200)
        body = resp.get_json()
        self.assertEqual(body["code"], 200)
        ids = [a["id"] for a in body["data"]]
        self.assertIn(aid, ids)

        # 3. 更新账户名称
        resp = self.client.put(f"/api/accounts/{aid}", json={"name": "集成测试账户-已更新"})
        self.assertEqual(resp.status_code, 200)
        body = resp.get_json()
        self.assertEqual(body["code"], 200)
        self.assertEqual(body["data"]["name"], "集成测试账户-已更新")

        # 4. 删除账户
        resp = self.client.delete(f"/api/accounts/{aid}")
        self.assertEqual(resp.status_code, 200)
        body = resp.get_json()
        self.assertEqual(body["code"], 200)

        # 5. 确认已删除 — 列表中不应包含该账户
        resp = self.client.get("/api/accounts")
        ids = [a["id"] for a in resp.get_json()["data"]]
        self.assertNotIn(aid, ids)

    def test_create_account_validation(self):
        """测试账户创建的校验逻辑"""
        # 名称为空
        resp = self.client.post("/api/accounts", json={"name": "", "type": "bank"})
        self.assertEqual(resp.get_json()["code"], 400)

        # 余额为负
        resp = self.client.post("/api/accounts", json={"name": "集成测试校验", "type": "bank", "balance": -1})
        self.assertEqual(resp.get_json()["code"], 400)


class TestTransactionIntegration(unittest.TestCase):
    """交易模块全链路集成测试"""

    def setUp(self):
        self.client = app.test_client()
        with connection_scope() as conn:
            c = conn.cursor()
            c.execute("DELETE FROM transactions WHERE account_id IN (SELECT id FROM accounts WHERE name LIKE '集成测试%')")
            c.execute("DELETE FROM accounts WHERE name LIKE '集成测试%'")
        # 创建测试账户
        resp = self.client.post("/api/accounts", json={
            "name": "集成测试账户", "type": "bank", "balance": 1000.00
        })
        self.account = resp.get_json()["data"]

    def test_add_income_transaction(self):
        """添加收入交易 — 验证余额是否自动增加"""
        resp = self.client.post("/api/transactions", json={
            "account_id": self.account["id"],
            "type": "income",
            "category": "工资",
            "amount": 3000.00,
            "note": "集成测试收入",
            "date": "2026-06-01"
        })
        self.assertEqual(resp.status_code, 200)
        body = resp.get_json()
        self.assertEqual(body["code"], 200)
        self.assertEqual(body["data"]["type"], "income")
        self.assertEqual(float(body["data"]["amount"]), 3000.00)

    def test_add_expense_transaction(self):
        """添加支出交易 — 验证余额是否自动减少"""
        resp = self.client.post("/api/transactions", json={
            "account_id": self.account["id"],
            "type": "expense",
            "category": "餐饮",
            "subcategory": "午餐",
            "amount": 50.00,
            "note": "集成测试支出",
            "date": "2026-06-02"
        })
        self.assertEqual(resp.status_code, 200)
        body = resp.get_json()
        self.assertEqual(body["code"], 200)
        self.assertEqual(body["data"]["type"], "expense")

    def test_transfer_between_accounts(self):
        """测试账户间转账功能"""
        # 创建第二个账户
        resp = self.client.post("/api/accounts", json={
            "name": "集成测试账户2", "type": "alipay", "balance": 0.00
        })
        acc2 = resp.get_json()["data"]

        # 从第一个账户转 200 到第二个账户
        resp = self.client.post("/api/transactions/transfer", json={
            "from_account": self.account["id"],
            "to_account": acc2["id"],
            "amount": 200.00,
            "note": "集成测试转账"
        })
        self.assertEqual(resp.status_code, 200)
        body = resp.get_json()
        self.assertEqual(body["code"], 200)

    def test_transaction_validation(self):
        """测试交易创建的校验逻辑"""
        # 无账户
        resp = self.client.post("/api/transactions", json={
            "type": "expense", "category": "餐饮", "amount": 10
        })
        self.assertEqual(resp.get_json()["code"], 400)

        # 金额为负
        resp = self.client.post("/api/transactions", json={
            "account_id": self.account["id"],
            "type": "expense", "category": "餐饮", "amount": -10
        })
        self.assertEqual(resp.get_json()["code"], 400)

        # 类型错误
        resp = self.client.post("/api/transactions", json={
            "account_id": self.account["id"],
            "type": "invalid", "category": "餐饮", "amount": 10
        })
        self.assertEqual(resp.get_json()["code"], 400)


class TestCategoryIntegration(unittest.TestCase):
    """分类模块全链路集成测试"""

    def setUp(self):
        self.client = app.test_client()
        with connection_scope() as conn:
            c = conn.cursor()
            c.execute("DELETE FROM categories WHERE type='集成测试'")

    def test_category_crud(self):
        """测试分类的完整 CRUD 流程"""
        # 1. 创建分类
        resp = self.client.post("/api/categories", json={
            "type": "集成测试", "main": "集成测试主分类", "sub": ""
        })
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()["code"], 200)

        # 2. 查询分类 — 应包含新分类
        resp = self.client.get("/api/categories")
        self.assertEqual(resp.status_code, 200)
        flat = resp.get_json()["data"]["flat"]
        categories = [c for c in flat if c["type"] == "集成测试"]
        self.assertGreaterEqual(len(categories), 1)

        # 3. 更新分类
        resp = self.client.put("/api/categories", json={
            "old_type": "集成测试", "old_main": "集成测试主分类", "old_sub": "",
            "new_type": "集成测试", "new_main": "集成测试主分类-新", "new_sub": ""
        })
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()["code"], 200)

        # 4. 删除分类
        resp = self.client.delete("/api/categories", json={
            "type": "集成测试", "main": "集成测试主分类-新", "sub": ""
        })
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()["code"], 200)

    def test_add_duplicate_category(self):
        """测试重复分类校验"""
        self.client.post("/api/categories", json={
            "type": "集成测试", "main": "重复分类", "sub": ""
        })
        resp = self.client.post("/api/categories", json={
            "type": "集成测试", "main": "重复分类", "sub": ""
        })
        self.assertEqual(resp.get_json()["code"], 400)


class TestBudgetIntegration(unittest.TestCase):
    """预算模块全链路集成测试"""

    def setUp(self):
        self.client = app.test_client()
        with connection_scope() as conn:
            c = conn.cursor()
            c.execute("DELETE FROM budgets WHERE year=2026 AND month=6")

    def test_budget_crud(self):
        """测试预算的 CRUD 流程"""
        # 1. 设置预算
        resp = self.client.post("/api/budgets", json={
            "year": 2026, "month": 6, "category": "餐饮", "amount": 2000.00
        })
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()["code"], 200)

        # 2. 查询预算列表
        resp = self.client.get("/api/budgets?year=2026&month=6")
        self.assertEqual(resp.status_code, 200)
        budgets = resp.get_json()["data"]
        self.assertTrue(any(b["category"] == "餐饮" for b in budgets))

        # 3. 获取预算汇总
        resp = self.client.get("/api/budgets/summary?year=2026&month=6")
        self.assertEqual(resp.status_code, 200)
        summary = resp.get_json()["data"]
        self.assertIn("summary", summary)
        self.assertIn("warnings", summary)

        # 4. 删除预算
        resp = self.client.delete("/api/budgets", json={
            "year": 2026, "month": 6, "category": "餐饮"
        })
        self.assertEqual(resp.status_code, 200)

    def test_budget_validation(self):
        """测试预算设置的校验逻辑"""
        resp = self.client.post("/api/budgets", json={
            "year": 2026, "month": 6, "category": "餐饮", "amount": -100
        })
        self.assertEqual(resp.get_json()["code"], 400)


if __name__ == "__main__":
    unittest.main(verbosity=2)

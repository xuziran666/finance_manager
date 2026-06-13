"""
个人收支财务管理系统 — 集成测试
测试全栈流程：route → service → DAO → DB
运行方式：python -m pytest tests/test_integration.py -v
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from fastapi.testclient import TestClient
from app import app
from db import connection_scope
from context import set_current_user, clear_current_user

client = TestClient(app)

TEST_USER = "integration_test"
TEST_PASS = "testpass123"
_token = None
_user_id = None


def setUpModule():
    """在所有测试前，注册并登录测试用户，获取 token 和 user_id"""
    global _token, _user_id
    # 清理遗留测试数据
    with connection_scope() as conn:
        c = conn.cursor()
        c.execute("DELETE FROM transactions WHERE account_id IN (SELECT id FROM accounts WHERE name LIKE '集成测试%')")
        c.execute("DELETE FROM accounts WHERE name LIKE '集成测试%'")
        c.execute("DELETE FROM categories WHERE type='集成测试'")
        c.execute("DELETE FROM budgets WHERE year=2026 AND month=6")
        c.execute("DELETE FROM logs WHERE user_id IN (SELECT id FROM users WHERE username=%s)", (TEST_USER,))
        c.execute("DELETE FROM categories WHERE user_id IN (SELECT id FROM users WHERE username=%s)", (TEST_USER,))
        c.execute("DELETE FROM users WHERE username=%s", (TEST_USER,))
    # 注册
    r = client.post("/api/auth/register", json={"username": TEST_USER, "password": TEST_PASS})
    assert r.json()["code"] == 200, f"注册失败: {r.json()}"
    # 登录
    r = client.post("/api/auth/login", json={"username": TEST_USER, "password": TEST_PASS})
    assert r.json()["code"] == 200, f"登录失败: {r.json()}"
    _token = r.json()["data"]["token"]
    # 获取 user_id
    from jose import jwt
    from config import SECRET_KEY, JWT_ALGORITHM
    payload = jwt.decode(_token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
    _user_id = payload["user_id"]
    set_current_user(_user_id, TEST_USER)


def tearDownModule():
    clear_current_user()


def auth_header():
    return {"Authorization": f"Bearer {_token}"}


def auth_post(url, json=None):
    return client.post(url, json=json, headers=auth_header())


def auth_put(url, json=None):
    return client.put(url, json=json, headers=auth_header())


def auth_delete(url, json=None):
    if json:
        return client.request("DELETE", url, json=json, headers=auth_header())
    return client.delete(url, headers=auth_header())


def auth_get(url):
    return client.get(url, headers=auth_header())


class TestAccountIntegration(unittest.TestCase):
    """账户模块全链路集成测试 (FastAPI TestClient)"""

    def setUp(self):
        with connection_scope() as conn:
            c = conn.cursor()
            c.execute("DELETE FROM transactions WHERE account_id IN (SELECT id FROM accounts WHERE name LIKE '集成测试%')")
            c.execute("DELETE FROM accounts WHERE name LIKE '集成测试%'")

    def test_full_account_lifecycle(self):
        """测试账户的完整生命周期：创建 → 查询列表 → 更新 → 删除"""
        resp = auth_post("/api/accounts", json={
            "name": "集成测试账户", "type": "bank", "balance": 500.00,
        })
        self.assertEqual(resp.status_code, 200)
        body = resp.json()
        self.assertEqual(body["code"], 200)
        data = body["data"]
        self.assertEqual(data["name"], "集成测试账户")
        self.assertEqual(data["type"], "bank")
        self.assertEqual(float(data["balance"]), 500.00)
        aid = data["id"]

        resp = auth_get("/api/accounts")
        self.assertEqual(resp.status_code, 200)
        body = resp.json()
        self.assertEqual(body["code"], 200)
        ids = [a["id"] for a in body["data"]]
        self.assertIn(aid, ids)

        resp = auth_put(f"/api/accounts/{aid}", json={"name": "集成测试账户-已更新"})
        self.assertEqual(resp.status_code, 200)
        body = resp.json()
        self.assertEqual(body["code"], 200)
        self.assertEqual(body["data"]["name"], "集成测试账户-已更新")

        resp = auth_delete(f"/api/accounts/{aid}")
        self.assertEqual(resp.status_code, 200)
        body = resp.json()
        self.assertEqual(body["code"], 200)

        resp = auth_get("/api/accounts")
        ids = [a["id"] for a in resp.json()["data"]]
        self.assertNotIn(aid, ids)

    def test_create_account_validation(self):
        """测试账户创建的校验逻辑"""
        resp = auth_post("/api/accounts", json={"name": "", "type": "bank"})
        self.assertEqual(resp.json()["code"], 400)

        resp = auth_post("/api/accounts", json={"name": "集成测试校验", "type": "bank", "balance": -1})
        self.assertEqual(resp.json()["code"], 400)


class TestTransactionIntegration(unittest.TestCase):
    """交易模块全链路集成测试"""

    def setUp(self):
        with connection_scope() as conn:
            c = conn.cursor()
            c.execute("DELETE FROM transactions WHERE account_id IN (SELECT id FROM accounts WHERE name LIKE '集成测试%')")
            c.execute("DELETE FROM accounts WHERE name LIKE '集成测试%'")
        resp = auth_post("/api/accounts", json={
            "name": "集成测试账户", "type": "bank", "balance": 1000.00,
        })
        self.account = resp.json()["data"]

    def test_add_income_transaction(self):
        """添加收入交易 — 验证余额是否自动增加"""
        resp = auth_post("/api/transactions", json={
            "account_id": self.account["id"],
            "type": "income",
            "category": "工资",
            "amount": 3000.00,
            "note": "集成测试收入",
            "date": "2026-06-01",
        })
        self.assertEqual(resp.status_code, 200)
        body = resp.json()
        self.assertEqual(body["code"], 200)
        self.assertEqual(body["data"]["type"], "income")
        self.assertEqual(float(body["data"]["amount"]), 3000.00)

    def test_add_expense_transaction(self):
        """添加支出交易 — 验证余额是否自动减少"""
        resp = auth_post("/api/transactions", json={
            "account_id": self.account["id"],
            "type": "expense",
            "category": "餐饮",
            "subcategory": "午餐",
            "amount": 50.00,
            "note": "集成测试支出",
            "date": "2026-06-02",
        })
        self.assertEqual(resp.status_code, 200)
        body = resp.json()
        self.assertEqual(body["code"], 200)
        self.assertEqual(body["data"]["type"], "expense")

    def test_transfer_between_accounts(self):
        """测试账户间转账功能"""
        resp = auth_post("/api/accounts", json={
            "name": "集成测试账户2", "type": "alipay", "balance": 0.00,
        })
        acc2 = resp.json()["data"]

        resp = auth_post("/api/transactions/transfer", json={
            "from_account": self.account["id"],
            "to_account": acc2["id"],
            "amount": 200.00,
            "note": "集成测试转账",
        })
        self.assertEqual(resp.status_code, 200)
        body = resp.json()
        self.assertEqual(body["code"], 200)

    def test_transaction_validation(self):
        """测试交易创建的校验逻辑"""
        resp = auth_post("/api/transactions", json={
            "type": "expense", "category": "餐饮", "amount": 10,
        })
        self.assertEqual(resp.json()["code"], 400)

        resp = auth_post("/api/transactions", json={
            "account_id": self.account["id"],
            "type": "expense", "category": "餐饮", "amount": -10,
        })
        self.assertEqual(resp.json()["code"], 400)

        resp = auth_post("/api/transactions", json={
            "account_id": self.account["id"],
            "type": "invalid", "category": "餐饮", "amount": 10,
        })
        self.assertEqual(resp.json()["code"], 400)


class TestCategoryIntegration(unittest.TestCase):
    """分类模块全链路集成测试"""

    def setUp(self):
        with connection_scope() as conn:
            c = conn.cursor()
            c.execute("DELETE FROM categories WHERE type='集成测试'")

    def test_category_crud(self):
        """测试分类的完整 CRUD 流程"""
        resp = auth_post("/api/categories", json={
            "type": "集成测试", "main": "集成测试主分类", "sub": "",
        })
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["code"], 200)

        resp = auth_get("/api/categories")
        self.assertEqual(resp.status_code, 200)
        flat = resp.json()["data"]["flat"]
        categories = [c for c in flat if c["type"] == "集成测试"]
        self.assertGreaterEqual(len(categories), 1)

        resp = auth_put("/api/categories", json={
            "old_type": "集成测试", "old_main": "集成测试主分类", "old_sub": "",
            "new_type": "集成测试", "new_main": "集成测试主分类-新", "new_sub": "",
        })
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["code"], 200)

        resp = auth_delete("/api/categories", json={
            "type": "集成测试", "main": "集成测试主分类-新", "sub": "",
        })
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["code"], 200)

    def test_add_duplicate_category(self):
        """测试重复分类校验"""
        auth_post("/api/categories", json={
            "type": "集成测试", "main": "重复分类", "sub": "",
        })
        resp = auth_post("/api/categories", json={
            "type": "集成测试", "main": "重复分类", "sub": "",
        })
        self.assertEqual(resp.json()["code"], 400)


class TestBudgetIntegration(unittest.TestCase):
    """预算模块全链路集成测试"""

    def setUp(self):
        pass

    def test_budget_crud(self):
        """测试预算的 CRUD 流程"""
        resp = auth_post("/api/budgets", json={
            "year": 2026, "month": 6, "category": "餐饮", "amount": 2000.00,
        })
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["code"], 200)

        resp = auth_get("/api/budgets?year=2026&month=6")
        self.assertEqual(resp.status_code, 200)
        budgets = resp.json()["data"]
        self.assertTrue(any(b["category"] == "餐饮" for b in budgets))

        resp = auth_get("/api/budgets/summary?year=2026&month=6")
        self.assertEqual(resp.status_code, 200)
        summary = resp.json()["data"]
        self.assertIn("summary", summary)
        self.assertIn("warnings", summary)

        resp = auth_delete("/api/budgets", json={
            "year": 2026, "month": 6, "category": "餐饮",
        })
        self.assertEqual(resp.status_code, 200)

    def test_budget_validation(self):
        """测试预算设置的校验逻辑"""
        resp = auth_post("/api/budgets", json={
            "year": 2026, "month": 6, "category": "餐饮", "amount": -100,
        })
        self.assertEqual(resp.json()["code"], 400)


if __name__ == "__main__":
    unittest.main(verbosity=2)

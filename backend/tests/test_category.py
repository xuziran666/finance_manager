import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from tests import ensure_test_user, cleanup_test_user
from dao import CategoryDAO, LogDAO
from service import CategoryService
from db import connection_scope

_uid = None
category_dao = CategoryDAO()
log_dao = LogDAO()
category_service = CategoryService(category_dao, log_dao)

def setUpModule():
    global _uid
    _uid = ensure_test_user("test_category_user")

def tearDownModule():
    cleanup_test_user("test_category_user")

class TestCategoryDAO(unittest.TestCase):

    def setUp(self):
        with connection_scope() as conn:
            c = conn.cursor()
            c.execute("DELETE FROM categories WHERE main='测试分类'")

    def test_create_category(self):
        category_dao.create("expense", "测试分类", "测试子分类", user_id=_uid)
        cats = category_dao.get_all(_uid)
        found = any(c["main"] == "测试分类" for c in cats)
        self.assertTrue(found)

    def test_exists(self):
        category_dao.create("expense", "测试分类", "测试子分类", user_id=_uid)
        self.assertTrue(category_dao.exists(_uid, "expense", "测试分类", "测试子分类"))
        self.assertFalse(category_dao.exists(_uid, "income", "测试分类", "测试子分类"))

    def test_get_tree(self):
        tree = category_dao.get_tree(_uid)
        self.assertIn("income", tree)
        self.assertIn("expense", tree)

class TestCategoryService(unittest.TestCase):

    def setUp(self):
        with connection_scope() as conn:
            c = conn.cursor()
            c.execute("DELETE FROM categories WHERE main='测试服务分类'")

    def test_add_category(self):
        succ, msg = category_service.add(_uid, "expense", "测试服务分类", "测试子")
        self.assertTrue(succ)

    def test_add_duplicate(self):
        category_service.add(_uid, "expense", "测试服务分类", "测试子")
        succ, msg = category_service.add(_uid, "expense", "测试服务分类", "测试子")
        self.assertFalse(succ)

if __name__ == "__main__":
    unittest.main(verbosity=2)

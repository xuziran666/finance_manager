"""
个人收支财务管理系统 — 分类模块单元测试
运行方式：python -m pytest tests/test_category.py -v
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from dao import CategoryDAO
from service import CategoryService
from db import connection_scope


class TestCategoryDAO(unittest.TestCase):
    """分类数据访问层单元测试"""

    def setUp(self):
        with connection_scope() as conn:
            c = conn.cursor()
            c.execute("DELETE FROM categories WHERE main='测试分类'")

    def test_create_category(self):
        CategoryDAO.create("expense", "测试分类", "测试子分类")
        cats = CategoryDAO.get_all()
        found = any(c["main"] == "测试分类" for c in cats)
        self.assertTrue(found)

    def test_exists(self):
        CategoryDAO.create("expense", "测试分类", "测试子分类")
        self.assertTrue(CategoryDAO.exists("expense", "测试分类", "测试子分类"))
        self.assertFalse(CategoryDAO.exists("income", "测试分类", "测试子分类"))

    def test_get_tree(self):
        tree = CategoryDAO.get_tree()
        self.assertIn("income", tree)
        self.assertIn("expense", tree)


class TestCategoryService(unittest.TestCase):
    """分类业务层单元测试"""

    def setUp(self):
        with connection_scope() as conn:
            c = conn.cursor()
            c.execute("DELETE FROM categories WHERE main='测试服务分类'")

    def test_add_category(self):
        succ, msg = CategoryService.add("expense", "测试服务分类", "测试子")
        self.assertTrue(succ)

    def test_add_duplicate(self):
        CategoryService.add("expense", "测试服务分类", "测试子")
        succ, msg = CategoryService.add("expense", "测试服务分类", "测试子")
        self.assertFalse(succ)


if __name__ == "__main__":
    unittest.main(verbosity=2)

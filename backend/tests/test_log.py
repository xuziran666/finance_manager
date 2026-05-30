"""
个人收支财务管理系统 — 日志与统计模块单元测试
运行方式：python -m pytest tests/test_log.py -v
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from dao import LogDAO
from service import StatisticsService


class TestLogDAO(unittest.TestCase):
    """日志数据访问层单元测试"""

    def test_add_log(self):
        LogDAO.add("TEST_ACTION", "测试日志")
        logs = LogDAO.get_all(limit=10)
        found = any(l["action"] == "TEST_ACTION" for l in logs)
        self.assertTrue(found)


class TestStatisticsService(unittest.TestCase):
    """统计业务层单元测试"""

    def test_get_statistics(self):
        r = StatisticsService.get()
        self.assertIn("total_income", r)
        self.assertIn("total_expense", r)
        self.assertIn("balance", r)


if __name__ == "__main__":
    unittest.main(verbosity=2)

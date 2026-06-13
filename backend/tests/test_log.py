import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from tests import ensure_test_user, cleanup_test_user
from dao import LogDAO, TransactionDAO
from service import StatisticsService

_uid = None
log_dao = LogDAO()
transaction_dao = TransactionDAO()
statistics_service = StatisticsService(transaction_dao)

def setUpModule():
    global _uid
    _uid = ensure_test_user("test_log_user")

def tearDownModule():
    cleanup_test_user("test_log_user")

class TestLogDAO(unittest.TestCase):

    def test_add_log(self):
        log_dao.add(_uid, "TEST_ACTION", "测试日志")
        logs = log_dao.get_all(_uid, limit=10)
        found = any(l["action"] == "TEST_ACTION" for l in logs)
        self.assertTrue(found)

class TestStatisticsService(unittest.TestCase):

    def test_get_statistics(self):
        r = statistics_service.get(_uid)
        self.assertIn("total_income", r)
        self.assertIn("total_expense", r)
        self.assertIn("balance", r)

if __name__ == "__main__":
    unittest.main(verbosity=2)

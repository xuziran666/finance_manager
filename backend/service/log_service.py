from dao import LogDAO
from context import get_current_user_id


class LogService:

    def __init__(self, log_dao: LogDAO):
        self.log_dao = log_dao

    def get_all(self, limit=100):
        return self.log_dao.get_all(get_current_user_id(), limit)

from dao import LogDAO


class LogService:

    def __init__(self, log_dao: LogDAO):
        self.log_dao = log_dao

    def get_all(self, user_id, limit=100):
        return self.log_dao.get_all(user_id, limit)

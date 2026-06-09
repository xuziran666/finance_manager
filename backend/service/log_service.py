from dao import LogDAO


class LogService:

    @staticmethod
    def get_all(user_id, limit=100):
        return LogDAO.get_all(user_id, limit)

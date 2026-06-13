from datetime import datetime, timedelta, timezone
from jose import jwt
from config import SECRET_KEY, JWT_ALGORITHM, JWT_EXPIRE_MINUTES
from datetime import datetime, timedelta, timezone
from jose import jwt
from config import SECRET_KEY, JWT_ALGORITHM, JWT_EXPIRE_MINUTES
from dao import UserDAO, CategoryDAO
from db import connection_scope


class UserService:

    @staticmethod
    def register(username, password):
        user_dao = UserDAO()
        category_dao = CategoryDAO()
        if not username or not username.strip():
            return False, "用户名不能为空"
        if len(username.strip()) < 2:
            return False, "用户名至少2个字符"
        if not password or len(password) < 8:
            return False, "密码至少8位"
        with connection_scope() as conn:
            existing = user_dao.get_by_username(username.strip(), conn=conn)
            if existing:
                return False, "用户名已存在"
            user_id = user_dao.create(username.strip(), password, conn=conn)
            category_dao.copy_defaults(user_id, conn=conn)
            return True, "注册成功，请登录"

    @staticmethod
    def login(username, password):
        user_dao = UserDAO()
        if not username or not password:
            return False, "用户名和密码不能为空"
        with connection_scope() as conn:
            user = user_dao.get_by_username(username.strip(), conn=conn)
            if not user or user["id"] < 0:
                return False, "用户名或密码错误"
            if user["password_hash"] != password:
                return False, "用户名或密码错误"
            expire = datetime.now(timezone.utc) + timedelta(minutes=JWT_EXPIRE_MINUTES)
            token = jwt.encode(
                {"user_id": user["id"], "username": user["username"], "exp": expire},
                SECRET_KEY, algorithm=JWT_ALGORITHM,
            )
            return True, {"token": token, "username": user["username"]}

    @staticmethod
    def verify_token(token):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
            return payload
        except Exception:
            return None

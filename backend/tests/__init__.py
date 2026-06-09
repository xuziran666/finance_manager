from context import set_current_user, clear_current_user
from service import UserService
from db import connection_scope
from config import SECRET_KEY, JWT_ALGORITHM
from jose import jwt

_uid_map = {}

def ensure_test_user(username="unittest_user", password="testpass123"):
    if username in _uid_map:
        return _uid_map[username]
    with connection_scope() as conn:
        c = conn.cursor()
        c.execute("DELETE FROM logs WHERE user_id IN (SELECT id FROM users WHERE username=%s)", (username,))
        c.execute("DELETE FROM categories WHERE user_id IN (SELECT id FROM users WHERE username=%s)", (username,))
        c.execute("DELETE FROM transactions WHERE user_id IN (SELECT id FROM users WHERE username=%s)", (username,))
        c.execute("DELETE FROM accounts WHERE user_id IN (SELECT id FROM users WHERE username=%s)", (username,))
        c.execute("DELETE FROM budgets WHERE user_id IN (SELECT id FROM users WHERE username=%s)", (username,))
        c.execute("DELETE FROM users WHERE username=%s", (username,))
    succ, msg = UserService.register(username, password)
    if not succ:
        raise RuntimeError(f"注册测试用户[{username}]失败: {msg}")
    succ, data = UserService.login(username, password)
    if not succ:
        raise RuntimeError(f"登录测试用户[{username}]失败: {data}")
    payload = jwt.decode(data["token"], SECRET_KEY, algorithms=[JWT_ALGORITHM])
    uid = payload["user_id"]
    set_current_user(uid, username)
    _uid_map[username] = uid
    return uid

def cleanup_test_user(username="unittest_user"):
    if username in _uid_map:
        del _uid_map[username]
    clear_current_user()
    with connection_scope() as conn:
        c = conn.cursor()
        c.execute("DELETE FROM logs WHERE user_id IN (SELECT id FROM users WHERE username=%s)", (username,))
        c.execute("DELETE FROM categories WHERE user_id IN (SELECT id FROM users WHERE username=%s)", (username,))
        c.execute("DELETE FROM transactions WHERE user_id IN (SELECT id FROM users WHERE username=%s)", (username,))
        c.execute("DELETE FROM accounts WHERE user_id IN (SELECT id FROM users WHERE username=%s)", (username,))
        c.execute("DELETE FROM budgets WHERE user_id IN (SELECT id FROM users WHERE username=%s)", (username,))
        c.execute("DELETE FROM users WHERE username=%s", (username,))

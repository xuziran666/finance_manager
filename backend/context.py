"""当前用户上下文：基于 contextvars 实现请求级别的用户身份注入"""
import contextvars

_current_user = contextvars.ContextVar("_current_user", default=None)


def set_current_user(user_id: int, username: str):
    _current_user.set({"user_id": user_id, "username": username})


def clear_current_user():
    _current_user.set(None)


def get_current_user_id() -> int | None:
    u = _current_user.get()
    return u["user_id"] if u else None


def get_current_username() -> str | None:
    u = _current_user.get()
    return u["username"] if u else None

from fastapi import Header, HTTPException
from service import UserService
from context import set_current_user, clear_current_user


async def get_current_user(authorization: str = Header(...)):
    token = authorization.removeprefix("Bearer ")
    payload = UserService.verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="未登录或登录已过期")
    set_current_user(payload["user_id"], payload["username"])
    return payload


def clear_user_context(_=None):
    clear_current_user()

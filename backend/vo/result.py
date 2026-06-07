from pydantic import BaseModel
from typing import Any


class ApiResponse(BaseModel):
    code: int = 200
    msg: str = "成功"
    data: Any = None

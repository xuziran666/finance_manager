from pydantic import BaseModel
from typing import Optional


class AccountCreate(BaseModel):
    name: str
    type: str
    balance: float = 0


class AccountUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None

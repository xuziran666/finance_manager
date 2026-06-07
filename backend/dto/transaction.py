from pydantic import BaseModel
from typing import Optional


class TransactionCreate(BaseModel):
    account_id: Optional[int] = None
    type: str
    category: str
    amount: float
    note: str = ""
    date: str = ""
    subcategory: str = ""


class TransferCreate(BaseModel):
    from_account: int
    to_account: int
    amount: float
    note: str = ""

from pydantic import BaseModel


class BudgetSet(BaseModel):
    year: int
    month: int
    category: str
    amount: float


class BudgetDelete(BaseModel):
    year: int
    month: int
    category: str = ""

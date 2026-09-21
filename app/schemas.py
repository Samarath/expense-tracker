from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class ExpenseBase(BaseModel):
    # gt=0 ensures the amount is greater than zero
    amount: float = Field(..., gt=0, description="Expense amount must be positive")
    category: str
    note: Optional[str] = None
    date: date

class ExpenseCreate(ExpenseBase):
    pass

class ExpenseOut(ExpenseBase):
    id: int

    class Config:
        from_attributes = True
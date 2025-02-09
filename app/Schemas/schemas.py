from pydantic import BaseModel
from typing import List

class BacktestResult(BaseModel):
    status: str
    final_balance: float
    trades: List[str]

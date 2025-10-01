from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class PriceAlert:
    id: Optional[int]
    user_id: int
    symbol: str
    target_price: float
    condition: str
    is_active: bool
    created_at: datetime
    last_triggered: Optional[datetime]



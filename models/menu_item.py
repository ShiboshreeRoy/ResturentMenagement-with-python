from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

@dataclass
class MenuItem:
    name: str
    price: Decimal
    category: str
    description: Optional[str] = None
    image_path: Optional[str] = None
    is_available: bool = True
    preparation_time: int = 15  # in minutes
    calories: Optional[int] = None
    ingredients: Optional[list[str]] = None
    allergens: Optional[list[str]] = None

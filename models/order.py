from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from enum import Enum

class OrderStatus(Enum):
    PENDING = "Pending"
    PREPARING = "Preparing"
    READY = "Ready"
    DELIVERED = "Delivered"
    CANCELLED = "Cancelled"

class PaymentStatus(Enum):
    PENDING = "Pending"
    PAID = "Paid"
    REFUNDED = "Refunded"

@dataclass
class OrderItem:
    item_name: str
    quantity: int
    unit_price: Decimal
    subtotal: Decimal
    special_instructions: Optional[str] = None
    
@dataclass
class Order:
    id: int
    customer_id: int
    items: List[OrderItem]
    total_amount: Decimal
    status: OrderStatus
    payment_status: PaymentStatus
    payment_method: str
    table_number: Optional[int]
    waiter_name: Optional[str]
    order_date: datetime
    special_requests: Optional[str] = None
    estimated_preparation_time: Optional[int] = None

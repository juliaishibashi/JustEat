from pydantic import BaseModel
from datetime import datetime

from app.models.order_status import OrderStatus

class OrderItemCreate(BaseModel):
    menu_id: int
    quantity: int

class OrderCreate(BaseModel):
    restaurant_id: int
    items: list[OrderItemCreate]

class OrderRead(BaseModel):
    id: int
    customer_id: int
    restaurant_id: int
    status: OrderStatus
    created_at: datetime

    class Config:
        from_attributes = True

class OrderItemRead(BaseModel):
    menu_name: str
    quantity: int
    price: float

class OrderDetailRead(BaseModel):
    id: int
    restaurant_name: str
    status: OrderStatus
    created_at: datetime
    items: list[OrderItemRead]

class OrderStatusUpdate(BaseModel):
    status: OrderStatus

class OrderSummaryRead(OrderRead):
    total_price: float
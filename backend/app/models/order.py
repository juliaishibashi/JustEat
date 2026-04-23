from sqlalchemy import Column, Integer, ForeignKey, String, Numeric, Enum, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

from app.models.order_status import OrderStatus

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=False)
    status = Column(
        Enum(OrderStatus, name="order_status"),
        default=OrderStatus.PLACED,
        nullable=False,
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    items = relationship("OrderItem", backref="order", cascade="all, delete-orphan")
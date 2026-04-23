from enum import Enum

class OrderStatus(str, Enum):
    PLACED = "PLACED"
    CONFIRMED = "CONFIRMED"
    COMPLETED = "COMPLETED"
from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Enum
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.models.menu_special import MenuSpecialType


class Menu(Base):
    __tablename__ = "menus"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    detail = Column(String(255), nullable=True)

    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=False)
    
    
    special_type = Column(
        Enum(MenuSpecialType, name="menu_special_type"),
        nullable=False,
        default=MenuSpecialType.NONE,
    )

    restaurant = relationship("Restaurant", backref="menus")
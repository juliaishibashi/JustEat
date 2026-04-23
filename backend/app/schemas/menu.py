from pydantic import BaseModel
from app.models.menu_special import MenuSpecialType

class MenuCreate(BaseModel):
    name: str
    price: float
    detail: str | None = None
    restaurant_id: int
    special_type: MenuSpecialType = MenuSpecialType.NONE

class MenuRead(BaseModel):
    id: int
    name: str
    price: float
    detail: str | None = None
    restaurant_id: int
    special_type: MenuSpecialType

class MenuUpdate(BaseModel):
    name: str | None = None
    price: float | None = None
    detail: str | None = None
    special_type: MenuSpecialType | None = None

    class Config:
        from_attributes = True
from fastapi import APIRouter, HTTPException, status
from sqlalchemy.orm import Session

from app.models.menu import Menu
from app.models.restaurant import Restaurant
from app.schemas.menu import MenuCreate, MenuRead, MenuUpdate
from app.core.dependencies import DbDependency, CurrentUser, CurrentOwner

router = APIRouter(prefix="/menus", tags=["menus"])

@router.post("", response_model=MenuRead)
def create_menu(
    data: MenuCreate, db: DbDependency, owner: CurrentOwner
):
    restaurant = db.query(Restaurant).filter(Restaurant.id == data.restaurant_id).first()

    if not restaurant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")
    
    if restaurant.owner_id != owner.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to add menu to this restaurant")

    menu = Menu(
        name=data.name,
        price=data.price,
        detail=data.detail,
        restaurant_id=data.restaurant_id,
        special_type=data.special_type,
    )
    db.add(menu)
    db.commit()
    db.refresh(menu)
    return menu

@router.get("/{restaurant_id}", response_model=list[MenuRead])
def get_menu(restaurant_id: int, db: DbDependency, _: CurrentUser):
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()

    if not restaurant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")

    return db.query(Menu).filter(Menu.restaurant_id == restaurant_id).all()

@router.put("/{menu_id}", response_model=MenuRead)
def update_menu(menu_id: int, data: MenuUpdate, db: DbDependency, owner: CurrentOwner):
    menu = db.query(Menu).filter(Menu.id == menu_id).first()

    if not menu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu not found")

    restaurant = db.query(Restaurant).filter(Restaurant.id == menu.restaurant_id).first()

    if restaurant.owner_id != owner.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not the owner of this restaurant",
        )

    menu.name = data.name
    menu.price = data.price
    menu.detail = data.detail
    menu.special_type = data.special_type

    db.commit()
    db.refresh(menu)
    return menu

@router.delete("/{menu_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_menu(
    menu_id: int, db: DbDependency, owner: CurrentOwner
):

    menu = db.query(Menu).filter(Menu.id == menu_id).first()

    if not menu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu not found")

    restaurant = db.query(Restaurant).filter(Restaurant.id == menu.restaurant_id).first()

    if restaurant.owner_id != owner.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not the owner of this restaurant",
        )

    db.delete(menu)
    db.commit()
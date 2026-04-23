from fastapi import APIRouter, Depends, Query,  HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.user import User
from app.models.restaurant import Restaurant
from app.schemas.restaurant import RestaurantCreate,RestaurantUpdate,  RestaurantRead
from app.core.dependencies import DbDependency, CurrentUser, CurrentOwner


router = APIRouter(prefix='/restaurants', tags=['restaurants'])

@router.post('', response_model=RestaurantRead)
def create_restaurant(
    data: RestaurantCreate, db: DbDependency, owner: CurrentOwner
):

    restaurant = Restaurant(
        name=data.name,
        cuisine=data.cuisine,
        location=data.location,
        owner_id=owner.id,
    )
    db.add(restaurant)
    db.commit()
    db.refresh(restaurant)
    return restaurant

# Search restaurants by name, location or cuisine
@router.get('', response_model=list[RestaurantRead])
def search_restaurants(
    db: DbDependency,
    current_user: CurrentUser,
    search: str | None = None,
    cuisine: str | None = None,

):
    query = db.query(Restaurant)

    if search:
        query = query.filter(
            or_(
                Restaurant.name.ilike(f"%{search}%"),
                Restaurant.location.ilike(f"%{search}%"),
                Restaurant.cuisine.ilike(f"%{search}%"),
            )
        )
    
    if cuisine:
        query = query.filter(Restaurant.cuisine.ilike(f"%{cuisine}%"))
        
    return query.all()

@router.put("/{restaurant_id}", response_model=RestaurantRead)
def update_restaurant(
    restaurant_id: int,
    data: RestaurantUpdate,
    db: DbDependency,
    owner: CurrentOwner,
):
    restaurant = (
        db.query(Restaurant)
        .filter(Restaurant.id == restaurant_id)
        .first()
    )

    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found",
        )

    if restaurant.owner_id != owner.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to update this restaurant",
        )


    restaurant.name = data.name
    restaurant.location = data.location
    restaurant.cuisine = data.cuisine

    db.commit()
    db.refresh(restaurant)

    return restaurant

@router.delete("/{restaurant_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_restaurant(
    restaurant_id: int,
    db: DbDependency,
    owner: CurrentOwner,
):
    restaurant = (
        db.query(Restaurant)
        .filter(Restaurant.id == restaurant_id)
        .first()
    )

    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found",
        )

    if restaurant.owner_id != owner.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not the owner of this restaurant",
        )

    db.delete(restaurant)
    db.commit()
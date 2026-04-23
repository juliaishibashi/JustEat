from fastapi import APIRouter, HTTPException, status

from app.core.dependencies import DbDependency, CurrentUser
from app.models.favourites import Favourite

router = APIRouter(prefix="/favourites", tags=["favourites"])


@router.post("/restaurant/{restaurant_id}", status_code=status.HTTP_201_CREATED)
def add_favourite(
    restaurant_id: int,
    db: DbDependency,
    user: CurrentUser,
):
    existing = (
        db.query(Favourite)
        .filter(
            Favourite.user_id == user.id,
            Favourite.restaurant_id == restaurant_id,
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Restaurant already favourited",
        )

    fav = Favourite(
        user_id=user.id,
        restaurant_id=restaurant_id,
    )

    db.add(fav)
    db.commit()

    return {"ok": True}


@router.delete("/restaurant/{restaurant_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_favourite(
    restaurant_id: int,
    db: DbDependency,
    user: CurrentUser,
):
    deleted = (
        db.query(Favourite)
        .filter(
            Favourite.user_id == user.id,
            Favourite.restaurant_id == restaurant_id,
        )
        .delete()
    )

    if deleted == 0:
        raise HTTPException(
            status_code=404,
            detail="Favourite not found",
        )

    db.commit()


@router.get("/restaurants/me")
def get_my_favourites(
    db: DbDependency,
    user: CurrentUser,
):
    favourites = (
        db.query(Favourite.restaurant_id)
        .filter(Favourite.user_id == user.id)
        .all()
    )

    return [
        {"restaurant_id": fav.restaurant_id}
        for fav in favourites
    ]
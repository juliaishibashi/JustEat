import sys
sys.path.append("/app")

from app.db.database import SessionLocal
from app.models.restaurant import Restaurant
from app.models.user import User, UserRole


def seed_restaurants():
    print("=== USING UPDATED seed_restaurants.py ===")
    
    db = SessionLocal()

    owners = (
        db.query(User)
        .filter(User.role == UserRole.RESTAURANT_OWNER)
        .all()
    )

    if not owners:
        raise RuntimeError("No restaurant owners found. Seed users first.")

    restaurants_data = [
        ("Cat Coffee", "Victoria", "Cafe"),
        ("Ramen Arashi", "Victoria", "Japanese"),
        ("Gozen Sushi", "Victoria", "Japanese"),
        ("Ene", "Victoria", "Japanese"),
        ("Koguma Cafe", "Akasaka", "Cafe"),
        ("Akasaka Pizza", "Akasaka", "Italian"),
        ("Local Pizza", "Victoria", "Italian"),
        ("Curry House", "Shibuya", "Indian"),
        ("Fat Burger", "Victoria", "American"),
        ("Wolf Steak", "Roppongi", "Western"),
        ("Green Cafe", "Shibuya", "Cafe"),
    ]

    owner_index = 0

    for name, location, cuisine in restaurants_data:
        owner = owners[owner_index % len(owners)]
        owner_index += 1

        restaurant = Restaurant(
            name=name,
            location=location,
            cuisine=cuisine,
            owner_id=owner.id,
        )

        db.add(restaurant)

    db.commit()
    db.close()


if __name__ == "__main__":
    seed_restaurants()
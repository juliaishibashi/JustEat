import sys
sys.path.append("/app")

from decimal import Decimal

from app.db.database import SessionLocal
from app.models.menu import Menu
from app.models.restaurant import Restaurant
from app.models.menu_special import MenuSpecialType


def seed_menus():
    print("=== USING UPDATED seed_menus.py ===")

    db = SessionLocal()

    restaurants = db.query(Restaurant).all()
    if not restaurants:
        raise RuntimeError("No restaurants found. Seed restaurants first.")

    for restaurant in restaurants:
        menus = build_menu_templates(restaurant)

        for m in menus:
            db.add(
                Menu(
                    name=m["name"],
                    detail=m["detail"],
                    price=m["price"],
                    special_type=m["special_type"],
                    restaurant_id=restaurant.id,
                )
            )

    db.commit()
    db.close()


def build_menu_templates(restaurant: Restaurant):
    cuisine = restaurant.cuisine.lower()

    base = [
        {
            "name": f"{restaurant.name} Special Dish",
            "detail": "Chef's recommended signature dish",
            "price": Decimal("1500"),
            "special_type": MenuSpecialType.TODAYS_SPECIAL,
        },
        {
            "name": "Lunch Set",
            "detail": "Popular set menu for lunch time",
            "price": Decimal("1200"),
            "special_type": MenuSpecialType.DEAL_OF_THE_DAY,
        },
        {
            "name": "Regular Menu",
            "detail": "Standard menu loved by customers",
            "price": Decimal("900"),
            "special_type": MenuSpecialType.NONE,
        },
    ]

    cuisine_menus = {
        "cafe": [
            {"name": "House Blend Coffee", "detail": "Freshly brewed original blend", "price": Decimal("600"), "special_type": MenuSpecialType.NONE},
            {"name": "Cheesecake", "detail": "Creamy cheesecake with berry sauce", "price": Decimal("700"), "special_type": MenuSpecialType.NONE},
            {"name": "Honey Toast", "detail": "Thick toast with honey and ice cream", "price": Decimal("850"), "special_type": MenuSpecialType.NONE},
        ],
        "japanese": [
            {"name": "Tonkotsu Ramen", "detail": "Rich pork broth with noodles", "price": Decimal("950"), "special_type": MenuSpecialType.NONE},
            {"name": "Gyoza", "detail": "Pan-fried dumplings", "price": Decimal("450"), "special_type": MenuSpecialType.NONE},
            {"name": "Tempura Set", "detail": "Assorted tempura with dipping sauce", "price": Decimal("1100"), "special_type": MenuSpecialType.NONE},
        ],
        "italian": [
            {"name": "Carbonara", "detail": "Creamy carbonara with pancetta", "price": Decimal("1300"), "special_type": MenuSpecialType.NONE},
            {"name": "Margherita Pizza", "detail": "Classic pizza with tomato and basil", "price": Decimal("1200"), "special_type": MenuSpecialType.NONE},
            {"name": "Garlic Bread", "detail": "Crispy garlic bread with herbs", "price": Decimal("500"), "special_type": MenuSpecialType.NONE},
        ],
    }

    if cuisine in cuisine_menus:
        base.extend(cuisine_menus[cuisine])

    return base


if __name__ == "__main__":
    seed_menus()
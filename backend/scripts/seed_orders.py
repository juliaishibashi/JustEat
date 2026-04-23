import sys
sys.path.append("/app")

from app.db.database import SessionLocal
from app.models.user import User, UserRole
from app.models.restaurant import Restaurant
from app.models.menu import Menu
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.order_status import OrderStatus


def seed_orders():
    print("=== USING UPDATED seed_orders.py ===")

    db = SessionLocal()

    customers = (
        db.query(User)
        .filter(User.role == UserRole.CUSTOMER)
        .all()
    )

    restaurants = db.query(Restaurant).all()

    if not customers or not restaurants:
        raise RuntimeError("Customers or restaurants not found. Seed them first.")

    customer_index = 0

    for restaurant in restaurants:
        menus = (
            db.query(Menu)
            .filter(Menu.restaurant_id == restaurant.id)
            .all()
        )

        if len(menus) < 2:
            continue

        customer = customers[customer_index % len(customers)]
        customer_index += 1

        order = Order(
            customer_id=customer.id,
            restaurant_id=restaurant.id,
            status=OrderStatus.PLACED,
        )
        db.add(order)
        db.flush()

        for menu in menus[:3]:
            db.add(
                OrderItem(
                    order_id=order.id,
                    menu_id=menu.id,
                    quantity=1,
                    price=menu.price,
                )
            )

    db.commit()
    db.close()


if __name__ == "__main__":
    seed_orders()
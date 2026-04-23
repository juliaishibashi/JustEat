from fastapi import APIRouter, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import DbDependency, CurrentUser, CurrentOwner
from app.models import Order, OrderItem, Menu
from app.models.order_status import OrderStatus
from app.models.restaurant import Restaurant
from app.schemas.order import OrderCreate, OrderRead, OrderStatusUpdate, OrderDetailRead, OrderSummaryRead

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post(
    "",
    response_model=OrderSummaryRead,
    status_code=status.HTTP_201_CREATED,
)
def create_order(
    data: OrderCreate,
    db: DbDependency,
    customer: CurrentUser,
):
    order = Order(
        customer_id=customer.id,
        restaurant_id=data.restaurant_id,
        status=OrderStatus.PLACED,
    )
    db.add(order)
    db.commit()
    db.refresh(order)

    total_price = 0.0

    for item in data.items:
        menu_item = db.query(Menu).filter(Menu.id == item.menu_id).first()
        if not menu_item:
            raise HTTPException(
                status_code=404,
                detail=f"Menu item with id {item.menu_id} not found",
            )

        price = float(menu_item.price) * item.quantity
        total_price += price

        order_item = OrderItem(
            order_id=order.id,
            menu_id=item.menu_id,
            quantity=item.quantity,
            price=price,
        )
        db.add(order_item)

    db.commit()
    db.refresh(order)

    return OrderSummaryRead(
        **order.__dict__,
        total_price=total_price,
    )

@router.get("/me", response_model=list[OrderDetailRead])
def get_my_orders(
    db: DbDependency,
    customer: CurrentUser,
):
    orders = (
        db.query(Order)
        .filter(Order.customer_id == customer.id)
        .order_by(Order.created_at.desc())
        .all()
    )

    result = []

    for order in orders:
        restaurant = (
            db.query(Restaurant)
            .filter(Restaurant.id == order.restaurant_id)
            .first()
        )

        items = []
        for item in order.items:
            menu = db.query(Menu).filter(Menu.id == item.menu_id).first()
            items.append(
                {
                    "menu_name": menu.name,
                    "quantity": item.quantity,
                    "price": float(item.price),
                }
            )

        result.append(
            {
                "id": order.id,
                "restaurant_name": restaurant.name,
                "status": order.status,
                "created_at": order.created_at,
                "items": items,
            }
        )

    return result

@router.get("/owner", response_model=list[OrderRead])
def get_owner_orders(
    db: DbDependency,
    owner: CurrentOwner,
):
    return (
        db.query(Order)
        .join(Restaurant, Order.restaurant_id == Restaurant.id)
        .filter(Restaurant.owner_id == owner.id)
        .order_by(Order.created_at.desc())
        .all()
    )

@router.patch("/{order_id}/status", response_model=OrderRead)
def update_order_status(
    order_id: int,
    data: OrderStatusUpdate,
    db: DbDependency,
    owner: CurrentOwner,
):
    order = (
        db.query(Order)
        .join(Restaurant, Order.restaurant_id == Restaurant.id)
        .filter(
            Order.id == order_id,
            Restaurant.owner_id == owner.id,
        )
        .first()
    )

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found or not allowed",
        )

    order.status = data.status
    db.commit()
    db.refresh(order)

    return order
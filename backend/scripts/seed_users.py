import sys

sys.path.append("/app")

from app.db.database import SessionLocal
from app.core.security import hash_password
from app.models.user import User, UserRole

def seed_users():
    print("=== USING UPDATED seed_users.py ===")

    db = SessionLocal()

    users = [
        {
            "email": "customer1@test.com",
            "password": "customer123",
            "name": "Customer One",
            "role": UserRole.CUSTOMER,
        },
        {
            "email": "customer2@test.com",
            "password": "customer123",
            "name": "Customer Two",
            "role": UserRole.CUSTOMER,
        },
        {
            "email": "owner2@test.com",
            "password": "owner123",
            "name": "Owner Two",
            "role": UserRole.RESTAURANT_OWNER,
        },
        {
            "email": "owner3@test.com",
            "password": "owner123",
            "name": "Owner Three",
            "role": UserRole.RESTAURANT_OWNER,
        },
    ]

    for u in users:
        user = User(
            email=u["email"],
            hashed_password=hash_password(u["password"]),
            name=u["name"],
            role=u["role"],
        )
        db.add(user)

    db.commit()
    db.close()

if __name__ == "__main__":
    seed_users()
# JustEat Backend Application

## Overview

This project is a backend application inspired by food delivery services such as JustEat.

Users can:

- Browse restaurants by location, cuisine, or name
- View restaurant menus
- See special menus (Today's Special and Deal of the Day)
- Place orders as customers

Restaurant owners can:

- Manage their own restaurants
- Manage menus and special offers
- Update order status

The project focuses on clean backend architecture, data consistency,
and full reproducibility through seed scripts.

## Tech Stack

Backend:

- FastAPI
- SQLAlchemy (ORM)
- PostgreSQL

Database & Migration:

- Alembic

Environment:

- Docker
- Docker Compose

## User Roles & Permissions

Roles:

- CUSTOMER
- RESTAURANT_OWNER

Permissions:

- Customers can browse restaurants, view menus, and place orders
- Restaurant owners can create and manage only their own restaurants and menus
- Owners cannot access or modify other owners' data

## Database Design

Main entities:

- User
- Restaurant
- Menu
- Order
- OrderItem

Relationships:

- One Restaurant Owner can have multiple Restaurants
- One Restaurant has multiple Menus
- One Order contains multiple OrderItems
- Orders belong to Customers

## Menu Special Design

Menu specials are managed using an Enum:

- NONE
- TODAYS_SPECIAL
- DEAL_OF_THE_DAY

Each restaurant is seeded so that:

- Exactly one menu is marked as Today's Special
- Exactly one menu is marked as Deal of the Day

This ensures consistency and easy frontend display.

## Search & Pagination

Restaurants can be searched by:

- Location
- Cuisine
- Restaurant name (partial match)

Pagination is supported using:

- limit
- offset

## Seed Data Philosophy

This project emphasizes reproducibility.

All seed scripts:

- Remove existing data
- Reset ID sequences
- Insert deterministic demo data

This guarantees that:

- IDs are predictable
- No manually inserted data remains
- The same dataset can always be recreated

## Reset Database and Seed Data

WARNING:
The following commands delete existing data.

1. Reset tables and IDs:

TRUNCATE
order_items,
orders,
menus,
restaurants
RESTART IDENTITY CASCADE;

2. Seed users:

docker compose run --rm backend python scripts/seed_users.py

3. Seed restaurants:

docker compose run --rm backend python scripts/seed_restaurants.py

4. Seed menus:

docker compose run --rm backend python scripts/seed_menus.py

5. Seed orders:

docker compose run --rm backend python scripts/seed_orders.py

## Test Users

Customer account:

- Email: customer@test.com
- Password: customer123

Restaurant owner account:

- Email: owner@test.com
- Password: owner123

## Example API Endpoints

Browse restaurants:
GET /restaurants?location=Shibuya
GET /restaurants?cuisine=Cafe
GET /restaurants?name=Pizza

View menus:
GET /menus/restaurant/{restaurant_id}

Place an order:
POST /orders

Update order status (owner only):
PUT /orders/{order_id}/status

## Development Notes

- Seed scripts use TRUNCATE + RESTART IDENTITY for full data reset
- Raw SQL in seed scripts is wrapped using sqlalchemy.text
- All seed scripts are intended for development/demo environments only

## Frontend Integration

This backend is designed to be consumed by a frontend application.

Seeded data provides:

- Meaningful restaurant diversity
- Consistent menu structures
- Visible special menu flags

This allows the frontend to focus on UI/UX without worrying about data inconsistency.

## Status

Backend core features are complete and ready for frontend integration.

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from fastapi.middleware.cors import CORSMiddleware


from app.db.database import SessionLocal, get_db
from app.routers import auth, restaurants, menus, orders, favourites


app = FastAPI(title="JustEat Backend API", version="0.1.0")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(restaurants.router)
app.include_router(favourites.router)
app.include_router(menus.router)
app.include_router(orders.router)

@app.get("/")
def health_check():
    return {"status": "ok", "service": "JustEat backend"}

@app.get("/db-test")
def db_test(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT 1")).fetchone()
        return {"db_connection": "successful", "result": result[0]}
    except Exception as e:
        return {"db_connection": "failed", "error": str(e)}

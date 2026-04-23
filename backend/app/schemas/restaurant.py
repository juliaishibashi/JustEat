from pydantic import BaseModel

class RestaurantCreate(BaseModel):
    name: str
    cuisine: str
    location: str

class RestaurantUpdate(BaseModel):
    name: str | None = None
    cuisine: str | None = None
    location: str | None = None

class RestaurantRead(BaseModel):
    id: int
    name: str
    cuisine: str
    location: str

    class Config:
        from_attributes = True
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated

from app.models.user import User
from app.db.database import get_db
from app.schemas.auth import TokenResponse, ReadUser
from app.curd.user import get_user_by_email
from app.core.security import verify_password, create_access_token
from app.core.dependencies import DbDependency, CurrentUser


router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=TokenResponse)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: DbDependency):
    user = get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",)
    
    token = create_access_token({"sub": str(user.id), "email": user.email, "role": user.role.value})

    return {"access_token": token}
    
@router.get("/me")
def read_me(current_user: CurrentUser):
    return {
        'id': current_user.id,
        'name': current_user.name,
    }

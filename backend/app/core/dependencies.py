from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from typing import Annotated

from app.db.database import get_db
from app.models.user import UserRole, User
from app.core.config import settings

auth2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/login")
DbDependency = Annotated[Session, Depends(get_db)]

def get_current_user(token: Annotated[str, Depends(auth2_bearer)], db: DbDependency) -> User:

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

        # user_id = payload.get("sub")
        user_id: str | None = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",)
        
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",)
        
    user = db.query(User).filter(User.id == int(user_id)).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",)

    return user

CurrentUser = Annotated[User, Depends(get_current_user)]

def get_current_owner(current_user: CurrentUser) -> User:
    
    if current_user.role != UserRole.RESTAURANT_OWNER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Owner privileges required')
    
    return current_user

CurrentOwner = Annotated[User, Depends(get_current_owner)]
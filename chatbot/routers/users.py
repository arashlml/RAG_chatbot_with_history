from fastapi import Depends, HTTPException, APIRouter
from passlib.context import CryptContext

from starlette import status
from sqlalchemy.orm import Session
from typing import Annotated
from .auth import get_current_user, get_db
from ..model import Users

router = APIRouter(prefix="/users",
                tags=["users"])


db_dependency = Annotated[Session , Depends(get_db)]
user_dependency = Annotated[dict , Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(password, hashed_password):
    return bcrypt_context.verify(password, hashed_password)

@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(db:db_dependency,user:user_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="unauthorized")
    user_model=db.query(Users).filter(Users.id==user.get("id")).first()
    return user_model

@router.put("/update_password", status_code=status.HTTP_204_NO_CONTENT)
async def update_password(user:user_dependency,db:db_dependency,new_password: str,password: str):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="unauthorized")
    user_model = db.query(Users).filter(Users.id==user.get("id")).first()
    if not verify_password(password, user_model.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="incorrect password")
    user_model.hashed_password = bcrypt_context.hash(new_password)
    db.add(user_model)
    db.commit()

@router.put("/update_username", status_code=status.HTTP_204_NO_CONTENT)
async def update_username(db:db_dependency,user: user_dependency,password: str,new_username: str):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="unauthorized")
    updating_user = db.query(Users).filter(Users.id==user.get("id")).first()
    if not verify_password(password , updating_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="incorrect password")
    updating_user.username = new_username
    db.add(updating_user)
    db.commit()






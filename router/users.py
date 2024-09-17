from fastapi import APIRouter, HTTPException, Path
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette import status
from typing import Annotated

from database import SessionLocal
from models import Todos, Users
from router.auth import get_current_user

router = APIRouter(
    prefix='/users',
    tags=['users']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get('/', status_code=status.HTTP_200_OK)
async def read_user(user: user_dependency, db: db_dependency):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Failed authentication')
    return db.query(Users).filter(Users.id == user.get('id')).first()

#@router.put('/password', status_code=status.HTTP_200_OK)
#async def change_password():
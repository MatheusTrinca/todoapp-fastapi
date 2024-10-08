from fastapi import APIRouter, HTTPException, Path
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette import status
from typing import Annotated

from database import SessionLocal
from models import Todos
from .auth import get_current_user

router = APIRouter(
    prefix='/admin',
    tags=['admin']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/todos", status_code=status.HTTP_200_OK)
async def admin_read_all(user: user_dependency, db: db_dependency):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Failed authentication')
    return db.query(Todos).all()


@router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def admin_delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Failed authentication')
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()

    if todo_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo with id {todo_id} not found")
    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()

    
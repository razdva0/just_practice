from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models import User
from app.models.base import get_db
from app.schemas.users import Users

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/create")
async def create(user: Users, db: Session = Depends(get_db)):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get("/")
async def list(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


@router.get("/{id}")
async def get(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    return user


@router.delete("/{id}/delete")
async def delete(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    db.delete(user)
    db.commit()
    return user

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.auth import get_session
from app.crud.users import crud_user
from app.schemas.users import UserOut, UserCreate, UserInDB, UserUpdate
from app.security import get_password_hash

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/create", response_model=UserOut)
async def create(user_in: UserCreate, session: Session = Depends(get_session)):
    user = await crud_user.get(session, email=user_in.email)
    if user is not None:
        raise HTTPException(status_code=409, detail="User already exists")
    obj_in = UserInDB(**user_in.model_dump(), hashed_password=get_password_hash(user_in.password))
    user = await crud_user.create(session, obj_in)
    return user


@router.get("/", response_model=list[UserOut])
async def list(
    offset: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    users = await crud_user.list(session, offset, limit)
    return users


@router.get("/{id}")
async def get(user_id: int, db: Session = Depends(get_session)):
    user = await crud_user.get(id=user_id, db=db)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        pass
    except IntegrityError:
        raise HTTPException(status_code=409, detail="User already exists")
    return user


@router.put("/{id}/update", response_model=UserOut)
async def update(user_id: int, user_in: UserUpdate, session: Session = Depends(get_session)):
    user = await crud_user.get(session, id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        user = await crud_user.update(
            session,
            id=user_id,
            obj_in={
                **user_in.model_dump(exclude={"password"}, exclude_none=True),
                "hashed_password": get_password_hash(user_in.password),
            },
        )
    except IntegrityError:
        raise HTTPException(status_code=409, detail="User already exists")
    return user


@router.delete("/{id}/delete", status_code=204)
async def delete(user_id: int, session: Session = Depends(get_session)):
    user = await crud_user.get(session, id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    await crud_user.delete(session, db_obj=user)

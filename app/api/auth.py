from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import CONFIG
from app.crud.users import crud_user
from app.models import User
from app.models.base import SessionLocal
from app.schemas.token import TokenPayload

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")


async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session


def get_token_data(token: str = Depends(oauth2_scheme)) -> TokenPayload:
    try:
        SECRET_KEY = CONFIG.main.secret_key
        ALGORITHM = CONFIG.jwt.algorithm
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    return token_data


async def get_current_user(
    token: str = Depends(get_token_data),
    session: AsyncSession = Depends(get_session),
) -> User:
    user = await crud_user.get(session, id=token.user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user


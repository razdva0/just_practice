from datetime import timedelta, datetime
from typing import Optional

from jose import jwt
from passlib.context import CryptContext
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import CONFIG
from app.crud.users import crud_user
from app.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(user: User) -> str:
    SECRET_KEY = CONFIG.main.secret_key
    ACCESS_TTL = CONFIG.jwt.access_ttl
    ALGORITHM = CONFIG.jwt.algorithm
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TTL)
    return jwt.encode(
        {"exp": expire, "user_id": str(user.id)},
        key=SECRET_KEY,
        algorithm=ALGORITHM,
    )


def is_valid_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


async def authenticate(
    session: AsyncSession, email: EmailStr, password: str
) -> Optional[User]:
    user = await crud_user.get(session, email=email)
    if user is not None and is_valid_password(password, user.hashed_password):
        return user
    return None

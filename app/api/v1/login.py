from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth import get_session
from app.schemas.token import Token
from app.security import authenticate, create_access_token

router = APIRouter(prefix="/login", tags=["login"])


@router.post("/", response_model=Token)
async def login(
    data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
):
    user = await authenticate(session, email=data.username, password=data.password)
    if user is None:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    return {"access_token": create_access_token(user), "token_type": "bearer"}

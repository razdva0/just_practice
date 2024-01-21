from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from app.config import CONFIG

engine = create_async_engine(
    "postgresql+asyncpg://"
    f"{CONFIG.db.user}:"
    f"{CONFIG.db.password}@"
    f"{CONFIG.db.host}:"
    f"{CONFIG.db.port}/"
    f"{CONFIG.db.name}",
    echo=True,
)

SessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


class Base(DeclarativeBase):
    pass
    
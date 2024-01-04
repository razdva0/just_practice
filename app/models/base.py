from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import CONFIG

engine = create_engine(
    "postgresql://"
    f"{CONFIG.db.user}:"
    f"{CONFIG.db.password}@"
    f"{CONFIG.db.host}:"
    f"{CONFIG.db.port}/"
    f"{CONFIG.db.name}",
    echo=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    
from sqlalchemy import create_engine

from app.config import CONFIG

engine = create_engine(
    "postgresql://"
    f"{CONFIG.database.user}:"
    f"{CONFIG.database.password}@"
    f"{CONFIG.database.host}:"
    f"{CONFIG.database.port}/"
    f"{CONFIG.database.name}",
    echo=True,
)
